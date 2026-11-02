# M5 Sample Run — submission, appeal, and audit log

## A submission

    $ curl -X POST http://127.0.0.1:5000/submit \
      -H "Content-Type: application/json" \
      -d '{"text":"Remote work has reshaped how teams communicate. Managers must establish clear expectations around availability and response times. Regular check-ins help maintain alignment without creating unnecessary meetings. Teams that document decisions well tend to coordinate more smoothly across time zones.","creator_id":"m5_reviewer"}'

    {
      "confidence": 0.3673,
      "content_id": "c0ef60b2-cbe8-4cce-986e-86889a70121f",
      "guess": "unsure",
      "label": "We can't tell whether a person or a machine wrote this, so we're not labelling it either way.",
      "model_score": 0.2868,
      "style_score": 0.4881
    }

## An appeal

    $ curl -X POST http://127.0.0.1:5000/appeal \
      -H "Content-Type: application/json" \
      -d '{"content_id":"c0ef60b2-cbe8-4cce-986e-86889a70121f","reasoning":"This paragraph is from a report I drafted for work last month. I can send the original document if needed."}'

    {
      "content_id": "c0ef60b2-cbe8-4cce-986e-86889a70121f",
      "message": "Appeal received. A person will review this decision and follow up.",
      "ok": true,
      "status": "under_review"
    }

## What the log shows afterwards

    $ curl "http://127.0.0.1:5000/log?limit=6"

    {
      "count": 6,
      "entries": [
        {
          "combined_score": 0.3673,
          "content_id": "799e1e24-96d5-42d4-81be-0388c1992f73",
          "creator_id": "m5_reviewer",
          "guess": "unsure",
          "label": "We're not sure who wrote this. It could be either, so we're not making a call either way.",
          "model_score": 0.2868,
          "status": "decided",
          "style_score": 0.4881,
          "timestamp": "2026-11-02T02:10:40+00:00"
        },
        {
          "content_id": "799e1e24-96d5-42d4-81be-0388c1992f73",
          "creator_id": "m5_reviewer",
          "event": "appeal",
          "reasoning": "This paragraph is from a report I drafted for work last month. I can send the original document if needed.",
          "status": "under_review",
          "timestamp": "2026-11-02T02:10:57+00:00"
        },
        {
          "combined_score": 0.421,
          "content_id": "918d3cd2-dd9e-49be-90b5-6aa1a21b3d6f",
          "creator_id": "m5_human_try",
          "guess": "unsure",
          "label": "We're not sure who wrote this. It could be either, so we're not making a call either way.",
          "model_score": 0.3641,
          "status": "decided",
          "style_score": 0.5063,
          "timestamp": "2026-11-02T02:12:27+00:00"
        },
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

The original decision for c0ef60b2-... is still there, and the appeal sits after
it with status "under_review". The log is append-only: the original was not
overwritten. Earlier entries still carry the old label wording, which shows the
log records exactly what was shown at the time.

## Unknown content_id returns 404

    $ curl -i -X POST http://127.0.0.1:5000/appeal \
      -H "Content-Type: application/json" \
      -d '{"content_id":"no-such-id-12345","reasoning":"testing the error path"}'

    HTTP/1.1 404 NOT FOUND
    {"error": "unknown content_id"}