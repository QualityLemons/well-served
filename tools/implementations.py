from .interface import BaseTool


class IdeaGenerationTool(BaseTool):
    name = 'Idea Generation'
    description = 'Capture an individual reflection as the start of an idea-generation session.'
    version = '1.0'

    def validate(self):
        text = (self.user_input.get('initial_thought') or '').strip()
        if len(text) < 5:
            self.errors['initial_thought'] = 'Please write a slightly longer reflection.'

    def process(self):
        text = (self.user_input.get('initial_thought') or '').strip()
        return {
            'initial_thought': text,
            'word_count': len(text.split()),
            'character_count': len(text),
        }


class IAmAndILikeTool(BaseTool):
    name = 'I am and I like'
    description = 'Each person shares their name with something they like or do not like.'
    version = '1.0'

    def validate(self):
        likes = (self.user_input.get('i_like') or '').strip()
        dislikes = (self.user_input.get('i_do_not_like') or '').strip()
        if not likes and not dislikes:
            self.errors['i_like'] = 'Please fill in at least one field.'

    def process(self):
        likes = (self.user_input.get('i_like') or '').strip()
        dislikes = (self.user_input.get('i_do_not_like') or '').strip()
        parts = []
        if likes:
            parts.append(f'I like {likes}')
        if dislikes:
            parts.append(f'I do not like {dislikes}')
        return {
            'statement': ' and '.join(parts) if parts else '',
            'i_like': likes,
            'i_do_not_like': dislikes,
            'word_count': len(' '.join(parts).split()),
        }


