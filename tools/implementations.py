from .interface import BaseTool


class SummarizerTool(BaseTool):
    name = 'Quick Summarizer'
    description = 'Trims long text into a punchy summary.'
    version = '1.1'

    def validate(self):
        text = self.user_input.get('raw_text', '')
        if len(text) < 10:
            self.errors['raw_text'] = 'Text is too short to summarize.'

    def process(self):
        text = self.user_input.get('raw_text', '')
        summary = text[:100] + ('...' if len(text) > 100 else '')
        return {
            'summary': summary,
            'word_count': len(text.split()),
        }


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


class DataCleanerTool(BaseTool):
    name = 'CSV Data Sanitizer'
    description = 'Removes duplicate rows from raw CSV input.'
    version = '1.0'

    def validate(self):
        if not self.user_input.get('csv_data'):
            self.errors['csv_data'] = 'CSV data is required.'

    def process(self):
        rows = [r for r in self.user_input.get('csv_data', '').splitlines() if r.strip()]
        unique = list(dict.fromkeys(rows))
        return {
            'cleaned_rows': unique,
            'duplicates_removed': len(rows) - len(unique),
        }
