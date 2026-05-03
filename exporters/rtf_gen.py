import os
from django.conf import settings
from django.utils.text import slugify


def _rtf_escape(value):
    """Escape a string for safe inclusion in an RTF document.

    Three substitutions are applied in order:
    1. Backslash (``\\``) — must come first to avoid double-escaping the
       backslashes introduced by later replacements.
    2. Braces (``{`` and ``}``) — RTF uses these as control word delimiters.
    3. Newlines — converted to the RTF line-break sequence ``\\line``.
    """
    return str(value).replace('\\', r'\\').replace('{', r'\{').replace('}', r'\}').replace('\n', r' \line ')


def generate_rtf(instance):
    """
    Tactic 6: Transforms payload_output into a basic .rtf file.

    Filename format: YYYYMMDD_tool-slug_instance-id.rtf
    """
    filename = f"{instance.submitted_at.strftime('%Y%m%d')}_{slugify(instance.tool_slug)}_{instance.id}.rtf"
    relative_path = os.path.join('archives/rtf/', filename)
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # RTF header directives:
    #   \rtf1    — RTF version 1
    #   \ansi    — ANSI character set
    #   \deff0   — default font is font 0 (Arial, defined in \fonttbl)
    #   \fonttbl — font table declaration
    #   \f0\fs24 — select font 0 at 12 pt (RTF uses half-points, so 24 = 12 pt)
    rtf_header = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Arial;}}\f0\fs24 "
    content = [rtf_header]

    content.append(r"\b " + instance.tool_slug.upper() + r"\b0 \line ")
    content.append(f"Date: {instance.submitted_at.strftime('%Y-%m-%d')} \line ")
    content.append(r"\line -------------------------- \line ")

    for key, value in instance.payload_output.items():
        label = key.replace('_', ' ').title()
        content.append(r"\b " + label + r": \b0 \line ")
        content.append(f"{_rtf_escape(value)} \line \line ")

    content.append("}")

    # RTF files use ANSI encoding by default.  The \ansi header directive
    # tells the reader to interpret bytes as ANSI.  No explicit encoding=
    # argument is passed; the platform default (typically UTF-8 on Linux) is
    # used.  Non-ASCII characters are not further escaped here, so callers
    # should ensure input text is limited to ASCII-safe content when strict
    # ANSI compatibility is required.
    with open(full_path, 'w') as f:
        f.write("".join(content))

    return relative_path


def generate_session_rtf(session):
    """Combine every participant's response into one RTF file."""
    closed_stamp = (session.closed_at or session.created_at).strftime('%Y%m%d')
    filename = f"{closed_stamp}_{slugify(session.tool_slug)}_session_{session.id}.rtf"
    relative_path = os.path.join('archives/rtf/', filename)
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    rtf_header = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Arial;}}\f0\fs24 "
    content = [rtf_header]

    title = session.tool_slug.upper() + ' - COMBINED SESSION RESULTS'
    content.append(r"\b " + title + r"\b0 \line ")
    content.append(f"Hosted by: {_rtf_escape(session.host.email)} \line ")
    if session.closed_at:
        content.append(f"Closed at: {session.closed_at.strftime('%Y-%m-%d %H:%M')} \line ")
    content.append(r"\line ========================== \line ")

    instances = session.instances.select_related('user').order_by('submitted_at', 'created_at')
    for inst in instances:
        marker = ' (host)' if inst.user_id == session.host_id else ''
        content.append(r"\b " + _rtf_escape(inst.user.email + marker) + r"\b0 \line ")
        if inst.payload_output:
            for key, value in inst.payload_output.items():
                label = key.replace('_', ' ').title()
                content.append(r"\b " + label + r": \b0 \line ")
                content.append(f"{_rtf_escape(value)} \line ")
        else:
            content.append(r"\i No response submitted. \i0 \line ")
        content.append(r"\line -------------------------- \line ")

    content.append("}")

    with open(full_path, 'w') as f:
        f.write("".join(content))

    return relative_path
