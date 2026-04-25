from django import forms


class IdeaGenerationForm(forms.Form):
    initial_thought = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your individual reflection (1 min)...'}),
        label="Phase 1: Self-Reflection"
    )


class IAmAndILikeForm(forms.Form):
    i_like = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'I like…',
            'rows': 2,
        }),
        label="I like…",
        required=False,
    )
    i_do_not_like = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'I do not like…',
            'rows': 2,
        }),
        label="I do not like…",
        required=False,
    )


class ConversationCafeForm(forms.Form):
    theme = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What is the theme or question your group will explore? '
                'Frame it as an open question that invites reflection rather than debate.'
            ),
            'rows': 2,
        }),
        label='Theme or question for the conversation',
    )
    round_one = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Round 1 — talking object: '
                'What are you thinking, feeling, or doing about the theme right now? '
                '(1 min per person, no interrupting)'
            ),
            'rows': 3,
        }),
        label='Round 1 — your initial thoughts, feelings, or actions on the theme (1 min per person)',
    )
    round_two = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Round 2 — talking object: '
                'After listening to everyone, what shifted or deepened for you? '
                '(1 min per person)'
            ),
            'rows': 3,
        }),
        label='Round 2 — what shifted after listening to everyone (1 min per person)',
    )
    open_conversation = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Round 3 — open conversation: '
                'What threads or insights emerged? '
                'What surprised you? What felt most alive in the room?'
            ),
            'rows': 5,
        }),
        label='Round 3 — key threads and insights from the open conversation (20–40 min)',
    )
    takeaway = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Round 4 — talking object: '
                'What do you take away from this conversation? '
                'What will you carry forward?'
            ),
            'rows': 3,
        }),
        label='Round 4 — your takeaway (5–10 min)',
    )


class HelpingHeuristicsForm(forms.Form):
    challenge = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What challenge are you passionate about working on? '
                'Share something real and specific — the more genuine, '
                'the richer the coaching interactions will be.'
            ),
            'rows': 3,
        }),
        label='Your challenge as client',
    )
    quiet_presence = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Round 1 — Quiet Presence: '
                'What did it feel like to be heard with compassionate listening and no advice? '
                'What did you notice as coach or observer?'
            ),
            'rows': 3,
        }),
        label='Round 1 — Quiet Presence (compassionate listening, 2 min)',
    )
    guided_discovery = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Round 2 — Guided Discovery: '
                'What happened when the coach guided inquiry rather than offering solutions? '
                'What was discovered?'
            ),
            'rows': 3,
        }),
        label='Round 2 — Guided Discovery (inquiry for mutual discovery, 2 min)',
    )
    loving_provocation = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Round 3 — Loving Provocation: '
                'What happened when the coach interjected advice and gently challenged? '
                'What did the coach see that the client did not?'
            ),
            'rows': 3,
        }),
        label='Round 3 — Loving Provocation (advice, accepting and blocking, 2 min)',
    )
    process_mindfulness = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Round 4 — Process Mindfulness: '
                'What novel possibilities emerged when both coach and client accepted all offers? '
                'What felt different about this round?'
            ),
            'rows': 3,
        }),
        label='Round 4 — Process Mindfulness (accepting all offers, noticing possibilities, 2 min)',
    )
    debrief = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Which pattern had the most impact? '
                'What did you notice about your own habits of helping, asking, and receiving? '
                'What shift will you make?'
            ),
            'rows': 4,
        }),
        label='Debrief — impact of all four patterns as client, coach, and observer (5 min)',
    )


class ImprovPrototypingForm(forms.Form):
    scenario = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What is the chronic challenge being explored? '
                'Describe the scene, the roles, and the situation to be acted out. '
                'What frustrating pattern are the players depicting?'
            ),
            'rows': 4,
        }),
        label='The challenge and scene — set the stage (3 min)',
    )
    scene_observations = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What worked in the scene? What did not? '
                'List the successful chunks worth keeping and the unsuccessful ones '
                'worth discarding. (Debrief in 1-2-4-All, 5 min.)'
            ),
            'rows': 4,
        }),
        label='Successful and unsuccessful chunks observed in the scene (1-2-4-All, 5 min)',
    )
    prototype = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'How did your group piece the successful chunks together into a new prototype? '
                'Describe what was acted out and what made it better than the original.'
            ),
            'rows': 4,
        }),
        label='Your improved prototype — assembled from the successful chunks (5 min)',
    )
    reflection = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'After all rounds, what prototype or behaviour is good enough to put into practice? '
                'What new insight emerged that you did not have before you started?'
            ),
            'rows': 3,
        }),
        label='What is good enough to put into practice',
    )


