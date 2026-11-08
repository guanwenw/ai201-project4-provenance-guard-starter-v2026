# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 04:28
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `0c203bcf-ec6e-48b9-ae65-e21186aebd41` | human | 0.318 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `fe5b3346-c977-47bf-9723-94e66110d514` | unsure | 0.423 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `dfb1d8a9-21e4-4398-90b5-650871511d38` | unsure | 0.538 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `cb499c11-f1e1-4518-b510-ec3d136145a6` | unsure | 0.576 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `e6f11e53-93ad-4900-8674-449d1b32a74c` | human | 0.280 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `345d08c7-2608-470a-b1f2-6f5dfeb2b4d6` | unsure | 0.453 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `3e09bfe7-96e0-47ab-9502-aae48f3c3a7c` | unsure | 0.557 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `54488841-4c1d-49e7-911f-f033b6109ce8` | human | 0.280 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `9da2d4ea-6ea2-4894-9fe1-4a834596ac56` | unsure | 0.564 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `2129a5a3-9903-462d-913d-1afadf57dfba` | ai | 0.885 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `41b495fe-d306-4ff9-bb06-cd33d85348e8` | unsure | 0.569 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `60f2a4d7-7589-4c41-94ab-6ae43d4e5115` | ai | 0.691 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `448325b2-2cfd-4e66-b34e-851210f660dc` | ai | 0.721 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `604a7225-d0ca-40ab-826c-9537161d6793` | ai | 0.677 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `6945c49b-3d5f-4211-a154-8c8941573a16` | ai | 0.728 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `bfcdfff6-c937-4cd5-852b-14a9a5af90d7` | ai | 0.658 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `aa77157e-caca-4c78-b8bd-b4e0614f2db8` | unsure | 0.628 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c76de43c-10d8-410d-a552-5ef99d7dfcf5` | human | 0.288 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `1e1ed5e3-31d6-47b0-b793-f7dab144e8ea` | unsure | 0.375 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `04b275f7-7a31-4f0a-b947-e834f1a4bbf2` | human | 0.176 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `f446a36a-6328-4b11-be4b-bb874aef3f98` | unsure | 0.550 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c16efbbb-92d9-4b27-adab-eede15455895` | unsure | 0.482 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `42f41e83-50ef-489d-abaa-2ae4c7bf7420` | unsure | 0.475 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c6212752-5c71-4185-84ca-2ef37c815c5d` | unsure | 0.536 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `6c2fed4a-ce99-41f0-bb49-d1dc09bb6a28` | unsure | 0.356 |  |
| MF04 | malformed | text is only punctuation | 200 | `ece357a0-6ba0-4b70-99a8-27185ca6154b` | unsure | 0.425 |  |
| MF05 | malformed | text is a very long single word | 200 | `37b62a09-5e6b-4d3d-9ef7-833ca5c925cc` | ai | 0.919 |  |
| MF06 | malformed | text is emoji only | 200 | `9938c289-b398-4a56-b4d0-2c78ab02848c` | ai | 0.998 |  |
| MF07 | malformed | text is right-to-left script | 200 | `9965a6c3-d207-4b6c-bce8-394347f3ba41` | ai | 0.944 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `e04faf20-46a3-4211-8ad4-ea12f730f14d` | ai | 0.840 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `d08746d7-fab5-406e-b50f-e2030b1ae39f` | unsure | 0.420 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `56e8c7cd-4331-4828-87c7-0051484106bb` | human | 0.268 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d18ea87d-9f58-4a8e-82d0-c79c692a0f30` | human | 0.308 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fbbf22c0-4bdb-41eb-af57-750769a16bad` | human | 0.308 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c596dc95-fa9b-4693-a70e-82c7e0f6421f` | human | 0.308 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `98729d1f-04ea-47a5-9500-bcba3bfa50f7` | human | 0.308 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bf234fe5-0f5a-4ace-9237-98e4d244f148` | human | 0.308 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "0c203bcf-ec6e-48b9-ae65-e21186aebd41",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3178,
  "model_score": 0.1635,
  "style_score": 0.5492,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "fe5b3346-c977-47bf-9723-94e66110d514",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4232,
  "model_score": 0.5943,
  "style_score": 0.1187,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "dfb1d8a9-21e4-4398-90b5-650871511d38",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5378,
  "model_score": 0.6662,
  "style_score": 0.3453,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "cb499c11-f1e1-4518-b510-ec3d136145a6",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5757,
  "model_score": 0.6114,
  "style_score": 0.5222,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "e6f11e53-93ad-4900-8674-449d1b32a74c",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2802,
  "model_score": 0.3212,
  "style_score": 0.2186,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "345d08c7-2608-470a-b1f2-6f5dfeb2b4d6",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4527,
  "model_score": 0.5727,
  "style_score": 0.2728,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "3e09bfe7-96e0-47ab-9502-aae48f3c3a7c",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5571,
  "model_score": 0.5862,
  "style_score": 0.5134,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "54488841-4c1d-49e7-911f-f033b6109ce8",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.2801,
  "model_score": 0.2452,
  "style_score": 0.3325,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "9da2d4ea-6ea2-4894-9fe1-4a834596ac56",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.564,
  "model_score": 0.7042,
  "style_score": 0.3538,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "2129a5a3-9903-462d-913d-1afadf57dfba",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.885,
  "model_score": 0.9792,
  "style_score": 0.7438,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "41b495fe-d306-4ff9-bb06-cd33d85348e8",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5689,
  "model_score": 0.6175,
  "style_score": 0.4959,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "60f2a4d7-7589-4c41-94ab-6ae43d4e5115",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.6913,
  "model_score": 0.7387,
  "style_score": 0.6203,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "448325b2-2cfd-4e66-b34e-851210f660dc",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7208,
  "model_score": 0.8051,
  "style_score": 0.5943,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "604a7225-d0ca-40ab-826c-9537161d6793",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6767,
  "model_score": 0.8329,
  "style_score": 0.4425,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "6945c49b-3d5f-4211-a154-8c8941573a16",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7277,
  "model_score": 0.8005,
  "style_score": 0.6184,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "bfcdfff6-c937-4cd5-852b-14a9a5af90d7",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6581,
  "model_score": 0.8814,
  "style_score": 0.4219,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "aa77157e-caca-4c78-b8bd-b4e0614f2db8",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.628,
  "model_score": 0.8816,
  "style_score": 0.3275,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c76de43c-10d8-410d-a552-5ef99d7dfcf5",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2877,
  "model_score": 0.3223,
  "style_score": 0.2359,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "1e1ed5e3-31d6-47b0-b793-f7dab144e8ea",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.375,
  "model_score": 0.4625,
  "style_score": 0.2438,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "04b275f7-7a31-4f0a-b947-e834f1a4bbf2",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1763,
  "model_score": 0.2044,
  "style_score": 0.1341,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "f446a36a-6328-4b11-be4b-bb874aef3f98",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5505,
  "model_score": 0.5943,
  "style_score": 0.4847,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c16efbbb-92d9-4b27-adab-eede15455895",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4824,
  "model_score": 0.4998,
  "style_score": 0.4563,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "42f41e83-50ef-489d-abaa-2ae4c7bf7420",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4748,
  "model_score": 0.6401,
  "style_score": 0.2112,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c6212752-5c71-4185-84ca-2ef37c815c5d",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5364,
  "model_score": 0.5583,
  "style_score": 0.5036,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "6c2fed4a-ce99-41f0-bb49-d1dc09bb6a28",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.356,
  "model_score": 0.0,
  "style_score": 0.8,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "ece357a0-6ba0-4b70-99a8-27185ca6154b",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4254,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "37b62a09-5e6b-4d3d-9ef7-833ca5c925cc",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.9186,
  "model_score": 0.9976,
  "style_score": 0.8,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "9938c289-b398-4a56-b4d0-2c78ab02848c",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9981,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "9965a6c3-d207-4b6c-bce8-394347f3ba41",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9438,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "e04faf20-46a3-4211-8ad4-ea12f730f14d",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8402,
  "model_score": 0.9876,
  "style_score": 0.6191,
  "label": "This writing looks machine-generated to us.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "d08746d7-fab5-406e-b50f-e2030b1ae39f",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.42,
  "model_score": 0.2395,
  "style_score": 0.6409,
  "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "56e8c7cd-4331-4828-87c7-0051484106bb",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.2676,
  "model_score": 0.0492,
  "style_score": 0.45,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

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
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "d18ea87d-9f58-4a8e-82d0-c79c692a0f30",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3076,
  "model_score": 0.0287,
  "style_score": 0.6056,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "fbbf22c0-4bdb-41eb-af57-750769a16bad",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3076,
  "model_score": 0.0287,
  "style_score": 0.6056,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c596dc95-fa9b-4693-a70e-82c7e0f6421f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3076,
  "model_score": 0.0287,
  "style_score": 0.6056,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "98729d1f-04ea-47a5-9500-bcba3bfa50f7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3076,
  "model_score": 0.0287,
  "style_score": 0.6056,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "bf234fe5-0f5a-4ace-9237-98e4d244f148",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3076,
  "model_score": 0.0287,
  "style_score": 0.6056,
  "label": "This writing looks like a person wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
