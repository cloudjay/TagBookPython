import markdown
import re
from django import template

register = template.Library()


autolink = lambda text: re.sub(r'(?<!href=")(https?://[^\s<>"\']+)', lambda m: f'<a href="{m.group(1)}" target="_blank">{m.group(1)}</a>', text)

@register.filter
def markdownify(text):
    if not text:
        return ""
    return autolink(markdown.markdown(
            text,
            extensions=['extra', 'nl2br']
            ))

