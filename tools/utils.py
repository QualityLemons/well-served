from .registry import TOOL_CATALOG


def _normalize_meta(slug, meta):
    """Return a copy of meta with guaranteed keys so templates never see missing vars."""
    if meta is None:
        return None
    m = dict(meta)
    m['slug'] = slug
    # Ensure both 'how' and 'how_to' exist so templates can reference either safely.
    m.setdefault('how', m.get('how_to', ''))
    m.setdefault('how_to', m.get('how', ''))
    m.setdefault('what', '')
    m.setdefault('why', '')
    m.setdefault('tagline', '')
    m.setdefault('show_canvas', False)
    m.setdefault('phases', None)
    return m


def get_tool_metadata(slug):
    """Fetches full metadata for a tool, including how-to and examples."""
    return _normalize_meta(slug, TOOL_CATALOG.get(slug))

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