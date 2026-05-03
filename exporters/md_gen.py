import os
from django.conf import settings
from django.utils.text import slugify


def generate_markdown(instance):
    """
    Tactic 6: Transforms payload_output into a .md file.

    Filename format: YYYYMMDD_tool-slug_instance-id.md
    """
    filename = f"{instance.submitted_at.strftime('%Y%m%d')}_{slugify(instance.tool_slug)}_{instance.id}.md"
    relative_path = os.path.join('archives/md/', filename)
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    content = [
        f"# {instance.tool_slug.replace('-', ' ').title()}",
        f"**Date:** {instance.submitted_at.strftime('%Y-%m-%d %H:%M')}",
        f"**Tool Version:** {instance.tool_version}",
        "\n--- \n",
        "## Results",
    ]

    for key, value in instance.payload_output.items():
        label = key.replace('_', ' ').title()
        content.append(f"### {label}\n{value}\n")

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))

    return relative_path


def generate_session_markdown(session):
    """Combine every participant's response into one Markdown file."""
    closed_stamp = (session.closed_at or session.created_at).strftime('%Y%m%d')
    filename = f"{closed_stamp}_{slugify(session.tool_slug)}_session_{session.id}.md"
    relative_path = os.path.join('archives/md/', filename)
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    title = session.tool_slug.replace('-', ' ').title()
    closed_at_str = session.closed_at.strftime('%Y-%m-%d %H:%M') if session.closed_at else '-'
    content = [
        f"# {title} — Combined Session Results",
        f"**Hosted by:** {session.host.email}",
        f"**Closed at:** {closed_at_str}",
        f"**Tool version:** {session.tool_version}",
        "\n---\n",
    ]

    # order_by('submitted_at', 'created_at'): participants who submitted are
    # sorted by submission time; unsubmitted (empty) entries fall back to
    # creation order so they appear last but still in a deterministic sequence.
    instances = session.instances.select_related('user').order_by('submitted_at', 'created_at')
    for inst in instances:
        marker = ' (host)' if inst.user_id == session.host_id else ''
        content.append(f"## {inst.user.email}{marker}")
        if inst.payload_output:
            for key, value in inst.payload_output.items():
                label = key.replace('_', ' ').title()
                content.append(f"### {label}\n{value}\n")
        else:
            content.append("*No response submitted.*\n")
        content.append("---\n")

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))

    return relative_path
