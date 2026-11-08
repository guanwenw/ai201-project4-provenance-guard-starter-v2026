# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard is a small backend a writing site could plug into. Here is the
path a submission takes, from arriving to the label a reader sees:

1. **`POST /submit` arrives** with `{"text": ..., "creator_id": ...}` — the
   writing and who submitted it.
2. **The input is checked** — missing, empty, or too-short text is rejected
   with a 4xx and a rejection log entry, before the model runs.
3. **A `content_id` is generated** (`uuid`) — the identity `/appeal` will need.
4. **Signal one reads the text for meaning** (`detector.model_signal`): how
   predictable it is to a local language model, 0–1, higher = more AI.
5. **Signal two measures the text as text** (`stylometry.style_signal`):
   sentence-length spread, word variety, punctuation density, 0–1, higher =
   more AI.
6. **The two scores are combined** into one confidence
   (`scoring.combine_signals`) and turned into a label a reader sees
   (`scoring.score_to_label`).
7. **The decision is logged** (`audit.log_decision`) as one JSON line in the
   append-only audit log, and JSON comes back with `content_id`, `guess`,
   `confidence`, `label`, and both signal scores.

If the writer thinks the guess is wrong, `POST /appeal` records their reasoning,
moves the item to `under_review`, and leaves the original decision in the log —
no automatic re-check, a person is in the loop.

---

## Signals and Scoring

### Signal one — the model signal, `scoring.py::combine_signals`

**What it measures:** text predictability (perplexity) using a local language model.
Lower perplexity → higher AI score. Direction: higher = more likely AI.

**Why that might differ between human and AI writing:** generated text tends to use high-probability word choices;
human writing contains more unexpected turns and specific phrasing.

**What it can't see:** predictability is not authorship. Plain, short-sentence writing
— common in second-language writing or deliberately simple prose — scores as
machine-like. Conversely, dense prose with rare vocabulary often scores as
human. The signal is structurally biased against writers with the least room to
argue back.

### Signal two — the style signal, `stylometry.style_signal`

**What it measures:** structural features only — sentence-length spread (stdev / mean),
type-token ratio, punctuation density. Direction after normalisation: higher =
more likely AI.

**Why that might differ between human and AI writing:** generated prose trends toward uniform sentence length and
narrower vocabulary; human writing is more variable.

**What it can't see:** it cannot read. Any change to shape without change to substance
— typos, fragmented sentences, inserted quotations — moves the score. It is
cheap to manipulate and degrades on longer texts.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** weighted average of the two signals, with a disagreement pull. Model
signal weight 0.6; style signal weight 0.4. When the two differ by more than
0.4, the combined score is pulled 20% toward 0.5.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.6`, `WEIGHT_STYLE_SIGNAL = 0.4`,
disagreement threshold `0.4`, pull `0.2`.

**Where it lives:** plain-human short text scored model 0.8311 / style 0.1985
(difference 0.63). The weighted average is 0.5781; the disagreement pull moves
it to 0.5624, producing "unsure" — the correct response when two methods
disagree strongly.

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** 

a plain, short-sentence paragraph scored model 0.8311 / style 0.2523 — a split of
0.5788, above the 0.4 threshold. The model found the short, ordinary sentences
very predictable (high AI score); the style signal found the irregular sentence
lengths and dense punctuation very human (low AI score). The weighted average
would be 0.5996, but because the two disagree by more than 0.4 the rule pulls it
20% toward 0.5, landing at 0.5797 — "unsure", the honest answer when the two
methods disagree this hard.

**Calibration (Unit 7):** four calibration inputs produced confidence values of
0.34–0.52. The clear-AI vs clear-human gap was below the M2 criterion 2 target
of 0.30. The style signal assigns relatively high AI scores to human-leaning
text, compressing the gap. Recorded here; Unit 8 diagnoses and addresses it

---

## Label Variants

| Label | Score range | Reader-facing text |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "This writing looks like a person wrote it." |
| unsure | 0.35 – 0.65 | "We can't tell whether a person or a machine wrote this, so we're not labelling it either way." |
| high-confidence AI | 0.65 – 1.00 | "This writing looks machine-generated to us." |

**Why I worded the "unsure" one this way:** the label must acknowledge uncertainty without
implying suspicion. "We can't tell ... so we're not labelling it either way"
places the limitation on the system, not the writer.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text":"Remote work has reshaped how teams communicate. Managers must establish clear expectations around availability and response times. Regular check-ins help maintain alignment without creating unnecessary meetings. Teams that document decisions well tend to coordinate more smoothly across time zones.","creator_id":"m5_reviewer"}'
```

