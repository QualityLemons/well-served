# tools/registry.py

TOOL_CATALOG = {
    'summarizer': {
        'class': 'tools.implementations.SummarizerTool',
        'title': 'Text Summarizer',
        'icon': 'edit-3',
        'category': 'Writing'
    },
    # Future tools get added here
}

def get_tool_instance(slug, input_data=None):
    """Helper to fetch and initialize a tool by its slug."""
    tool_info = TOOL_CATALOG.get(slug)
    if not tool_info:
        return None
    
    # Logic to dynamically import and instantiate the class
    # (Simplified for this blueprint)
    return SummarizerTool(user_input=input_data)