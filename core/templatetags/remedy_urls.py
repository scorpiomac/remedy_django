"""Template tags pour résoudre des URLs sans provoquer d'erreur 500 si la vue n'est pas enregistrée."""
from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()


@register.simple_tag
def remedy_url(name, *args, **kwargs):
    """Retourne l'URL pour `name`, ou None si elle n'existe pas (évite NoReverseMatch en production)."""
    try:
        return reverse(name, args=args if args else None, kwargs=kwargs if kwargs else None)
    except NoReverseMatch:
        return None