class MinSpecsForm(forms.Form):
    max_specs = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'List every must-do and must-not-do you can think of. '
                'Make the list as complete as possible — include everything, '
                'even rules that may turn out to be nonessential.'
            ),
            'rows': 6,
        }),
        label='Max Specs — full list of all must-dos and must-not-dos (1 min alone, 5 min small group)',
    )
    sifting_result = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'For each rule on your Max Spec list, ask: '
                '"If we broke or ignored this rule, could we still achieve our purpose?" '
                'List what was dropped and briefly why. Note what survived the test.'
            ),
            'rows': 5,
        }),
        label='Sifting — what was dropped after testing against the purpose, and what survived',
    )
    min_specs = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Your final, shortest possible list. '
                'Only the rules that are truly essential — '
                'nothing more that can be taken away.'
            ),
            'rows': 4,
        }),
        label='Min Specs — the absolute essentials only',
    )


class WiseCrowdsLargeGroupForm(forms.Form):
    challenge = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Describe your challenge, the status of any work in progress, '
                'and the specific advice or help you are looking for.'
            ),
            'rows': 5,
        }),
        label='Client challenge and request for help (10 min presentation)',
    )
    clarifying_questions = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What clarifying questions did the primary consulting team ask?',
            'rows': 3,
        }),
        label='Clarifying questions from the primary consulting team (10 min)',
    )
    primary_advice = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What joint advice and recommendations did the primary consulting team '
                'develop while the client had their back turned?'
            ),
            'rows': 4,
        }),
        label='Primary consulting team\'s joint advice — client back turned (7 min)',
    )
    satellite_feedback = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What critiques of the primary team\'s advice emerged from satellite teams? '
                'What additional recommendations did they contribute? '
                '(One comment and one recommendation per team, no repeats.)'
            ),
            'rows': 4,
        }),
        label='Critiques and recommendations from satellite teams (10 min)',
    )
    takeaway = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What was most useful? What do you take away from this consultation?',
            'rows': 3,
        }),
        label='Client feedback — what was useful and what you take away (2 min)',
    )
    group_reflection = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What did the full group notice about this process? '
                'So what — why does it matter? '
                'Now what — what actions follow?'
            ),
            'rows': 3,
        }),
        label='Full-group reflection — So What and Now What (5 min)',
    )


class WiseCrowdsForm(forms.Form):
    challenge = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Briefly describe your challenge and what kind of help you are asking for. '
                'Be specific enough that your consultants can give useful advice.'
            ),
            'rows': 4,
        }),
        label='Your challenge and request for help (client presents, 2 min)',
    )
    clarifying_questions = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What questions did your consultants ask to clarify the challenge?',
            'rows': 3,
        }),
        label='Clarifying questions the consultants asked (3 min)',
    )
    consultant_advice = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What advice, recommendations, or ideas did the consultants offer '
                'while you had your back turned? Capture what you heard.'
            ),
            'rows': 5,
        }),
        label='Advice and recommendations from consultants — back turned (8 min)',
    )
    takeaway = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What was most useful? '
                'What will you take away from this consultation?'
            ),
            'rows': 3,
        }),
        label='Your feedback to the consultants — what was useful and what you take away (2 min)',
    )


class TwentyFiveTenCrowdSourcingForm(forms.Form):
    bold_idea = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'If you were ten times bolder, what big idea would you recommend? '
                'What first step would you take to get started?'
            ),
            'rows': 4,
        }),
        label='Your bold idea and first step (write on your index card, 5 min)',
    )
    scores_received = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What five scores (each 1–5) did your card receive across the rounds? '
                'What was the total out of 25?'
            ),
            'rows': 2,
        }),
        label='Scores your card received across the five rounds (total out of 25)',
    )
    top_ideas = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Which ideas scored highest in the countdown from 25? '
                'What surprised you? What caught your attention?'
            ),
            'rows': 4,
        }),
        label='Top ideas that emerged — and what caught your attention (2 min debrief)',
    )


class ShiftAndShareForm(forms.Form):
    innovation_summary = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What is the innovation or program you are sharing? '
                'Describe the essence in a way that helps others see the value — '
                'include a story, example, or object if possible.'
            ),
            'rows': 5,
        }),
        label='Your innovation — what you shared at your station (10 min presentation)',
    )
    questions_feedback = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What questions did visitors ask? '
                'What feedback or reactions stood out? '
                'If you were a visitor, what did you ask or contribute?'
            ),
            'rows': 4,
        }),
        label='Questions and feedback at your station (2 min per visit)',
    )
    key_takeaways = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What innovations did you see at other stations? '
                'What ideas sparked your thinking? '
                'Any potential collaborations or follow-ups?'
            ),
            'rows': 4,
        }),
        label='What you learned visiting other stations',
    )


