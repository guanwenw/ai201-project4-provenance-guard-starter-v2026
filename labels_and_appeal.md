# M5 labels and appeal

Three labels wired into scoring.score_to_label:

- high-confidence human (0.00–0.35): "This writing looks like a person wrote it."
- unsure (0.35–0.65): "We can't tell whether a person or a machine wrote this, so we're not labelling it either way."
- high-confidence AI (0.65–1.00): "This writing looks machine-generated to us."

## Reachability (verified)

- **high-confidence AI:** reachable — content_id 1869d96c-..., confidence
  0.7418 (model 0.8309, style 0.6082), guess "ai".
- **unsure:** reachable — content_id c0ef60b2-..., confidence 0.3673.
- **high-confidence human:** NOT produced by the tested inputs. An ornate,
  rare-word paragraph scored model 0.3641 but style 0.5063, combining to
  0.421 — above the 0.35 human threshold. The style signal keeps human-leaning
  text out of the human band. Recorded for Unit 8; not fixed by lowering
  thresholds.

## Appeal path

POST /appeal on a real content_id returns 200, status "under_review", writes an
appeal entry beside the original decision (append-only). Unknown content_id
returns 404.