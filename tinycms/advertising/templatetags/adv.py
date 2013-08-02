import time
import datetime

from django.template import Library

from tinycms.advertising.models import Advertising

register = Library()

@register.assignment_tag
def get_ad(name="", *args, **kwargs):
    if not name:
        return ""

    try:
        ad = Advertising.objects.get(identifier=name, active=True)
    except Advertising.ObjectDoesNotExist:
        return ""

    now = datetime.datetime.now()

    if ad.start_date and ad.start_date >= now:
        return ""

    if ad.end_date and ad.end_date < now:
        return ""

    if ad.code:
        return ad.code

    if ad.image and ad.link:
        return '<a href="%s" title="%s" target="_blank"><img src="%s" title="%s" /></a>' % (ad.link, ad.title, ad.image.url, ad.title)