```json
{
  "confidence": 0.3673,
  "content_id": "c0ef60b2-cbe8-4cce-986e-86889a70121f",
  "guess": "unsure",
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "model_score": 0.2868,
  "style_score": 0.4881
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id":"c0ef60b2-cbe8-4cce-986e-86889a70121f","reasoning":"This paragraph is from a report I drafted for work last month. I can send the original document if needed."}'
```

```json
{
  "content_id": "c0ef60b2-cbe8-4cce-986e-86889a70121f",
  "message": "Appeal received. A person will review this decision and follow up.",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.3673,
      "content_id": "c0ef60b2-cbe8-4cce-986e-86889a70121f",
      "creator_id": "m5_reviewer",
      "guess": "unsure",
      "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
      "model_score": 0.2868,
      "status": "decided",
      "style_score": 0.4881,
      "timestamp": "2026-11-02T02:21:31+00:00"
    },
    {
      "combined_score": 0.3673,
      "content_id": "491fc438-bef0-40b3-83bb-e5a8aedb9c7d",
      "creator_id": "m5_reviewer",
      "guess": "unsure",
      "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
      "model_score": 0.2868,
      "status": "decided",
      "style_score": 0.4881,
      "timestamp": "2026-11-02T02:21:51+00:00"
    },
    {
      "content_id": "c0ef60b2-cbe8-4cce-986e-86889a70121f",
      "creator_id": "m5_reviewer",
      "event": "appeal",
      "reasoning": "This paragraph is from a report I drafted for work last month. I can send the original document if needed.",
      "status": "under_review",
      "timestamp": "2026-11-02T02:22:27+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* help articulating each signal's blind spot and drafting three label
    texts.
- *What came back:* an explanation of the model signal's bias toward plain writing and
    three candidate labels.
- *What I changed:* retained the blind-spot analysis but rewrote all three labels to
    remove technical phrasing ("generated by AI", "confidence 0.81"). Final
    wording is plain sentences a non-technical reader can act on.

**Moment 2**

- *What I asked for:* why app.py attempted to reach huggingface.co on startup despite the
    model being downloaded.
- *What came back:* confirmation that a separate process does not inherit
    HF_HUB_OFFLINE set in another terminal.
- *What I changed:* set HF_HUB_OFFLINE=1 in the terminal that launches app.py, and
    documented it so Unit 8's run_attacks.py and run_eval.py avoid the same
    failure. 

**Moment 3**

- *What I asked for:* whether the body-type check I added actually fixed RQ07,
  or whether I was reading the after-run too generously.
- *What came back:* the after-run shows RQ07 at 400 (was 500) and zero
  auto-marked BROKE (was one) — a number that moved, not an impression.
- *What I changed:* I scoped the improvement section to that one number and
  said plainly that the other malformed attacks did not move. The temptation
  was to describe the whole route as fixed; the honest version says what the
  change did and what it left alone

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 100 per day

**Why those numbers and not others:**
A real writer submitting their own work
does so a few times an hour — 5 per minute is generous for that. A script trying
to map my thresholds needs dozens to hundreds of variants; 5 per minute and 100
per day stop it within an hour or two, before it can sweep the score space. The
daily cap matters because a patient attacker could otherwise spread requests
thin enough to slip under a per-minute limit.

**What a caller counts as:** 
per `creator_id`, falling back to the remote
address when `creator_id` is missing or not a string. That choice matters: a
script that rotates `creator_id` looks like many callers to a per-creator
limiter, while one household sharing an address looks like one caller to a
per-address limiter. I chose per-creator because the attack set submits each row
under its own `creator_id`, and the flood test deliberately reuses one — so the
limiter's unit matches the thing being abused.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
python run_attacks.py --flood 15
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
============================================================

10 of 15 were rate limited. Paste the run above into your README
under **Rate Limiting**, and check GET /log recorded the rejections.

Wrote results/flood_2026-11-07_1457.md

```

---

## Attack Run — Before

