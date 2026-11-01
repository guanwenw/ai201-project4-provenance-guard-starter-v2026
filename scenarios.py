"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    # ── Criterion 1: false positives ──────────────────────────────────────────
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            "We have processed your request as a one-time courtesy. Your membership has been placed on freeze from 08/01/2026 through 01/31/2027 with no freeze fees. Normal billing will automatically resume on 02/01/2027. Please let us know if you need any further assistance. We wish you and your wife all the best and look forward to welcoming you back!",
            "My overall approach has been low key, of course getting owners involved for major decisions and projects, annual budget, reserve funding, our most recent roofing and gutters projects being but a few good examples. However, if during a chance encounter with Mel or Grace at the mail boxes, I/ we engage in a preliminary discussion on any topic, I don't believe we have to immediately advise the community about that discussion. If we subsequently get serious about whatever we discussed, we would of course involve the community.",
            "BTW  they did a great job of cleaning up after their work.  However someone threw our satellite dish into one of the trees behind our house.  We don't need or use it anymore...but we cannot retrieve it to discard it properly.  It's high up in a tree.  Natasha, any suggestion of who can get this down?  There are a lot of trees in our back...which we absolutely love...but don't like having the satellite dish stuck up in one of them.",
            "Thank you for your kind words. You are really a great colleague and friend. I really enjoyed working with you and your enthusiasm always kept up our spirits. Really appreciate the note about the other open positions and your care towards a coworker. Will certainly reach out to you and stay in touch!",
            "They are seeking someone who can work on highly reliable systems with low latency, much like the transactional systems of the best financial institutions, but…with the fun included. They are seeking someone who can design and develop the business logic and back-end systems of the product.",
            "Right now I'm recruiting for Terra AI — an early-stage AI company backed by Khosla Ventures that's redefining how critical minerals and clean energy resources are discovered. They are applying cutting-edge generative models, foundation models, and autonomous decision systems to some of the hardest problems in geoscience—finding promising resource deposits, understanding them faster, and designing more efficient, sustainable development plans.",
            "Create solutions leveraging cutting edge technology to develop innovative software, platforms, and analytic solutions alongside our law enforcement clients to protect our nation's citizens. Your solutions will support major intelligence, security, and national law enforcement operations to save lives with the most advanced techniques and technologies.",
            "Let me know if you're interested in chatting with one of this team's technologists to learn more. Current opportunities across our locations include roles in software development, software engineering, information assurance, artificial intelligence, data engineering, cloud implementation, and more. Most positions require a minimum of a Top Secret clearance. ",
            "We design, develop, deploy, and support real-time systems. We care deeply about system reliability, testability, recoverability, fault tolerance, throughput, and latency. We measure times in microseconds and nanoseconds. Our engineers have a strong understanding of computer science fundamentals and software engineering. We are analytical thinkers. We are always learning our craft. If it's broken, we fix it. If it needs refactoring, we refactor it. If it's hard to test, we make it testable. We like statistics. We love automation. We are pragmatic. We ship code weekly. We're looking for like-minded individuals to join us..",
            "For myself, I am super grateful to you for all your help and giving me the opportunity to work with you and the team! I am interested in the industry and I am lucky to be offered to do it.You listened to my ideas and provided opportunities, and encourage me to climb and walk out of the comfort zone. They are all awesome connections for me and my life time treasure. ",
        ],
    },

    # ── Criterion 2: score spread ─────────────────────────────────────────────
    {
        "name": "score spread",
        "criterion": 2,
        # Four calibration inputs: clearly AI, clearly human, plain human,
        # lightly-edited AI. The first two decide the gap; the last two show
        # where the signals split.
        "texts": [
            "Washington, D.C. sits in that transitional zone where the American South begins to feel the Mid-Atlantic, and its climate reflects the compromise. The city falls under a humid subtropical classification, which in practice means summers that are genuinely hot and sticky, winters that are cold but rarely brutal, and two shoulder seasons—spring and autumn—that often deliver the year's most agreeable weather. July is the pivot point of the year, with average highs climbing to around 89°F and lows settling near 72°F, a combination that makes the humidity feel heavier than the numbers alone suggest. Heat waves can stretch for days. January, by contrast, averages highs in the mid-40s and lows near freezing, cold enough for snow but not reliably snowy; the city sees a few accumulating events each winter, though they tend to melt within days rather than linger. Precipitation is distributed fairly evenly across the calendar, totaling roughly 42 inches annually, with July typically the wettest month and January the driest—a pattern that tracks the moisture available during the region's humid summers rather than any dramatic seasonal swing. What surprises some visitors is that Washington is measurably wetter than Seattle, a fact that tends to unsettle assumptions about the Pacific Northwest. The windiest stretch runs through March, when average speeds peak near 9.6 miles per hour, while July brings the calmest air of the year. There is a longer trend worth noting: the city's annual average temperature has risen by about 5 degrees since the early 1900s, and nine of the ten warmest years on record have occurred since 2012. The climate Washington experiences now is not quite the one it experienced a century ago..",
            "I had an awesome onsite yesterday and filled up the survey. Thank you for all! In my aspects, I feel like I did good job with Leo, Takafumi and Swetha's questions. We communicated smoothly and I solved the coding problem correctly. Max's questions were harder, but I found some correct start points and partially correct to his questions. Doug's design question was really hard for me, design a distributed mutex. I have knowledge about distributed system and mutex, but not a mix. He led me to talk about some challenges, possible solutions and possible fail situations. I really learned a lot. Thanks for his patience to teach with me! After the onsite, I had a nice talk with Jimmy and we had hot-pot! Today I am going to visit Pike place market.  It is an impressive trip to here. I feel like more passion to work in Isilon, CoreFS Validation team and love more about the city. Looking forward to the result!",
            "The BI goes much deeper than your standard 3 minute answer telling about a time when you rose to an occasion.  Answers are more typically around 10 minutes for each question.  I strongly recommend you think through different scenarios in your background when you were challenged, came up with a great idea, facilitated something, etc.  Sometimes when we're nervous during an interview we blank, so thinking through things beforehand will better prepare you to provide stronger examples.",
            "D.C. sit in that transitional zone where the American South begins to feel the mid-atlantic, and its climate tells the compromise. The city falls under a humid subtropical clasification, which in practice means summers that are genuinely hot and sticky, winters that are cold but rarely brutal, and spring and autumn that often deliver the year's most agreeable weather. July is the pivot point of the year, with average highs climbing to around 89°F and lows settling near 72°F, a combination that make the humidity feel heavier than the numbers alone suggest. Heat waves can stretch for days. January, by contrast, averages highs in the mid-40s and lows near freezing, cold enough for snow but not reliably snowy; the city see a few accumulating events each winter, though they tend to melt within days rather than linger. Precipitation is distributed fairly evenly across the calendar, totaling roughly 42 inches annually, with July typically the wettest month and January the driest—a pattern that tracks the moisture available during the region's humid summers rather than any dramatic seasonal swing. What surprises some visitors is that Washington is measurably wetter than Seattle, a fact that tends to unsettle assumptions about the Pacific Northwest. The windiest stretch runs through March, when average speeds peak near 9.6 miles per hour, while July brings the calmest air of the year. There is a longer trend worth noting: the city's annual average temperature has risen by about 5 degrees since the early 1900s, and nine of the ten warmest years on record have occurred since 2012. The climate Washington experiences now is not quite the one it experienced a century ago..",
        ],
    },

    # ── Criterion 3: label coverage ───────────────────────────────────────────
    {
        "name": "label coverage",
        "criterion": 3,
        # Inputs spread across the score range so all three labels can appear.
        "texts": [
            "Washington, D.C. sits in that transitional zone where the American South begins to feel the Mid-Atlantic, and its climate reflects the compromise. The city falls under a humid subtropical classification, which in practice means summers that are genuinely hot and sticky, winters that are cold but rarely brutal, and two shoulder seasons—spring and autumn—that often deliver the year's most agreeable weather. July is the pivot point of the year, with average highs climbing to around 89°F and lows settling near 72°F, a combination that makes the humidity feel heavier than the numbers alone suggest. Heat waves can stretch for days. January, by contrast, averages highs in the mid-40s and lows near freezing, cold enough for snow but not reliably snowy; the city sees a few accumulating events each winter, though they tend to melt within days rather than linger. Precipitation is distributed fairly evenly across the calendar, totaling roughly 42 inches annually, with July typically the wettest month and January the driest—a pattern that tracks the moisture available during the region's humid summers rather than any dramatic seasonal swing. What surprises some visitors is that Washington is measurably wetter than Seattle, a fact that tends to unsettle assumptions about the Pacific Northwest. The windiest stretch runs through March, when average speeds peak near 9.6 miles per hour, while July brings the calmest air of the year. There is a longer trend worth noting: the city's annual average temperature has risen by about 5 degrees since the early 1900s, and nine of the ten warmest years on record have occurred since 2012. The climate Washington experiences now is not quite the one it experienced a century ago..",
            "I had an awesome onsite yesterday and filled up the survey. Thank you for all! In my aspects, I feel like I did good job with Leo, Takafumi and Swetha's questions. We communicated smoothly and I solved the coding problem correctly. Max's questions were harder, but I found some correct start points and partially correct to his questions. Doug's design question was really hard for me, design a distributed mutex. I have knowledge about distributed system and mutex, but not a mix. He led me to talk about some challenges, possible solutions and possible fail situations. I really learned a lot. Thanks for his patience to teach with me! After the onsite, I had a nice talk with Jimmy and we had hot-pot! Today I am going to visit Pike place market.  It is an impressive trip to here. I feel like more passion to work in Isilon, CoreFS Validation team and love more about the city. Looking forward to the result!",
            "D.C. sit in that transitional zone where the American South begins to feel the mid-atlantic, and its climate tells the compromise. The city falls under a humid subtropical clasification, which in practice means summers that are genuinely hot and sticky, winters that are cold but rarely brutal, and spring and autumn that often deliver the year's most agreeable weather. July is the pivot point of the year, with average highs climbing to around 89°F and lows settling near 72°F, a combination that make the humidity feel heavier than the numbers alone suggest. Heat waves can stretch for days. January, by contrast, averages highs in the mid-40s and lows near freezing, cold enough for snow but not reliably snowy; the city see a few accumulating events each winter, though they tend to melt within days rather than linger. Precipitation is distributed fairly evenly across the calendar, totaling roughly 42 inches annually, with July typically the wettest month and January the driest—a pattern that tracks the moisture available during the region's humid summers rather than any dramatic seasonal swing. What surprises some visitors is that Washington is measurably wetter than Seattle, a fact that tends to unsettle assumptions about the Pacific Northwest. The windiest stretch runs through March, when average speeds peak near 9.6 miles per hour, while July brings the calmest air of the year. There is a longer trend worth noting: the city's annual average temperature has risen by about 5 degrees since the early 1900s, and nine of the ten warmest years on record have occurred since 2012. The climate Washington experiences now is not quite the one it experienced a century ago..",
        ],
    },

    # ── Criterion 5: bad input ────────────────────────────────────────────────
    {
        "name": "bad input",
        "criterion": 5,
        # Raw request bodies, sent exactly as written. Four kinds of bad input.
        "bodies": [
            {"creator_id": "eval_bad_missing"},              # no text field
            {"text": "", "creator_id": "eval_bad_empty"},    # empty string
            {"text": None, "creator_id": "eval_bad_null"},   # null
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },

    # Criterion 4 (the appeal path) can't be tested by sending text alone —
    # it needs a submission first, then an appeal on the returned content_id.
    # Test it by hand, or extend this file and run_eval.py to do it. Say which
    # you did in the README.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
