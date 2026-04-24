from .registry import TOOL_CATALOG

def get_tool_metadata(slug):
    """Fetches full metadata for a tool, including how-to and examples."""
    return TOOL_CATALOG.get(slug)

def get_all_tools_by_category():
    """Groups tools for the Catalog view."""
    grouped = {}
    for slug, meta in TOOL_CATALOG.items():
        cat = meta.get('category', 'General')
        if cat not in grouped:
            grouped[cat] = []
        meta['slug'] = slug # Ensure slug is available for URLs
        grouped[cat].append(meta)
    return grouped