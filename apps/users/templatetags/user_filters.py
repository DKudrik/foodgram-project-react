from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Encode URL with context."""
    query = context['request'].GET.copy()
    if query.get('page') is not None:
        query.pop('page')
    query.update(kwargs)
    return query.urlencode()
