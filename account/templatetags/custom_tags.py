from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_username(context):
    username = context.request.user.email.split('@')[0]
    return username if context.request.user.is_authenticated else None