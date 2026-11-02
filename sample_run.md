# Sample Run — submissions and audit log

## Submission 1 (AI text)

    $ curl -X POST http://127.0.0.1:5000/submit \
      -H "Content-Type: application/json" \
      -d '{"text":"Effective time management is essential for professional success. First, individuals should prioritize their tasks based on urgency and importance. Additionally, it is important to set clear goals and establish a structured schedule. Furthermore, taking regular breaks can improve focus and overall productivity. By implementing these strategies, professionals can achieve a better work-life balance and enhance their performance.","creator_id":"retest_ai"}'

    {
      "confidence": 0.7939,
      "content_id": "8c6d019f-ad84-4a4d-8bc7-39767d362300",
      "guess": "unsure",
      "label": "PLACEHOLDER label (filled in at Milestone 5)",
      "model_score": 0.7939,
      "style_score": 0.0
    }

## Submission 2 (human text)

    $ curl -X POST http://127.0.0.1:5000/submit \
      -H "Content-Type: application/json" \
      -d '{"text":"Honestly I still can not believe we actually pulled that off. Remember when the printer jammed at 2am and we just sat there laughing because there was nothing else to do? That whole night was ridiculous but somehow it worked out. Anyway, let me know when you are free next week, I owe you a coffee at least.","creator_id":"retest_human"}'

    {
      "confidence": 0.6436,
      "content_id": "a47120ee-8704-4ac8-8446-a44bc3158188",
      "guess": "unsure",
      "label": "PLACEHOLDER label (filled in at Milestone 5)",
      "model_score": 0.6436,
      "style_score": 0.0
    }

## Bad input (two kinds, both 4xx)

    $ curl -i -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"creator_id":"retest_bad"}'
    HTTP/1.1 400 BAD REQUEST
    {"error": "text is required and must be non-empty"}

    $ curl -i -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text":"Ok.","creator_id":"retest_bad"}'
    HTTP/1.1 400 BAD REQUEST
    {"error": "Text is too short to score — a few sentences at least."}

## The audit log

    $ curl "http://127.0.0.1:5000/log?limit=8"

    {
      "count": 5,
      "entries": [
        {
          "combined_score": 0.8309,
          "content_id": "edc10d6a-e140-4e93-bba8-0ca2516ffcf5",
          "creator_id": "me",
          "guess": "unsure",
          "label": "PLACEHOLDER label (filled in at Milestone 5)",
          "model_score": 0.8309,
          "status": "decided",
          "style_score": 0.0,
          "timestamp": "2026-11-01T23:20:56+00:00"
        },
        {
          "combined_score": 0.7939,
          "content_id": "8c6d019f-ad84-4a4d-8bc7-39767d362300",
          "creator_id": "retest_ai",
          "guess": "unsure",
          "label": "PLACEHOLDER label (filled in at Milestone 5)",
          "model_score": 0.7939,
          "status": "decided",
          "style_score": 0.0,
          "timestamp": "2026-11-01T23:37:11+00:00"
        },
        {
          "combined_score": 0.6436,
          "content_id": "a47120ee-8704-4ac8-8446-a44bc3158188",
          "creator_id": "retest_human",
          "guess": "unsure",
          "label": "PLACEHOLDER label (filled in at Milestone 5)",
          "model_score": 0.6436,
          "status": "decided",
          "style_score": 0.0,
          "timestamp": "2026-11-01T23:37:59+00:00"
        },
        {
          "creator_id": "retest_bad",
          "event": "rejected",
          "reason": "empty_or_missing_text",
          "status": "rejected",
          "timestamp": "2026-11-01T23:38:24+00:00"
        },
        {
          "creator_id": "retest_bad",
          "event": "rejected",
          "reason": "unscoreable: Text is too short to score — a few sentences at least.",
          "status": "rejected",
          "timestamp": "2026-11-01T23:38:36+00:00"
        }
      ]
    }