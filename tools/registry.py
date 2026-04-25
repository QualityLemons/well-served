from importlib import import_module


TOOL_CATALOG = {
    'conversation-cafe': {
        'class': 'tools.implementations.ConversationCafeTool',
        'form_class': 'tools.forms.ConversationCafeForm',
        'title': 'Conversation Café',
        'icon': 'comments',
        'category': 'Facilitation',
        'what': (
            'Structure calm, profound group dialogue around a confusing or challenging theme. '
            'Four rounds with a talking object create space for genuine listening '
            'and collective sense-making without debate.'
        ),
        'how': (
            'State the theme as an open question. Read the six Conversation Café agreements. '
            'Round 1 — talking object: each person shares thoughts, feelings, or actions (1 min per person). '
            'Round 2 — talking object: each person shares what shifted after listening (1 min per person). '
            'Round 3 — open conversation (20–40 min). '
            'Round 4 — talking object: each member shares their takeaway (5–10 min).'
        ),
        'why': (
            'Lay the ground for new strategies to emerge from confusion or shock. '
            'The talking object disciplines listening; the four-round structure '
            'prevents premature closure and lets meaning surface at its own pace.'
        ),
        'example_input': {
            'theme': 'How do we stay connected and purposeful when everything around us keeps changing?',
            'round_one': (
                'I am feeling fatigued by the pace of change and quietly disengaged. '
                'I keep doing the work but I have stopped believing the strategy.'
            ),
            'round_two': (
                'Hearing others name the same fatigue made me feel less isolated. '
                'I had assumed I was the only one struggling — I was wrong.'
            ),
            'open_conversation': (
                'The group kept returning to purpose. Not strategy, not process — purpose. '
                'Several people said they had stopped asking "why" because the "what" '
                'was so relentless. One person said: "We are solving problems we haven\'t '
                'named." That landed for everyone.'
            ),
            'takeaway': (
                'I am going to name this fatigue explicitly in my next team meeting '
                'rather than working around it. The conversation itself was a model '
                'for what we need more of.'
            ),
        },
        'display_fields': ['theme', 'round_one', 'round_two', 'open_conversation', 'takeaway', 'word_count'],
        'timer_seconds': 2700,
    },
    'helping-heuristics': {
        'class': 'tools.implementations.HelpingHeuristicsTool',
        'form_class': 'tools.forms.HelpingHeuristicsForm',
        'title': 'Helping Heuristics',
        'icon': 'handshake-angle',
        'category': 'Facilitation',
        'what': (
            'Explore and shift your patterns of helping, receiving help, and asking for help. '
            'Four structured rounds — each using a different coaching approach — '
            'reveal habits and open new possibilities.'
        ),
        'how': (
            'Groups of 3: client, coach, observer. '
            'Round 1 — Quiet Presence: compassionate listening only (2 min). '
            'Round 2 — Guided Discovery: inquiry for mutual discovery (2 min). '
            'Round 3 — Loving Provocation: advice, accepting and blocking (2 min). '
            'Round 4 — Process Mindfulness: accept all offers, notice novel possibilities (2 min). '
            'Debrief the impact of all four patterns (5 min). '
            'Repeat any rounds as needed. ~15 min total.'
        ),
        'why': (
            'Gain insight into your own interaction patterns and develop the '
            'ability to choose how you engage. Heuristics help people make smarter '
            'decisions quickly and develop deeper self-awareness in real time.'
        ),
        'example_input': {
            'challenge': 'I keep taking on too much and struggling to delegate meaningfully.',
            'quiet_presence': (
                'Being heard without advice or fix-it energy was unexpectedly calming. '
                'The observer noticed I visibly relaxed and became more specific as the coach stayed silent.'
            ),
            'guided_discovery': (
                'The coach\'s questions ("what does meaningful look like?") surfaced '
                'that I don\'t trust others to care as much as I do. That was new.'
            ),
            'loving_provocation': (
                'The coach said "you\'re protecting your team from growing." '
                'It landed hard. The observer noted I went quiet for a long moment.'
            ),
            'process_mindfulness': (
                'When both of us accepted all offers, the conversation became generative. '
                'We ended up designing a delegation experiment together rather than talking about the problem.'
            ),
            'debrief': (
                'Loving Provocation had the most impact but Guided Discovery was most useful. '
                'My habit is to jump to Loving Provocation too quickly. '
                'I am going to practise Quiet Presence as my default opening move.'
            ),
        },
        'display_fields': [
            'challenge',
            'quiet_presence',
            'guided_discovery',
            'loving_provocation',
            'process_mindfulness',
            'debrief',
            'word_count',
        ],
        'timer_seconds': 900,
    },
    'improv-prototyping': {
        'class': 'tools.implementations.ImprovPrototypingTool',
        'form_class': 'tools.forms.ImprovPrototypingForm',
        'title': 'Improv Prototyping',
        'icon': 'masks-theater',
        'category': 'Facilitation',
        'what': (
            'Act out a chronic challenge, identify what works and what does not, '
            'then rapidly assemble improved prototypes through repeated rounds of '
            'performance and structured observation.'
        ),
        'how': (
            'Set the stage — describe the scenario and roles (3 min). '
            'Players enact the scene (3–5 min). Observer groups debrief with '
            '1-2-4-All to find successful and unsuccessful chunks (5 min). '
            'Each group assembles a new prototype and acts it out for themselves (5 min). '
            'The strongest prototype comes on stage for the whole group (3–5 min). '
            'Repeat rounds until one or more prototypes are good enough to practise. '
            '~20 min per round.'
        ),
        'why': (
            'Enable people to act their way into new thinking. '
            'Tap explicit, tacit, and latent knowledge simultaneously. '
            'Break through frozen behaviour and create a rehearsal for real life '
            'that is far more engaging than conventional training.'
        ),
        'example_input': {
            'scenario': (
                'A nurse asks a doctor for an urgent medication clarification. '
                'The doctor is distracted, gives a vague answer, and the nurse '
                'leaves uncertain. Scene explores communication breakdown at handover.'
            ),
            'scene_observations': (
                'Unsuccessful: doctor never made eye contact; nurse did not state urgency clearly. '
                'Successful: nurse used the patient name, which got the doctor\'s attention briefly.'
            ),
            'prototype': (
                'New scene: nurse opens with "I need 30 seconds — patient name, room 4, '
                'urgent." Doctor pauses, confirms. Nurse reads back the instruction. '
                'Both confirm before separating.'
            ),
            'reflection': (
                'The read-back confirmation is what we are taking into practice. '
                'It costs under 10 seconds and eliminates ambiguity at the handover point.'
            ),
        },
        'display_fields': ['scenario', 'scene_observations', 'prototype', 'reflection', 'word_count'],
        'timer_seconds': 1200,
    },
    'min-specs': {
        'class': 'tools.implementations.MinSpecsTool',
        'form_class': 'tools.forms.MinSpecsForm',
        'title': 'Min Specs',
        'icon': 'list-check',
        'category': 'Facilitation',
        'what': (
            'Identify only the absolute must-dos and must-not-dos for achieving a purpose. '
            'Start with a complete list of rules, then ruthlessly drop anything that '
            'could be broken without losing the purpose.'
        ),
        'how': (
            'Generate the full Max Spec list alone (1 min) then in small groups (5 min). '
            'Test each rule: "If we broke this, could we still achieve our purpose?" — '
            'drop every rule that passes the test (15 min, repeat if needed). '
            'Compare across small groups and consolidate to the shortest shared list (15 min).'
        ),
        'why': (
            'Eliminate rule clutter and unlock innovation. '
            'Free people from micromanagement, focus energy where it matters, '
            'and create enabling constraints that guide scaling with fidelity.'
        ),
        'example_input': {
            'max_specs': (
                'Must-dos: communicate daily, document decisions, involve stakeholders early, '
                'get sign-off at each stage, use the approved template, '
                'hold a kick-off meeting, assign a named owner, run a retrospective. '
                'Must-not-dos: skip testing, launch without approval, ignore user feedback.'
            ),
            'sifting_result': (
                'Dropped: daily communication (weekly is enough), approved template '
                '(format doesn\'t affect outcome), kick-off meeting (can be async). '
                'Survived: named owner, involve stakeholders early, no launch without approval, '
                'no skipping testing.'
            ),
            'min_specs': (
                'Must-dos: assign a named owner; involve key stakeholders before any build begins. '
                'Must-not-dos: launch without explicit approval; skip user testing.'
            ),
        },
        'display_fields': ['max_specs', 'sifting_result', 'min_specs', 'word_count'],
        'timer_seconds': 2700,
    },
    'wise-crowds-large-group': {
        'class': 'tools.implementations.WiseCrowdsLargeGroupTool',
        'form_class': 'tools.forms.WiseCrowdsLargeGroupForm',
        'title': 'Wise Crowds (Large Group)',
        'icon': 'users-rectangle',
        'category': 'Facilitation',
        'what': (
            'Scale peer consultation to a large room. One client presents at the front; '
            'a chosen primary team consults openly; satellite groups of 5–7 critique '
            'and add their own recommendations in parallel.'
        ),
        'how': (
            'Client presents challenge (10 min). Primary consultants ask clarifying '
            'questions (10 min). Client turns back; primary team forms joint advice (7 min). '
            'Satellite teams critique and generate recommendations (10 min) while client '
            'confers with primary team. Gather one critique then one recommendation from '
            'each satellite team — no repeats (10 min). Client shares takeaway (2 min). '
            'Full-group reflection (5 min). ~1 hour total.'
        ),
        'why': (
            'Liberate wisdom across an entire organisation simultaneously. '
            'Satellite teams prevent the primary team becoming a bottleneck and '
            'ensure every voice in the room contributes to the client\'s challenge.'
        ),
        'example_input': {
            'challenge': (
                'We have launched three digital tools in the last year and adoption '
                'stalls every time. I need help diagnosing what keeps blocking us.'
            ),
            'clarifying_questions': (
                'Are the tools replacing existing workflows or adding new ones? '
                'Who owns adoption post-launch? '
                'How are frontline staff involved in the selection process?'
            ),
            'primary_advice': (
                'Frontline buy-in must happen before launch, not after. '
                'Consider a "shadow week" where implementers join a real shift '
                'before building the training plan.'
            ),
            'satellite_feedback': (
                'Team A: the primary advice overlooks manager resistance — add a '
                '"manager readiness" checklist. '
                'Team B: a staged rollout with visible quick wins builds momentum better '
                'than a big-bang launch.'
            ),
            'takeaway': (
                'The shadow week idea and the manager readiness checklist are both '
                'things I can act on immediately. Taking both away.'
            ),
            'group_reflection': (
                'The group noticed how quickly satellite teams converged on the same '
                'root cause the primary team missed. '
                'Now what: propose a 90-day adoption sprint with a named owner.'
            ),
        },
        'display_fields': [
            'challenge',
            'clarifying_questions',
            'primary_advice',
            'satellite_feedback',
            'takeaway',
            'group_reflection',
            'word_count',
        ],
        'timer_seconds': 3600,
    },
    'wise-crowds': {
        'class': 'tools.implementations.WiseCrowdsTool',
        'form_class': 'tools.forms.WiseCrowdsForm',
        'title': 'Wise Crowds',
        'icon': 'users-gear',
        'category': 'Facilitation',
        'what': (
            'Rapid peer consultation in groups of 4–5. Each person takes a turn '
            'as client: presents a challenge, receives clarifying questions, then '
            'turns their back while consultants advise freely for 8 minutes.'
        ),
        'how': (
            'Client presents their challenge and request for help (2 min). '
            'Consultants ask clarifying questions (3 min). '
            'Client turns back and takes notes while consultants discuss freely (8 min). '
            'Client turns back and shares what was useful and what they take away (2 min). '
            'Repeat for each person in the group. ~15 min per person.'
        ),
        'why': (
            'Tap the intelligence of the whole group without time-consuming presentations. '
            'Liberate wisdom across silos, build trust through mutual support, '
            'and practise listening without defending.'
        ),
        'example_input': {
            'challenge': (
                'I need help deciding whether to escalate a recurring team conflict '
                'or let the team resolve it themselves. I keep going back and forth.'
            ),
            'clarifying_questions': (
                'How long has this been going on? '
                'Have you spoken to both parties separately? '
                'What outcome are you hoping for?'
            ),
            'consultant_advice': (
                'The group suggested I set a clear timeline: give the team two weeks '
                'to resolve it, then step in. They also recommended naming the pattern '
                'openly rather than managing around it.'
            ),
            'takeaway': (
                'The idea of naming the pattern directly felt like the step I had been '
                'avoiding. That is what I am taking away.'
            ),
        },
        'display_fields': [
            'challenge',
            'clarifying_questions',
            'consultant_advice',
            'takeaway',
            'word_count',
        ],
        'timer_seconds': 900,
    },
    '25-10-crowd-sourcing': {
        'class': 'tools.implementations.TwentyFiveTenCrowdSourcingTool',
        'form_class': 'tools.forms.TwentyFiveTenCrowdSourcingForm',
        'title': '25/10 Crowd Sourcing',
        'icon': 'ranking-star',
        'category': 'Facilitation',
        'what': (
            'Generate and sift a large group\'s boldest actionable ideas in 30 minutes. '
            'Everyone writes one idea, passes cards through five scoring rounds, '
            'and the top ten surface via a countdown from 25.'
        ),
        'how': (
            'Each person writes a bold idea and first step on an index card (5 min). '
            'Mill around passing cards — no reading, just passing. When the bell rings, '
            'pair up and score the card you hold 1–5. Repeat for five rounds (15 min). '
            'Tally scores and count down from 25 to reveal the top ten ideas (5 min). '
            'Debrief: "What caught your attention?" (2 min).'
        ),
        'why': (
            'Spread innovations out and up — the crowd\'s collective wisdom sifts '
            'the boldest ideas without facilitated debate. Fast, fun, and surprisingly '
            'valid. Surprises are frequent.'
        ),
        'example_input': {
            'bold_idea': (
                'Create a 15-minute "decision sprint" at the start of every project '
                'kick-off — one decision made, owner named, deadline set.'
            ),
            'scores_received': 'Scores: 4, 3, 5, 4, 5 — total 21 out of 25.',
            'top_ideas': (
                'The highest scorer (25) was an idea for a shared "team health pulse" '
                'sent weekly to every manager. What surprised me was how many ideas '
                'focused on reducing meetings rather than improving them.'
            ),
        },
        'display_fields': ['bold_idea', 'scores_received', 'top_ideas', 'word_count'],
        'timer_seconds': 1800,
    },
    'shift-and-share': {
        'class': 'tools.implementations.ShiftAndShareTool',
        'form_class': 'tools.forms.ShiftAndShareForm',
        'title': 'Shift & Share',
        'icon': 'arrows-spin',
        'category': 'Facilitation',
        'what': (
            'Replace long large-group presentations with simultaneous concise '
            'station sessions. A few innovators share in 10 minutes; small groups '
            'rotate through every station, then share what they learned.'
        ),
        'how': (
            'Identify 3–7 presenters and form an equal number of small groups (5 min). '
            'Each group visits a different station for a 10-min presentation plus '
            '2-min Q&A, then rotates (1 min per move) until everyone has visited '
            'every station. ~90 min for 6 stations.'
        ),
        'why': (
            'Quickly surface innovations hidden within the group and build a '
            'community of practice. Reveal frontline contributions that formal '
            'hierarchies can obscure, and spark collaboration and friendly '
            'mash-ups across teams.'
        ),
        'example_input': {
            'innovation_summary': (
                'I shared our async-first onboarding approach: new hires complete '
                'a self-paced module before any live sessions, cutting first-week '
                'confusion by roughly half.'
            ),
            'questions_feedback': (
                'Teams asked how we handle questions that come up during the '
                'module. Feedback: add a short FAQ section and a Slack channel '
                'dedicated to onboarding questions.'
            ),
            'key_takeaways': (
                'Station 3 showed a brilliant visual "team radar" to track skill '
                'gaps. I want to bring that back to our team.'
            ),
        },
        'display_fields': [
            'innovation_summary',
            'questions_feedback',
            'key_takeaways',
            'word_count',
        ],
        'timer_seconds': 5400,
    },
    'discovery-action-dialogue': {
        'class': 'tools.implementations.DiscoveryActionDialogueTool',
        'form_class': 'tools.forms.DiscoveryActionDialogueForm',
        'title': 'Discovery & Action Dialogue',
        'icon': 'magnifying-glass-chart',
        'category': 'Facilitation',
        'what': (
            'Surface hidden local solutions to chronic problems by asking '
            'seven progressive questions that draw out positive-deviant '
            'practices already present in your group or community.'
        ),
        'how': (
            'Introduce the purpose and invite brief round-robin introductions (5 min). '
            'Work through the seven questions one by one, giving everyone a voice '
            'at each step while a recorder captures insights and action ideas (15–60 min). '
            'Recap insights, actions, and who else to involve (5 min).'
        ),
        'why': (
            'Unleash local wisdom without importing outside solutions. '
            'Stimulate change and innovation by engaging all forms of diversity '
            'present in your group, and create favourable conditions for '
            'positive deviant behaviours to spread.'
        ),
        'example_input': {
            'problem_presence': 'We notice delayed responses, repeated questions, and low morale in standups.',
            'effective_contributions': 'I circulate a shared prep doc the night before so people arrive ready to contribute.',
            'barriers': 'Time pressure and no shared habit — the doc only works if everyone buys in.',
            'positive_deviants': 'Jana consistently keeps standups under 10 min by timeboxing each speaker. She makes it feel safe to say "let\'s take that offline".',
            'ideas': 'Use a rotating facilitator role and a visible parking-lot board for side conversations.',
            'next_steps': 'Pilot rotating facilitation next week. Sarah volunteered to draft the guide.',
            'who_else': 'The product owner and two team leads who were not in this session.',
        },
        'display_fields': [
            'problem_presence',
            'effective_contributions',
            'barriers',
            'positive_deviants',
            'ideas',
            'next_steps',
            'who_else',
            'word_count',
        ],
        'timer_seconds': 2100,
    },
    'what-so-what-now-what': {
        'class': 'tools.implementations.WhatSoWhatNowWhatTool',
        'form_class': 'tools.forms.WhatSoWhatNowWhatForm',
        'title': 'What, So What, Now What?',
        'icon': 'layer-group',
        'category': 'Facilitation',
        'what': (
            'Reflect on a shared experience in three disciplined stages — '
            'facts first, then sense-making, then action — so every voice is '
            'heard and understanding is genuinely shared before decisions are made.'
        ),
        'how': (
            'Stage 1 — WHAT? Individually note facts and observations (1 min), '
            'then share in a small group (2–7 min), then collect salient points '
            'with the whole group. Repeat for SO WHAT? (patterns, conclusions, '
            'hypotheses) and NOW WHAT? (actions). ~45 min total.'
        ),
        'why': (
            'Avoid jumping prematurely to action. Build shared understanding, '
            'surface all the data, and eliminate arguments rooted in different '
            'interpretations of what actually happened.'
        ),
        'example_input': {
            'what': (
                'Attendance dropped in week 3. '
                'Three teams submitted work late. '
                'Energy in the room felt lower than usual.'
            ),
            'so_what': (
                'The pattern suggests people are overloaded. '
                'There may be a misalignment between the pace we set and capacity.'
            ),
            'now_what': (
                'We will reduce the number of parallel workstreams next sprint '
                'and check in weekly on load rather than monthly.'
            ),
        },
        'display_fields': ['what', 'so_what', 'now_what', 'word_count'],
        'timer_seconds': 2700,
    },
    'troika-consulting': {
        'class': 'tools.implementations.TroikaConsultingTool',
        'form_class': 'tools.forms.TroikaConsultingForm',
        'title': 'Troika Consulting',
        'icon': 'people-arrows',
        'category': 'Facilitation',
        'what': (
            'Peer-to-peer coaching in trios. Each person takes a turn as client '
            'while the other two consult — back turned, speaking freely.'
        ),
        'how': (
            'Reflect on your challenge and the help you need (1 min). '
            'As client, share your question (1–2 min), answer clarifying questions '
            '(1–2 min), then turn your back while consultants generate advice (4–5 min). '
            'Turn back and share what was most valuable (1–2 min). '
            'Repeat for each person in the trio.'
        ),
        'why': (
            'Help people gain insight on issues they face and unleash local wisdom. '
            'Extend peer coaching beyond formal reporting relationships and '
            'reveal patterns, discover everyday solutions, and refine prototypes.'
        ),
        'example_input': {
            'consulting_question': 'I am struggling to get cross-team buy-in for a new process. What should I try?',
            'consultant_advice': (
                'We suggested mapping the stakeholders and finding one early champion. '
                'Also: frame it as an experiment, not a permanent change.'
            ),
            'valuable_takeaway': 'The idea of finding one champion first felt immediately actionable.',
        },
        'display_fields': [
            'consulting_question',
            'consultant_advice',
            'valuable_takeaway',
            'word_count',
        ],
        'timer_seconds': 1800,
    },
    '15-percent-solutions': {
        'class': 'tools.implementations.FifteenPercentSolutionsTool',
        'form_class': 'tools.forms.FifteenPercentSolutionsForm',
        'title': '15% Solutions',
        'icon': 'seedling',
        'category': 'Facilitation',
        'what': (
            'Reveal the actions — however small — that everyone can do immediately '
            'using only what they already have. 15% is always there for the taking.'
        ),
        'how': (
            'Alone, generate your list of 15% Solutions: things you can do without '
            'more resources or authority (5 min). Share with a small group, one '
            'person at a time (3 min each). Then receive clarifying questions and '
            'advice from the group (5–7 min each).'
        ),
        'why': (
            'Move away from blockage and powerlessness. Reveal bottom-up solutions, '
            'close the knowing-doing gap, and build trust by helping one another act '
            'on what is already within reach.'
        ),
        'example_input': {
            'solutions_list': (
                'I can start a weekly 15-min knowledge-share in my team. '
                'I can document one process this week without being asked.'
            ),
            'group_share': (
                'I shared my ideas and heard a colleague plans to connect two '
                'teams who never talk but face the same problem.'
            ),
            'consultation_insights': (
                'The group asked who else should know about this. '
                'Advice: start small and make it visible so others can join.'
            ),
        },
        'display_fields': [
            'solutions_list',
            'group_share',
            'consultation_insights',
            'word_count',
        ],
        'timer_seconds': 1200,
    },
    'triz': {
        'class': 'tools.implementations.TrizTool',
        'form_class': 'tools.forms.TrizForm',
        'title': 'TRIZ',
        'icon': 'trash-can',
        'category': 'Facilitation',
        'what': (
            'Clear space for innovation by challenging sacred cows safely. '
            'Invert your objective to expose what is actually holding progress back.'
        ),
        'how': (
            'Three steps, each 10 minutes, using 1-2-4-All within your group: '
            '(1) List all you could do to guarantee the worst result. '
            '(2) Identify what you are currently doing that resembles that list. '
            '(3) Decide on first steps to stop each counterproductive activity.'
        ),
        'why': (
            'Make it possible to speak the unspeakable and get skeletons out of '
            'the closet. Build trust by acting together to remove barriers and '
            'lay the ground for creative destruction in a seriously fun way.'
        ),
        'example_input': {
            'worst_result_list': (
                'Never share information across teams. '
                'Reward individual performance only. '
                'Hold endless meetings with no decisions.'
            ),
            'current_resemblances': (
                'We do silo our knowledge in separate drives. '
                'Our bonus structure is entirely individual.'
            ),
            'stop_first_steps': (
                'We will stop sending reports only to our own team. '
                'I will stop attending status meetings with no agenda.'
            ),
        },
        'display_fields': [
            'worst_result_list',
            'current_resemblances',
            'stop_first_steps',
            'word_count',
        ],
        'timer_seconds': 2100,
    },
    'appreciative-interviews': {
        'class': 'tools.implementations.AppreciativeInterviewsTool',
        'form_class': 'tools.forms.AppreciativeInterviewsForm',
        'title': 'Appreciative Interviews',
        'icon': 'comments',
        'category': 'Facilitation',
        'what': (
            'Generate the conditions essential for success by surfacing hidden '
            'success stories. Positive momentum springs from uncovering what '
            'works and why.'
        ),
        'how': (
            'In pairs, take turns interviewing each other about a proud success '
            'story and what made it possible (15–20 min). In groups of four, '
            'retell your partner\'s story and listen for patterns (15 min). '
            'Collect insights for the whole group, then discuss opportunities '
            'to invest more in those conditions (10–15 min + 10 min).'
        ),
        'why': (
            'Groups are energised sharing success stories rather than problems. '
            'Spontaneous momentum and insights for positive change are liberated '
            'as "hidden" stories are revealed and root causes of success identified.'
        ),
        'example_input': {
            'success_story': 'A time our team pulled together under pressure and delivered something we were proud of…',
            'success_conditions': 'Clear purpose, trust between members, and space to experiment.',
            'partner_story': 'My partner described a project where leadership stepped back and let the team lead…',
            'group_patterns': 'Psychological safety, shared ownership, and consistent communication appeared across stories.',
            'opportunities': 'We could invest more in regular reflection time and cross-team storytelling.',
        },
        'display_fields': [
            'success_story',
            'success_conditions',
            'partner_story',
            'group_patterns',
            'opportunities',
            'word_count',
        ],
        'timer_seconds': 3600,
    },
    'wicked-questions': {
        'class': 'tools.implementations.WickedQuestionsTool',
        'form_class': 'tools.forms.WickedQuestionsForm',
        'title': 'Wicked Questions',
        'icon': 'bolt',
        'category': 'Facilitation',
        'what': (
            'Articulate the paradoxical challenges a group must confront to succeed. '
            'Surface opposing-yet-complementary strategies that must be pursued simultaneously.'
        ),
        'how': (
            'Individually generate pairs of opposites using the format '
            '"How is it that we are ____ and we are ____ simultaneously?" (5 min). '
            'Small groups select their most impactful question (5 min). '
            'The whole group picks out the most powerful and refines them (10 min).'
        ),
        'why': (
            'Spark innovative action while diminishing "yes, but…" and "either-or" thinking. '
            'Bring to light paradoxical-yet-complementary forces that influence behaviours, '
            'especially during change efforts.'
        ),
        'example_input': {
            'individual_questions': (
                'How is it that we are deeply committed to our staff and we are '
                'constantly asking them to do more with less, simultaneously?'
            ),
            'group_question': (
                'How is it that we are focused on long-term strategy and we are '
                'reacting to short-term pressures, simultaneously?'
            ),
            'whole_group_refinement': (
                'The group sharpened this to: "How is it that we prize innovation '
                'and we reward compliance, simultaneously?"'
            ),
        },
        'display_fields': [
            'individual_questions',
            'group_question',
            'whole_group_refinement',
            'word_count',
        ],
        'timer_seconds': 1500,
    },
    'nine-whys': {
        'class': 'tools.implementations.NineWhysTool',
        'form_class': 'tools.forms.NineWhysForm',
        'title': 'Nine Whys',
        'icon': 'circle-question',
        'category': 'Facilitation',
        'what': (
            'Rapidly clarify for individuals and a group what is essentially '
            'important in their work by asking "Why?" up to nine times.'
        ),
        'how': (
            'In pairs, one partner interviews the other for 5 minutes — '
            'starting with activities, then asking "Why is that important?" '
            'repeatedly. Switch roles. Then share insights in a foursome, '
            'and finally reflect as a whole group.'
        ),
        'why': (
            'When a group discovers an unambiguous shared purpose, more freedom '
            'and responsibility are unleashed. You lay the foundation for '
            'spreading innovations with fidelity.'
        ),
        'example_input': {
            'activities': 'I facilitate workshops, write reports, coordinate teams…',
            'why_chain': 'Because it helps people align… because alignment reduces waste… because…',
            'fundamental_purpose': 'To make sure no one is left behind.',
            'foursome_insights': 'We all arrived at themes of connection and meaning.',
            'group_reflection': 'Our shared purpose should shape how we prioritise the agenda.',
        },
        'display_fields': [
            'activities',
            'why_chain',
            'fundamental_purpose',
            'foursome_insights',
            'group_reflection',
            'word_count',
        ],
        'timer_seconds': 1200,
    },
    'impromptu-networking': {
        'class': 'tools.implementations.ImpromptNetworkingTool',
        'form_class': 'tools.forms.ImpromptNetworkingForm',
        'title': 'Impromptu Networking',
        'icon': 'handshake',
        'category': 'Facilitation',
        'what': (
            'Tap a deep well of curiosity and talent by helping the group '
            'focus on problems they want to solve. Loose yet powerful '
            'connections are formed in 20 minutes.'
        ),
        'how': (
            'Three rounds of pair conversations (4–5 min each). Before you '
            'begin, write down your challenge and what you hope to get and '
            'give. Find a new partner for each round.'
        ),
        'why': (
            'Initiate participation immediately. Attract deeper engagement '
            'around challenges, invite stories to deepen as they are repeated, '
            'and affirm that little things can make a big difference.'
        ),
        'example_input': {
            'challenge': 'A challenge I bring is…',
            'give_and_get': 'I hope to get… and give…',
            'round_one': 'In Round 1 I heard…',
            'round_two': 'In Round 2 I noticed…',
            'round_three': 'In Round 3 the pattern I saw was…',
        },
        'display_fields': [
            'challenge',
            'give_and_get',
            'round_one',
            'round_two',
            'round_three',
            'word_count',
        ],
        'timer_seconds': 1200,
    },
    '1-2-4-all': {
        'class': 'tools.implementations.OneTwoFourAllTool',
        'form_class': 'tools.forms.OneTwoFourAllForm',
        'title': '1-2-4-All',
        'icon': 'people-group',
        'category': 'Facilitation',
        'what': (
            'Engage everyone simultaneously in generating questions, ideas, '
            'and suggestions — regardless of group size.'
        ),
        'how': (
            'Work through four timed phases: 1 min of silent self-reflection, '
            '2 min in pairs, 4 min in foursomes, then 5 min sharing one '
            'standout idea with the whole group.'
        ),
        'why': (
            'Ideas and solutions are sifted rapidly. Participants own the '
            'ideas, so follow-up and implementation is simplified — no '
            'buy-in strategies needed.'
        ),
        'example_input': {
            'self_reflection': 'One opportunity I see is…',
            'pair_ideas': 'Together we noticed…',
            'foursome_ideas': 'Our group built on the idea that…',
            'standout_idea': 'The idea that stood out most was…',
        },
        'display_fields': [
            'self_reflection',
            'pair_ideas',
            'foursome_ideas',
            'standout_idea',
            'word_count',
        ],
        'timer_seconds': 720,
        'phases': [
            {'label': 'Phase 1 — Self-reflection', 'seconds': 60},
            {'label': 'Phase 2 — Pair ideas', 'seconds': 120},
            {'label': 'Phase 3 — Foursome ideas', 'seconds': 240},
            {'label': 'Phase 4 — Standout idea', 'seconds': 300},
        ],
    },
    'i-am-and-i-like': {
        'class': 'tools.implementations.IAmAndILikeTool',
        'form_class': 'tools.forms.IAmAndILikeForm',
        'title': 'I am and I like',
        'icon': 'smile',
        'category': 'Low-Risk Warm-ups',
        'what': (
            'The group stands or sits in a circle, facing inwards.'
        ),
        'how': (
            'Going around the circle everyone says their first name, '
            'together with something they like or do not like or both.'
        ),
        'why': 'Keep working on breaking the ice.',
        'example_input': {
            'i_like': 'walking in the rain',
            'i_do_not_like': 'cold coffee',
        },
        'display_fields': ['statement', 'i_like', 'i_do_not_like', 'word_count'],
        'timer_seconds': 60,
    },
    'idea-generation': {
        'class': 'tools.implementations.IdeaGenerationTool',
        'form_class': 'tools.forms.IdeaGenerationForm',
        'title': 'Idea Generation',
        'icon': 'lightbulb',
        'category': 'Facilitation',
        'how_to': (
            'Spend a minute writing down your individual reflection before '
            'sharing it with the group.'
        ),
        'example_input': {
            'initial_thought': 'A challenge I keep noticing is...',
        },
        'display_fields': ['initial_thought', 'word_count'],
        'timer_seconds': 60,
    },
    'five-structural-elements': {
        'class': 'tools.implementations.FiveStructuralElementsTool',
        'form_class': 'tools.forms.FiveStructuralElementsForm',
        'title': 'Five Structural Elements',
        'icon': 'brickpile',
        'category': 'Facilitation',
        'how_to': (
            'Rapidly share challenges and expectations, build new connections. '
            'Get into pairs.'
        ),
        'example_input': {
            'pair_one_challenge': 'A challenge I bring is...',
            'pair_one_hope': 'I hope to get... and give...',
            'pair_two_challenge': 'A challenge I bring is...',
            'pair_two_hope': 'I hope to get... and give...',
        },
        'display_fields': [
            'pair_one_challenge', 'pair_one_hope',
            'pair_two_challenge', 'pair_two_hope',
            'word_count',
        ],
        'timer_seconds': 1200,
    },
}


def _resolve_class(dotted_path):
    module_path, _, class_name = dotted_path.rpartition('.')
    return getattr(import_module(module_path), class_name)


def get_tool_instance(slug, input_data=None):
    """Fetch and initialize a tool by its slug."""
    info = TOOL_CATALOG.get(slug)
    if not info:
        return None
    tool_class = _resolve_class(info['class'])
    return tool_class(user_input=input_data)


def get_tool_form_class(slug):
    """Return the Django form class associated with a tool, or None."""
    info = TOOL_CATALOG.get(slug)
    if not info or 'form_class' not in info:
        return None
    return _resolve_class(info['form_class'])
