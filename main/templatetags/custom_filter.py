from django import template
register = template.Library()

@register.filter
def first_letters(value):
    """
    Extracts the first letter of each word in the input string.
    """
    value = str(value)
    return ''.join([word[0] for word in value.split() if word]).upper()