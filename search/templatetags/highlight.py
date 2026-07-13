from django import template
from django.utils.safestring import mark_safe
import re

register = template.library()


@register.filter
def highlight(text,word):
    
    if not word:
        return text
    pattern = re.compile(re.escape(word),re.IGHNORECASE)
    
    result = pattern.sub(
        lambda m : f"<mark>{m.group()}</mark>",
        text
    )
    return mark_safe(result)