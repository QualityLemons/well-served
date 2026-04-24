# tools/registry.py

TOOL_CATALOG = {
    'summarizer': {
        'class': 'tools.implementations.SummarizerTool',
        'title': 'Quick Summarizer',
        'icon': 'align-left',
        'category': 'Writing',
        # Tactic 3: How-to and Example content
        'how_to': ("Enter long-form text or report data. The tool will extract "
                   "the core narrative and provide a punchy summary."),
        'example_input': {
            'raw_text': "The quarterly results showed a 15% increase in user retention, primarily driven by the new onboarding flow..."
        },
        # Metadata for Tactic 6 (File naming/Headers)
        'display_fields': ['summary', 'word_count']
    },
    'data-cleaner': {
        'class': 'tools.implementations.DataCleanerTool',
        'title': 'CSV Data Sanitizer',
        'icon': 'database',
        'category': 'Data',
        'how_to': "Upload raw comma-separated values to remove duplicates and fix formatting issues.",
        'example_input': {
            'csv_data': "name,email\nJohn,john@example.com\nJohn,john@example.com"
        },
        'display_fields': ['cleaned_rows', 'duplicates_removed']
    }
}

def get_tool_instance(slug, input_data=None):
    """Helper to fetch and initialize a tool by its slug."""
    tool_info = TOOL_CATALOG.get(slug)
    if not tool_info:
        return None
    
    # Logic to dynamically import and instantiate the class
    # (Simplified for this blueprint)
    return SummarizerTool(user_input=input_data)