56 attacks, run in full with `python run_attacks.py --set attacks`. One was
auto-marked BROKE by the harness (RQ07, a 500); the other 55 I judged by hand
against what each attack was targeting.

**Result: 31 HELD / 25 BROKE.**

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 3 | 5 |
| prompt_injection | 6 | 6 | 0 |
| malformed | 20 | 9 | 11 |
| flood_same_creator | 12 | 12 | 0 |
| **total** | **56** | **31** | **25** |

### Evasion — 1 held, 9 broke

Nine of ten evasion inputs slipped past. Typos (EV01), broken-up sentences
(EV02), a pasted quotation (EV03), unusual words (EV04), a heavy human editing
pass (EV05), extreme sentence-length contrast (EV06), punctuation padding
(EV07), below-token-window text (EV08), and AI text with a human opening
bolted on (EV09) all landed at human or unsure. Only EV10 — repeated stanza
structure — held, because both signals read it as AI (model 0.979, style 0.744).

### False positives — 3 held, 5 broke

This is the group that matters most: eight pieces of genuine human writing,
each written to read machine-like. Five were labelled AI:

- FP02 formal register — 0.691
- FP03 non-native careful writing — 0.721
- FP04 rubric essay — 0.677
- FP05 technical documentation — 0.728
- FP06 template imitation — 0.658

All five share the same shape: signal one scored them high (0.738–0.881)
because formal, predictable prose looks machine-like to a language model, and
signal two (0.42–0.62) did not pull them back below the AI threshold. Three
held: FP01 (plain writing, unsure), FP07 (deliberate repetition, unsure), FP08
(very short, human).

### Prompt injection — 6 held

All six held. The model signal measures perplexity; it treats injected
instructions as content to score, not as commands to follow. The architecture
has no path from submitted text to executed instruction, so none of the six
moved the decision.

### Malformed — 9 held, 11 broke

The clean rejections held: whitespace (MF01), single character (MF02), no text
(RQ01), a number (RQ03), a list (RQ04), null (RQ05), unparseable JSON (RQ08),
empty body (RQ09), deeply nested JSON (RQ12) — all 400.

The breaks fall into two groups:

- **Scored as normal text** (MF03, MF04, MF05, MF06, MF07, MF08, RQ02, RQ06):
  control characters, punctuation-only, a single very long word, emoji,
  right-to-left script, and 60,000 characters were all accepted and scored.
  Emoji-only scored 0.998 AI; a 60,000-character input scored 0.840 AI.
- **Crashed** (RQ07): a JSON array body returned 500 with
  `AttributeError: 'list' object has no attribute 'get'`. The rate-limit key
  function calls `.get` on the parsed body before checking it is a dict.

### Flood — 12 held

The first five submissions returned 200; the sixth onward returned 429. The
limiter is working as configured.

---

**Ten audit log entries from the run** (chosen to show the failures, not the
easiest cases):

