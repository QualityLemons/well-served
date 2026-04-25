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


