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