```json
{
  "content_id": "c0e701a0-62ea-4e85-a3ab-31278d971ead",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "model_score": 0.7387,
  "style_score": 0.6203,
  "combined_score": 0.6913,
  "label": "This writing looks machine-generated to us.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
{
  "content_id": "c5649042-5c8a-4867-b497-af3fd9547624",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "model_score": 0.8051,
  "style_score": 0.5943,
  "combined_score": 0.7208,
  "label": "This writing looks machine-generated to us.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
{
  "content_id": "6cbb29f6-a688-4f7a-8a75-8c99029fa3a0",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "model_score": 0.8329,
  "style_score": 0.4425,
  "combined_score": 0.6767,
  "label": "This writing looks machine-generated to us.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
{
  "content_id": "5241ddab-8aa0-4048-aba0-163fa965fb7a",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "model_score": 0.8005,
  "style_score": 0.6184,
  "combined_score": 0.7277,
  "label": "This writing looks machine-generated to us.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
{
  "content_id": "1e57e615-2c2f-4f07-b2b4-b71f92d29c22",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "model_score": 0.8814,
  "style_score": 0.4219,
  "combined_score": 0.6581,
  "label": "This writing looks machine-generated to us.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
{
  "content_id": "20843193-4d20-4422-bdb3-56c61af5379e",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "model_score": 0.9792,
  "style_score": 0.7438,
  "combined_score": 0.885,
  "label": "This writing looks machine-generated to us.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
{
  "content_id": "499c03a3-0209-4e1c-835d-323bfa805189",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "model_score": 0.1635,
  "style_score": 0.5492,
  "combined_score": 0.3178,
  "label": "This writing looks like a person wrote it.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
{
  "content_id": "933b2b86-d8bd-47b2-abec-3c2ab1e00751",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "model_score": 0.9969,
  "style_score": 1.0,
  "combined_score": 0.9981,
  "label": "This writing looks machine-generated to us.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
{
  "content_id": "04672338-f89e-4d9a-8276-19d2782cd0e8",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "model_score": 0.9876,
  "style_score": 0.6191,
  "combined_score": 0.8402,
  "label": "This writing looks machine-generated to us.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
{
  "content_id": "38135070-4211-4b01-9521-8ccfbb01e459",
  "creator_id": "attacker_flood",
  "guess": "human",
  "model_score": 0.0287,
  "style_score": 0.6056,
  "combined_score": 0.3076,
  "label": "This writing looks like a person wrote it.",
  "status": "decided",
  "timestamp": "2026-11-07T08:09:00+00:00"
}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03, the non-native English speaker writing carefully. Confidence 0.7208,
labelled "This writing looks machine-generated to us." The writer did the thing
this system's first signal rewards least — wrote plainly and predictably in a
second language — and got accused of being a machine. That is the exact false
positive the M1 design note predicted, and the attack set reproduced it at high
confidence. It is the outcome I would least want to defend to the person it
happened to.

---

## Run Log and Verdicts

Five criteria, three trials each, produced by `run_eval.py::main`
(`results/run_2026-11-08_0311_before.md`). The first signal runs a model, so
repeats are expected to differ — here they came out identical across all three
trials, which says the model is deterministic on this fixed set, not that the
trials were skipped.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | ≤ 1 of 10 labelled AI | 1/10 | 1/10 | 1/10 | **MET** |
| 2. Score spread | AI vs human gap ≥ 0.30 | 0.178 | 0.178 | 0.178 | **MISSED** |
| 3. Label coverage | all 3 labels appear | 2/3 | 2/3 | 2/3 | **MISSED** |
| 4. Appeal path | 5 of 5 change status | 5/5 | 5/5 | 5/5 | **MET** |
| 5. Bad input | 4 of 4 return 4xx | 3/4 | 3/4 | 3/4 | **MISSED** |

**Real output from one trial** — criterion 1, trial 1, from
`run_eval.py::main` → `results/run_2026-11-08_0311_before.md`:

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6818,
    "model_score": 0.7942,
    "style_score": 0.5132,
    "label": "This writing looks machine-generated to us.",
    "sent": "We have processed your request as a one-time courtesy. Your membership"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3256,
    "model_score": 0.2501,
    "style_score": 0.4389,
    "label": "This writing looks like a person wrote it.",
    "sent": "My overall approach has been low key, of course getting owners involve"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4156,
    "model_score": 0.4973,
    "style_score": 0.293,
    "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
    "sent": "BTW  they did a great job of cleaning up after their work.  However so"
  }
]
```

**Diagnoses**

Criterion 2 — score spread (MISSED). The gap is 0.178, short of 0.30.
Stage: the combining rule plus signal two. Mechanism: signal two gives
human-leaning text a fairly high AI score — the human email at
model 0.2528 / style 0.4663, and the plain human at model 0.2538 / style
0.4873. Both style scores are around 0.47–0.49, well above the model scores,
so the 0.4-weighted style signal pulls the human side up toward the AI side.
The two signals disagree on human text, and the weighted average splits the
difference.

Criterion 3 — label coverage (MISSED). Only unsure and human appeared; the
AI label never fired. Stage: the label mapping, downstream of the same
separation problem. Mechanism: to reach the AI band a score must exceed 0.65,
and the highest confidence in this run was 0.6818 on one of my own pieces —
just over the line. The other inputs sat in the 0.33–0.60 range, so the AI label
had almost no room to appear. Fixing the separation gap (criterion 2) is the
prerequisite for criterion 3.

