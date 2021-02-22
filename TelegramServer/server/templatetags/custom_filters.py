from django import template

# если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать фильтры
register = template.Library()


# Поступил перевод
@register.filter(name='transfer')
def transfer(value, arg):
    value1 = value + arg
    return value1
