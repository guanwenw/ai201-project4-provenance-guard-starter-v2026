# Milestone 1 — Trace a submission before building one

Written before any code. Four outputs: the submission path, the two signals
with their blind spots, a false-positive walkthrough, and the two endpoint
contracts. These feed M2 (criteria), M3 (submit), M4 (scoring), M5 (labels +
appeal), and the README.

---

## 1. The path a submission takes

From arriving to the label a reader sees. Each step names what it adds.

1. **HTTP POST `/submit` arrives** with JSON `{text, creator_id}`.
   → `app.py::submit` receives raw input.
2. **Input validation.** Check `text` is present, non-empty, and not so short
   it can't be scored.
   → rejects bad input *before* spending ~1s on the model; rejections go to
   `audit.log_rejection`, not silently dropped.
3. **Generate `content_id`** (`uuid` — `app.py` already imports it).
   → an identity `/appeal` can reference later. A submission without one
   cannot be appealed.
4. **Signal one: `detector.model_signal(text)`**
   → reads the text for **meaning** (predictability). Returns 0–1, higher = more AI.
   → mechanism: local `gpt2` perplexity, logistic-squashed at midpoint 45,
   steepness 1.6 (`detector.py`).
5. **Signal two: `stylometry.style_signal(text)`**
   → measures the text **as text** (shape, not meaning). Returns 0–1, higher = more AI.
   → combines `sentence_length_spread`, `type_token_ratio`, `punctuation_density`.
6. **Combine: `scoring.combine_signals(model_score, style_score)`**
   → one confidence, 0–1.
7. **Label: `scoring.score_to_label(score)` → `(guess, label_text)`**
   → turns the number into a sentence a non-technical reader sees.
8. **Log: `audit.log_decision(content_id, creator_id, guess, model_score,
   style_score, combined_score, label, status="decided")`**
   → appends one JSON line to `logs/audit.jsonl` (append-only).
9. **Respond JSON** `{content_id, guess, confidence, label, model_score,
   style_score}`.
   → ⚠️ `model_score` and `style_score` must be in the response: unit 8's
   `run_attacks.py` and `run_eval.py` read them straight off it.

---

## 2. The two signals, and what each cannot see

### Signal one — `detector.py::model_signal`

**What it measures:** how *predictable* the text is to a language model
(perplexity). Low perplexity ("I could have guessed this") → high AI score.
Score direction: **higher = more likely AI**.

**Why that might differ between human and AI writing:** a model writes by
picking the likely next word repeatedly, so model-written text tends to be
text a model finds easy to predict. Human writing wanders — odd word choices,
abrupt turns.

**What it can't see (the blind spot):**
- **Predictability ≠ authorship.** What it actually rewards is *common words
  in short, ordinary sentences*. A second-language writer sticking to safe
  vocabulary, a younger writer, anyone writing plainly on purpose — all score
  about as machine-like as machine writing.
- **The reverse also trips:** dense, ornate prose full of rare words often
  scores as *human*, because rare words are exactly what a model fails to
  predict. Formal ≠ AI.
- So the writers most likely to be accused are the ones with the **least room
  to argue back**. This is structural, not a bug.

### Signal two — `stylometry.py::style_signal`

**What it measures:** the *shape* of the text — sentence-length spread
(stdev / mean), word variety (type-token ratio), punctuation density. No
reading of meaning. Score direction after normalisation: **higher = more
likely AI**.

**Why that might differ between human and AI writing:** generated prose tends
toward even, mid-length sentences and a narrower vocabulary band; human
writing is lumpier — a three-word sentence next to a forty-word one.

**What it can't see (the blind spot):**
- **It cannot read.** It has no idea what the text says. Anything that changes
  the shape without changing the substance moves it — typos, broken-up
  sentences, a pasted quotation. **Very cheap to do on purpose**, and unit 8's
  attack set will do exactly that.
- Short text: `statistics.stdev` raises on fewer than two sentences, and TTR
  drifts down as text grows, so length alone can look like a signal.

---

## 3. Following the false positive

The scenario that sets every threshold downstream. A real writer submits
their own work; the system calls it AI.

> **Worked example — illustrative numbers, not a measurement.** The scores
> below are a design trace, not output from a real run. Actual scores get
> filled in during M4's calibration runs, and the label wording gets checked
> against the real text in M5.
Scenario: a second-language English writer submits their own poem.
Plain vocabulary, short ordinary sentences — exactly what signal one rewards.

    What score did they get?
    Signal one returns high (gpt2 finds plain prose very predictable), e.g. 0.82.
    Signal two, if their sentences are uniform, also scores AI-ish, e.g. 0.70.
    Combined ≈ 0.76 → above AI_THRESHOLD (0.65 in config.py) → "ai".

    What did the label say?
    The high-confidence-AI label (written in M5). It accuses them outright.

    What can they do?
    POST /appeal with content_id + reasoning. audit.log_appeal moves status to
    "under_review"; the original decision stays in the log (append-only). No
    automatic re-check.

This is the person M2's false-positive target and M4's weighting exist for.
Weighting toward the signal that reads more human means fewer false
accusations — and more AI text getting through. No weighting avoids the trade.

> **Revisit in M5:** confirm the actual high-confidence-AI label still reads as
> an accusation in this scenario. If the final wording turns out more neutral,
> update this trace to match.

---

## 4. The two endpoint contracts

Written before coding. Field names, types, required-ness, and bad-input
behaviour all decided here so M3/M5 can build against it without asking.

### `POST /submit`

**Input (JSON):**
| field | type | required | notes |
|---|---|---|---|
| `text` | string | yes | non-empty |
| `creator_id` | string | yes | who submitted |

**Output (JSON):**
| field | type | notes |
|---|---|---|
| `content_id` | string | uuid; `/appeal` needs it |
| `guess` | string | `"ai"` / `"human"` / `"unsure"` |
| `confidence` | number | 0.0–1.0 |
| `label` | string | full reader-facing sentence |
| `model_score` | number | 0.0–1.0 — **required**, unit 8 reads it |
| `style_score` | number | 0.0–1.0 — **required**, unit 8 reads it |

**Bad input:**
- `text` missing or empty → `400` with an error body; logged via
  `audit.log_rejection`.
- `text` too short to score (under 3 tokens) → `400`; logged via
  `audit.log_rejection`.
- `text` enormous → handled in M3: reject with `400` or truncate + flag.
  (Write the choice here once made.)

### `POST /appeal`

**Input (JSON):**
| field | type | required | notes |
|---|---|---|---|
| `content_id` | string | yes | must exist in the log |
| `reasoning` | string | yes | the writer's explanation |

**Output (JSON):** confirmation + status now `"under_review"`.

**Bad input:**
- unknown `content_id` → `404`. **Must not fail silently** — a typo here is
  the #1 way M5 eats an hour (per `app.py` docstring).

---

## Notes carried forward

- The path (step 1) becomes README **What This Does**.
- The blind spots (step 2) become README **Signals and Scoring**.
- The false-positive walkthrough (step 3) sets M2's false-positive target and
  M4's combining rule.
- The contracts (step 4) are what M3 and M5 build against.
- `scoring.py::combine_signals` is the file and function the README must name.