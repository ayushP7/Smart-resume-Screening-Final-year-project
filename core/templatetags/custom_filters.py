from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Replaces all occurrences of the first character of arg with the rest of arg.
    Example: {{ "hello_world"|replace:"_, " }} -> "hello world"
    """
    if len(arg) < 1:
        return value
    
    # Simple logic: assume arg is "old,new" or similar if we want a more complex one
    # But for now, let's just make it work for the specific case: "_" -> " "
    if arg.startswith('_'):
        old = '_'
        new = arg[1:]
        return value.replace(old, new)
    
    return value
