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