class DiscoveryActionDialogueForm(forms.Form):
    problem_presence = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What signals or signs tell you the problem is present?',
            'rows': 3,
        }),
        label='Q1 — How do you know when the problem is present?',
    )
    effective_contributions = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What specific actions or approaches do you take that actually help?',
            'rows': 3,
        }),
        label='Q2 — How do you contribute effectively to solving it?',
    )
    barriers = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What gets in the way of doing those things consistently?',
            'rows': 3,
        }),
        label='Q3 — What prevents you from doing this all the time?',
    )
    positive_deviants = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Who in this group or community manages to solve this more often? '
                'What behaviours or practices make their success possible?'
            ),
            'rows': 3,
        }),
        label='Q4 — Who frequently overcomes these barriers, and how?',
    )
    ideas = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Any ideas for solving this problem or removing barriers?',
            'rows': 3,
        }),
        label='Q5 — Do you have any ideas?',
    )
    next_steps = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What concrete steps need to happen? Who is willing to take them on?',
            'rows': 3,
        }),
        label='Q6 — What needs to happen? Any volunteers?',
    )
    who_else = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Who else should be part of this conversation or effort?',
            'rows': 3,
        }),
        label='Q7 — Who else needs to be involved?',
    )


class WhatSoWhatNowWhatForm(forms.Form):
    what = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What happened? What did you notice? '
                'What facts or observations stood out? (Stick to observable facts — save interpretations for So What)'
            ),
            'rows': 4,
        }),
        label='WHAT? — Facts and observations (1 min alone, then small group)',
    )
    so_what = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Why is that important? '
                'What patterns or conclusions are emerging? '
                'What hypotheses can you make?'
            ),
            'rows': 4,
        }),
        label='SO WHAT? — Patterns and conclusions (1 min alone, then small group)',
    )
    now_what = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What actions make sense? What will you do differently?',
            'rows': 4,
        }),
        label='NOW WHAT? — Actions (1 min alone, small group, then whole group)',
    )


class TroikaConsultingForm(forms.Form):
    consulting_question = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What is your challenge? '
                'What kind of help do you need from your consultants?'
            ),
            'rows': 3,
        }),
        label='Your consulting question (reflect alone, 1 min)',
    )
    consultant_advice = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What ideas, suggestions, or coaching advice did you offer '
                'while acting as a consultant for your colleagues?'
            ),
            'rows': 4,
        }),
        label='Advice you gave as a consultant',
    )
    valuable_takeaway = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What was most valuable about what you heard when you were the client? '
                'What will you take away?'
            ),
            'rows': 3,
        }),
        label='Most valuable takeaway from your client turn (1–2 min)',
    )


class FifteenPercentSolutionsForm(forms.Form):
    solutions_list = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'What is your 15 percent? Where do you have discretion and freedom to act? '
                'What can you do without more resources or authority?'
            ),
            'rows': 5,
        }),
        label='Your 15% Solutions (individual, 5 min)',
    )
    group_share = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What did you share with your group? What did others share that resonated with you?',
            'rows': 4,
        }),
        label='Small group share (3 min per person)',
    )
    consultation_insights = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What clarifying questions did you receive? What advice was offered or given?',
            'rows': 4,
        }),
        label='Group consultation — questions and advice (5–7 min per person)',
    )


class TrizForm(forms.Form):
    worst_result_list = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'List everything you could do to guarantee the worst result '
                'imaginable for your top strategy or objective…'
            ),
            'rows': 5,
        }),
        label='Step 1 — How to guarantee the worst result (10 min)',
    )
    current_resemblances = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Go through your list above item by item. '
                'What are you currently doing that in any way resembles those items? '
                'Be brutally honest…'
            ),
            'rows': 5,
        }),
        label='Step 2 — What we are currently doing that resembles that list (10 min)',
    )
    stop_first_steps = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'For each item above, what first steps will help you stop it? '
                'Frame as "I will stop…" or "We will stop…"'
            ),
            'rows': 4,
        }),
        label='Step 3 — First steps to stop counterproductive activities (10 min)',
    )


