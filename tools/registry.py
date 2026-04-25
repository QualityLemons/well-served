from importlib import import_module


TOOL_CATALOG = {
    'summarizer': {
        'class': 'tools.implementations.SummarizerTool',
        'title': 'Quick Summarizer',
        'icon': 'align-left',
        'category': 'Writing',
        'how_to': (
            'Enter long-form text or report data. The tool will extract '
            'the core narrative and provide a punchy summary.'
        ),
        'example_input': {
            'raw_text': (
                'The quarterly results showed a 15% increase in user retention, '
                'primarily driven by the new onboarding flow...'
            ),
        },
        'display_fields': ['summary', 'word_count'],
    },
    'data-cleaner': {
        'class': 'tools.implementations.DataCleanerTool',
        'title': 'CSV Data Sanitizer',
        'icon': 'database',
        'category': 'Data',
        'how_to': 'Upload raw comma-separated values to remove duplicates and fix formatting issues.',
        'example_input': {
            'csv_data': 'name,email\nJohn,john@example.com\nJohn,john@example.com',
        },
        'display_fields': ['cleaned_rows', 'duplicates_removed'],
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