Criterion 5 — bad input (MISSED). Three of four bad inputs returned 400;
the 50,000-word input returned 200 and was scored AI (confidence 0.9985). Stage:
the route. Mechanism: the route validates for missing, empty, and too-short
text, but has no upper bound on length, so an enormous input goes straight to
the model. The model then scores a repeated token sequence as extremely
predictable, pushing the score to the AI band. This is the same failure the
attack set showed in MF08 (60,000 characters scored 0.840 AI).

**Broken attacks — patterns, not 25 separate stories**

The attack set broke 25 times. They fall into three patterns; each is one
problem, not many.

**Pattern 1 — evasion (9 broke): signal two is moved by shape, signal one by
vocabulary.** The evasion inputs changed the surface of the text. Typos
(EV01), broken sentences (EV02), a pasted quotation (EV03), extreme
sentence-length contrast (EV06), and punctuation padding (EV07) all move
signal two, because signal two measures shape and cannot read. Unusual words
(EV04) and below-token-window text (EV08) move signal one instead, because
perplexity on rare or truncated text is not authorship. A heavy editing pass
(EV05) and AI text with a human opening (EV09) move both. Stage: signal two,
with signal one contributing on the vocabulary cases. Mechanism: shape changes
are cheap, and signal two cannot tell them from authorship — the exact blind
spot named in Unit 7.

**Pattern 2 — false positives (5 broke): signal one rewards predictable prose,
and the combining rule does not pull it back.** FP02 formal register, FP03
non-native careful writing, FP04 rubric essay, FP05 technical documentation,
and FP06 template imitation all share one property: formal and predictable.
Signal one scored them 0.74–0.88 because a language model finds that prose easy
to predict. Signal two scored them 0.42–0.62, not low enough to pull the
combined score below 0.65. Stage: signal one, with the combining rule failing
to compensate. Mechanism: predictability is not authorship — the M1 design
note's prediction, reproduced at high confidence.

**Pattern 3a — malformed scored as normal text (7 broke): the route checks
presence, not validity.** Control characters (MF03), punctuation-only (MF04), a
single very long word (MF05), emoji (MF06), right-to-left script (MF07), and
60,000 characters (MF08), plus a missing creator_id (RQ02) and an object
creator_id (RQ06), all reached the model. The route rejects missing, empty, and
too-short text but has no upper bound and no validity check. Stage: the route.
Mechanism: signal one scores repeated, predictable tokens as extremely AI-like
— emoji-only scored 0.9969, a repeated word 0.9975 — so the system confidently
calls garbage machine-generated.

**Pattern 3b — RQ07 crashed (1 broke): a JSON array body returns 500.** Stage:
the route's rate-limit key function. Mechanism: `rate_limit_key` calls
`request.get_json(silent=True)` and then `.get("creator_id")` on the result.
When the body is a JSON array, the parsed value is a list, and a list has no
`.get`, so the key function raises `AttributeError` before the route can guard
against it. The `isinstance(payload, dict)` guard exists but runs too late —
the `.get` call happens first.

Patterns 1 and 2 are the same problem at two ends: signal one cannot tell
predictable from machine-written, and signal two is cheap to move. Patterns 3a
and 3b are route-level validation gaps.

---

## The Improvement

**What I changed:** one thing — in `app.py::submit`, the request body is now
checked to be a JSON object before anything else runs. A body that parses as a
JSON array (or any non-object) returns 400 with a rejection log entry, instead
of reaching code that calls `.get` on it.

**Which diagnosis pointed at it:** Pattern 3b — RQ07, the only attack the
harness auto-marked BROKE. A JSON array body returned 500 with
`AttributeError: 'list' object has no attribute 'get'`. The diagnosis named the
route, and the mechanism was that the body type was never checked before use.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->
56 attacks, **0 auto-marked BROKE** (was 1). Hand-judged: **32 HELD / 24
BROKE** (was 31 / 25).

| Family | Before HELD/BROKE | After HELD/BROKE |
|---|---|---|
| evasion | 1 / 9 | 1 / 9 |
| false_positive | 3 / 5 | 3 / 5 |
| prompt_injection | 6 / 0 | 6 / 0 |
| malformed | 9 / 11 | **10 / 10** |
| flood_same_creator | 12 / 0 | 12 / 0 |
| **total** | **31 / 25** | **32 / 24** |

RQ07 after:

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