class AppreciativeInterviewsForm(forms.Form):
    success_story = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Tell a story about a time when you worked on a challenge with others '
                'and you are proud of what you accomplished…'
            ),
            'rows': 5,
        }),
        label='Your success story (pairs, 15–20 min)',
    )
    success_conditions = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What made the success possible? What conditions or assets were at play?',
            'rows': 3,
        }),
        label='What made the success possible?',
    )
    partner_story = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Retell your partner\'s story. '
                'What patterns in conditions or assets supporting success did you notice?'
            ),
            'rows': 4,
        }),
        label='Your partner\'s story and patterns noticed (groups of 4, 15 min)',
    )
    group_patterns = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Conditions and assets for success collected by the whole group…',
            'rows': 4,
        }),
        label='Whole-group patterns and conditions (10–15 min)',
    )
    opportunities = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'How are we investing in the assets and conditions that foster success? '
                'What opportunities do you see to do more?'
            ),
            'rows': 3,
        }),
        label='Opportunities to invest more (10 min)',
    )


class WickedQuestionsForm(forms.Form):
    individual_questions = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Use the format: "How is it that we are ____ and we are ____ simultaneously?"\n'
                'Write one or more pairs of opposites that are at play in your work…'
            ),
            'rows': 5,
        }),
        label='Your Wicked Questions (individual, 5 min)',
    )
    group_question = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'The most impactful Wicked Question your small group selected…',
            'rows': 3,
        }),
        label='Small group\'s selected Wicked Question (5 min)',
    )
    whole_group_refinement = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'The most powerful questions and any further refinements from the whole group…',
            'rows': 4,
        }),
        label='Whole-group refinement (10 min)',
    )


class NineWhysForm(forms.Form):
    activities = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What do you do when working on this challenge? List your activities…',
            'rows': 3,
        }),
        label='Your activities',
    )
    why_chain = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Record your answers as your partner asked "Why is that important to you?" '
                'up to nine times…'
            ),
            'rows': 5,
        }),
        label='Your why-chain (pairs interview, 10 min)',
    )
    fundamental_purpose = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'The deepest "why" you reached — the fundamental purpose of this work…',
            'rows': 2,
        }),
        label='Your fundamental purpose',
    )
    foursome_insights = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What did your foursome share? What insights or patterns emerged?',
            'rows': 3,
        }),
        label='Foursome insights (5 min)',
    )
    group_reflection = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'How do our purposes influence the next steps we take?',
            'rows': 3,
        }),
        label='Whole-group reflection (5 min)',
    )


class ImpromptNetworkingForm(forms.Form):
    challenge = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What big challenge do you bring to this gathering?',
            'rows': 3,
        }),
        label='Your challenge',
    )
    give_and_get = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What do you hope to get from and give this group or community?',
            'rows': 3,
        }),
        label='What you hope to get and give',
    )
    round_one = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What did you hear, share, or notice in Round 1?',
            'rows': 3,
        }),
        label='Round 1 notes (4–5 min)',
    )
    round_two = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What did you hear, share, or notice in Round 2?',
            'rows': 3,
        }),
        label='Round 2 notes (4–5 min)',
    )
    round_three = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What did you hear, share, or notice in Round 3?',
            'rows': 3,
        }),
        label='Round 3 notes (4–5 min)',
    )


class OneTwoFourAllForm(forms.Form):
    self_reflection = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What opportunities do YOU see for making progress on this challenge?',
            'rows': 3,
        }),
        label='Phase 1 — Self-reflection (1 min)',
    )
    pair_ideas = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Ideas generated with your pair partner…',
            'rows': 3,
        }),
        label='Phase 2 — Pair ideas (2 min)',
    )
    foursome_ideas = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Ideas and themes that emerged in your group of four…',
            'rows': 3,
        }),
        label='Phase 3 — Foursome ideas (4 min)',
    )
    standout_idea = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What is one idea that stood out in your conversation?',
            'rows': 2,
        }),
        label='Phase 4 — Standout idea for whole group (5 min)',
    )


class FiveStructuralElementsForm(forms.Form):
    pair_one_challenge = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What big challenge do you bring to this gathering?',
            'rows': 3,
        }),
        label="Pair Member One — Challenge",
    )
    pair_one_hope = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What do you hope to get from and give this group?',
            'rows': 3,
        }),
        label="Pair Member One — Hope",
    )
    pair_two_challenge = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What big challenge do you bring to this gathering?',
            'rows': 3,
        }),
        label="Pair Member Two — Challenge",
    )
    pair_two_hope = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What do you hope to get from and give this group?',
            'rows': 3,
        }),
        label="Pair Member Two — Hope",
    )
