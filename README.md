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

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
