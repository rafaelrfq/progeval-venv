from django import template

register = template.Library()

@register.filter
def calificativo(total):
    if 90 <= total <= 100:
            return 'Excelente'
    elif 80 <= total < 90:
        return 'Muy Bueno'
    elif 70 <= total < 80:
        return 'Bueno'
    elif 60 <= total < 70:
        return 'Suficiente'
    elif total < 60:
        return 'Insuficiente'