class WiseCrowdsLargeGroupTool(BaseTool):
    name = 'Wise Crowds (Large Group)'
    description = (
        'Tap the wisdom of a large group in a structured 1-hour consultation. '
        'One client, a primary consulting team at the front, and multiple satellite '
        'teams — all contributing advice in timed rounds.'
    )
    version = '1.0'

    PHASES = (
        ('challenge',          'Client presents the challenge and request for help (10 min)'),
        ('clarifying_questions', 'Clarifying questions from the primary consulting team (10 min)'),
        ('primary_advice',     'Primary consulting team\'s joint advice — client back turned (7 min)'),
        ('satellite_feedback', 'Critiques and recommendations from satellite teams (10 min)'),
        ('takeaway',           'Client feedback: what was useful and what they take away (2 min)'),
        ('group_reflection',   'Full-group reflection: So What and Now What (5 min)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class WiseCrowdsTool(BaseTool):
    name = 'Wise Crowds'
    description = (
        'Tap the wisdom of the whole group in rapid cycles. '
        'Each person takes a turn as client — presenting a challenge, '
        'receiving clarifying questions, then listening with their back turned '
        'while consultants advise freely.'
    )
    version = '1.0'

    PHASES = (
        ('challenge',            'Your challenge and request for help (client presents, 2 min)'),
        ('clarifying_questions', 'Clarifying questions consultants asked you (3 min)'),
        ('consultant_advice',    'Advice and recommendations from consultants while your back was turned (8 min)'),
        ('takeaway',             'What was useful and what you take away (client feedback, 2 min)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class TwentyFiveTenCrowdSourcingTool(BaseTool):
    name = '25/10 Crowd Sourcing'
    description = (
        'Rapidly generate and sift a group\'s most powerful actionable ideas. '
        'Everyone writes a bold idea and first step, passes cards through five '
        'scoring rounds, and the top ten rise to the surface.'
    )
    version = '1.0'

    PHASES = (
        ('bold_idea',    'Your bold idea and first step (write on your index card, 5 min)'),
        ('scores_received', 'The five scores your card received across the rounds (total out of 25)'),
        ('top_ideas',    'Ideas that rose to the top — what caught your attention? (2 min debrief)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class ShiftAndShareTool(BaseTool):
    name = 'Shift & Share'
    description = (
        'Spread good ideas and make informal connections with innovators. '
        'A few presenters set up stations; small groups rotate through each '
        'one for a 10-minute presentation and feedback round.'
    )
    version = '1.0'

    PHASES = (
        ('innovation_summary', 'Your innovation — what you shared or are sharing at your station (10 min each)'),
        ('questions_feedback',  'Questions and feedback received (or given) at your station (2 min each)'),
        ('key_takeaways',       'What you learned from visiting other stations'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class DiscoveryActionDialogueTool(BaseTool):
    name = 'Discovery & Action Dialogue'
    description = (
        'Discover, invent, and unleash local solutions to chronic problems. '
        'Seven progressive questions surface positive-deviant practices hidden '
        'within the group itself.'
    )
    version = '1.0'

    PHASES = (
        ('problem_presence',       'Q1 — How do you know when the problem is present?'),
        ('effective_contributions', 'Q2 — How do you contribute effectively to solving it?'),
        ('barriers',               'Q3 — What prevents you from doing this all the time?'),
        ('positive_deviants',      'Q4 — Who frequently overcomes these barriers, and what makes their success possible?'),
        ('ideas',                  'Q5 — Do you have any ideas?'),
        ('next_steps',             'Q6 — What needs to happen? Any volunteers?'),
        ('who_else',               'Q7 — Who else needs to be involved?'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class WhatSoWhatNowWhatTool(BaseTool):
    name = 'What, So What, Now What?'
    description = (
        'Together, look back on progress to date and decide what adjustments '
        'are needed. Three stages — facts, sense-making, and action — build '
        'shared understanding and spur coordinated action.'
    )
    version = '1.0'

    PHASES = (
        ('what',      'WHAT? Facts and observations you noticed (1 min alone, then small group)'),
        ('so_what',   'SO WHAT? Patterns, conclusions, and hypotheses emerging (1 min alone, then small group)'),
        ('now_what',  'NOW WHAT? Actions that make sense (1 min alone, small group, then whole group)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class TroikaConsultingTool(BaseTool):
    name = 'Troika Consulting'
    description = (
        'Get practical and imaginative help from colleagues immediately. '
        'Round-robin peer consultations in trios — each person takes a turn '
        'as client while the other two act as consultants.'
    )
    version = '1.0'

    PHASES = (
        ('consulting_question', 'Your challenge and the help you need (client reflection, 1 min)'),
        ('consultant_advice',   'Ideas, suggestions, and coaching advice you gave as a consultant'),
        ('valuable_takeaway',   'What was most valuable from your time as client (1–2 min)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class FifteenPercentSolutionsTool(BaseTool):
    name = '15% Solutions'
    description = (
        'Discover and focus on what each person has the freedom and resources '
        'to do right now. Reveal actions, however small, that create momentum.'
    )
    version = '1.0'

    PHASES = (
        ('solutions_list',       'Your 15% Solutions — what you can do without more resources or authority (individual, 5 min)'),
        ('group_share',          'What you shared with your small group and what you heard from others (3 min per person)'),
        ('consultation_insights', 'Clarifying questions and advice from the group consultation (5–7 min per person)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class TrizTool(BaseTool):
    name = 'TRIZ'
    description = (
        'Stop counterproductive activities and behaviours to make space for '
        'innovation. Three rounds of creative destruction using inversion.'
    )
    version = '1.0'

    PHASES = (
        ('worst_result_list',    'Everything you could do to guarantee the worst result (10 min)'),
        ('current_resemblances', 'What you are currently doing that resembles items on that list (10 min)'),
        ('stop_first_steps',     'First steps to stop each counterproductive activity (10 min)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class AppreciativeInterviewsTool(BaseTool):
    name = 'Appreciative Interviews'
    description = (
        'Discover and build on the root causes of success. '
        'In under an hour, a group of any size generates the conditions '
        'essential for its success by uncovering hidden success stories.'
    )
    version = '1.0'

    PHASES = (
        ('success_story',      'Your success story (pairs, 15–20 min)'),
        ('success_conditions', 'What made the success possible?'),
        ('partner_story',      'Your partner\'s story retold — and patterns you noticed (groups of 4, 15 min)'),
        ('group_patterns',     'Conditions and assets for success collected by the whole group (10–15 min)'),
        ('opportunities',      'How are we investing in these assets? What opportunities do you see? (10 min)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class WickedQuestionsTool(BaseTool):
    name = 'Wicked Questions'
    description = (
        'Articulate the paradoxical challenges a group must confront to succeed. '
        'Surface opposing-yet-complementary strategies that must be pursued simultaneously.'
    )
    version = '1.0'

    PHASES = (
        ('individual_questions',  'Your Wicked Questions — pairs of opposites (individual, 5 min)'),
        ('group_question',        'Your small group\'s most impactful Wicked Question (5 min)'),
        ('whole_group_refinement', 'Refined Wicked Questions from the whole group (10 min)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class NineWhysTool(BaseTool):
    name = 'Nine Whys'
    description = (
        'Make the purpose of your work together clear. '
        'Through repeated "Why?" questions, individuals and groups '
        'surface the fundamental purpose behind their work.'
    )
    version = '1.0'

    PHASES = (
        ('activities',           'Your activities (before interview)'),
        ('why_chain',            'Your why-chain — answers to repeated "Why is that important?" (10 min pairs)'),
        ('fundamental_purpose',  'The fundamental purpose you reached at the end of your why-chain'),
        ('foursome_insights',    'Insights and experiences shared in your foursome (5 min)'),
        ('group_reflection',     'How your purposes influence next steps — whole-group reflection (5 min)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class ImpromptNetworkingTool(BaseTool):
    name = 'Impromptu Networking'
    description = (
        'Rapidly share challenges and expectations, build new connections. '
        'Three rounds of pair conversations in 20 minutes.'
    )
    version = '1.0'

    PHASES = (
        ('challenge',   'Your challenge (before rounds begin)'),
        ('give_and_get', 'What you hope to get from and give the group (before rounds begin)'),
        ('round_one',   'Notes from Round 1 (4–5 min)'),
        ('round_two',   'Notes from Round 2 (4–5 min)'),
        ('round_three', 'Notes from Round 3 (4–5 min)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class OneTwoFourAllTool(BaseTool):
    name = '1-2-4-All'
    description = (
        'Engage everyone simultaneously in generating questions, ideas, and '
        'suggestions. Moves from individual reflection through pairs and '
        'foursomes to a whole-group share-out.'
    )
    version = '1.0'

    PHASES = (
        ('self_reflection',  'Individual reflection (1 min)'),
        ('pair_ideas',       'Ideas from your pair (2 min)'),
        ('foursome_ideas',   'Ideas from your foursome (4 min)'),
        ('standout_idea',    'One standout idea to share with everyone (5 min)'),
    )

    def validate(self):
        for field, label in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = f'{label}: please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field, _ in self.PHASES:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


class FiveStructuralElementsTool(BaseTool):
    name = 'Five Structural Elements'
    description = 'Pairs share challenges and hopes to build new connections.'
    version = '1.0'

    FIELDS = (
        'pair_one_challenge',
        'pair_one_hope',
        'pair_two_challenge',
        'pair_two_hope',
    )

    def validate(self):
        for field in self.FIELDS:
            value = (self.user_input.get(field) or '').strip()
            if len(value) < 3:
                self.errors[field] = 'Please write a slightly longer response.'

    def process(self):
        result = {}
        total_words = 0
        for field in self.FIELDS:
            value = (self.user_input.get(field) or '').strip()
            words = len(value.split())
            result[field] = value
            result[f'{field}_word_count'] = words
            total_words += words
        result['word_count'] = total_words
        return result


