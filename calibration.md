# M4 calibration — four inputs

| # | Type | model_score | style_score | confidence |
|---|---|---|---|---|
| 1 | Clear AI | 0.5832 | 0.4159 | 0.5163 |
| 2 | Clear human (onsite) | 0.2528 | 0.4663 | 0.3382 |
| 3 | Plain human (BI advice) | 0.2538 | 0.4873 | 0.3472 |
| 4 | Lightly-edited AI | 0.5382 | 0.4180 | 0.4901 |

## Findings

- `style_score` now varies (0.42–0.49); the second signal is active.
- `confidence` differs from `model_score`; the 0.6/0.4 combining rule is live.
- Clear-AI vs clear-human confidence gap: **0.178**, below the M2 criterion 2
  target of 0.30. Recorded honestly; Unit 8 diagnoses and fixes.
- The style signal gives both human inputs a fairly high AI-leaning score
  (0.47–0.49), which shrinks the gap. The `style_signal` normalisation
  constants need recalibrating in Unit 8.
- No signal split above the 0.4 disagreement threshold in these four inputs;
  the pull-toward-0.5 rule did not fire.