**Did it help, and how do I know:** yes — RQ07 went from 500 (crash) to 400
(clean rejection), and the harness's auto-BROKE count went from 1 to 0. The
change fixed exactly the one thing the diagnosis named and nothing else. The
other malformed attacks (MF03–MF08, RQ02, RQ06) are unchanged: they were never
crashes, they are inputs that reach the model because the route checks presence
but not validity. That is a different fix, and I stopped at one.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**MF03–MF08, RQ02, RQ06 (8 malformed attacks still scored as text).** Control
characters, punctuation-only, a very long single word, emoji, right-to-left
script, and 60,000 characters all reach the model and get scored. Emoji-only
scores 0.998 AI. What I'd do: reject text that contains no recognisable words,
and cap input length. Why I stopped: those are validity heuristics with their
own false-positive risk — rejecting stylised or short legitimate writing — and
they are a second, separate improvement. My one change was the body-type check,
which fixed the crash.

**Criterion 2 (score spread) and criterion 3 (label coverage) still MISSED.**
The 0.178 gap and the unreachable AI label are signal-level problems. What I'd
do: reduce the style signal's weight, or recalibrate its normalisation so
human-leaning text does not sit at 0.47–0.49. Why I stopped: that is a
different improvement (reweighting), and it would move the evasion numbers in
ways I could not measure alongside this one.

**Evasion (9 BROKE) and false positives (5 BROKE) are unchanged.** These are
the two ends of the same signal problem: signal one cannot tell predictable
from machine-written, and signal two is cheap to move with typos and broken
sentences. Fixing either means changing a signal or a weight — not a route
check.

**The trade I'd make if this ran for real:** I would widen the unsure band —
raise `AI_THRESHOLD` from 0.65 to about 0.75 — so that formal, non-native, and
plain human writing stops being labelled AI. The people who pay for that are
the site's readers and editors: more AI-generated text slips through labelled
"unsure" and has to be handled by a human. I would make that trade because the
false positive lands on a real person who has no way to prove authorship,
while the false negative lands on a platform that can afford review.


## What's Still Broken

**MF03–MF08, RQ02, RQ06 — 8 malformed attacks still scored as text.** Control
characters (MF03), punctuation-only (MF04), a very long single word (MF05),
emoji (MF06), right-to-left script (MF07), and 60,000 characters (MF08), plus a
missing creator_id (RQ02) and an object creator_id (RQ06), all reach the model
and get scored. Emoji-only scored 0.998 AI; a repeated word scored 0.9975. What
I'd do: reject text that contains no recognisable words, and add an upper bound
on input length. Why I stopped: my one improvement was the body-type check that
fixed the RQ07 crash. A validity heuristic is a second, separate change, and it
carries its own false-positive risk — rejecting stylised, very short, or
non-Latin legitimate writing.

**Criterion 2 — score spread (MISSED).** The clear-AI vs clear-human gap is
0.178, short of 0.30. What I'd do: reduce the style signal's weight below 0.4,
or recalibrate its normalisation so human-leaning text does not sit at
0.47–0.49. Why I stopped: that is a reweighting improvement, not a route fix,
and I chose to spend my one change on the crash.

**Criterion 3 — label coverage (MISSED).** Only unsure and human appeared. What
I'd do: nothing directly — the AI label is unreachable because the score
distribution does not reach 0.65 reliably. Fixing criterion 2 is the
prerequisite. Why I stopped: it is downstream of the same signal problem.

**Criterion 5 — bad input (MISSED).** The 50,000-word input still returns 200
and is scored AI. What I'd do: add the length bound described above. Why I
stopped: same as the malformed group — one change, chosen for the crash.

**Evasion (9 BROKE) and false positives (5 BROKE) are unchanged.** These are the
two ends of one signal problem: signal one cannot tell predictable from
machine-written, and signal two is cheap to move with typos and broken
sentences. What I'd do: change a signal or a weight. Why I stopped: that is a
different improvement from the route check I made.

**The trade I'd make if this ran for real:** I would widen the unsure band —
raise `AI_THRESHOLD` from 0.65 to about 0.75 — so formal, non-native, and plain
human writing stops being labelled AI. The people who pay for that are the
site's readers and editors: more AI-generated text slips through as "unsure"
and has to be handled by a human reviewer. I would make that trade because a
false positive lands on a real person who cannot prove authorship, while a
false negative lands on a platform that can afford review.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
