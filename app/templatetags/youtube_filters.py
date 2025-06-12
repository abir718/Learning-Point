from django import template
import re
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_id(url):
    """
    Extract YouTube video ID from a full YouTube URL.
    Supports various YouTube URL formats.
    """
    if not url:
        return ""

    # Try parsing from query string (e.g., watch?v=VIDEO_ID)
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if "v" in query_params:
        return query_params["v"][0]

    # Fallback to regex for other formats like youtu.be, embed, shorts, etc.
    match = re.search(r'(youtu\.be/|embed/|shorts/|v/|watch\?v=|watch\?.+&v=)([^&#?/]{11})', url)
    if match:
        return match.group(2)

    # Last fallback: search for any 11-character video ID in the URL
    match = re.search(r'([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else ""
