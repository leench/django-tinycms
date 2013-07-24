import re
import time
import datetime
from itertools import chain

from django import template
from django.template import Library
from django.db.models import Q
from django.conf import settings

from tinycms.models import Category, Article, Video, EntryBase

register = Library()

@register.assignment_tag
def get_entries_list(cid="1", num=1, frm=0, symbols="", children=True, cls="", obj=EntryBase, *args, **kwargs):
    if settings.DEBUG:
        st = time.time()
    cid = str(cid)
    clist = cid.split(",")
    #now = datetime.datetime.now()
    entries = obj.objects.filter(pk__lt=0)
    all_entries = {}
    if children:
        for cpk in clist:
            c = Category.objects.get(pk=cpk)
            #entries = EntryBase.objects.filter(publish=True, category__lft__gte=c.lft, category__rght__lte=c.rght, category__tree_id=c.tree_id)
            #entries_sub = EntryBase.objects.filter(publish=True, sub_category__lft__gte=c.lft, sub_category__rght__lte=c.rght, sub_category__tree_id=c.tree_id)
            all_entries[cpk] = obj.objects.filter(
                Q(publish=True) & (
                    ( Q(category__lft__gte=c.lft) & Q(category__rght__lte=c.rght) & Q(category__tree_id=c.tree_id) ) | 
                    ( Q(sub_category__lft__gte=c.lft) & Q(sub_category__rght__lte=c.rght) & Q(sub_category__tree_id=c.tree_id) )
                ) #& Q(pub_date__lte=now)
            )
    else:
        for cpk in clist:
            #entries = EntryBase.objects.filter(publish=True, category__pk=cid)
            #entries_sub = EntryBase.objects.filter(publish=True, sub_category__pk=cid)
            all_entries = obj.objects.filter(
                Q(publish=True) &
                ( Q(category__pk=cpk) | Q(sub_category__pk=cpk) )
                #& Q(pub_date__lte=now)
            )

    for (k, v) in all_entries.items():
        entries = entries | v
    #if entries_sub:
        #entries = Q(list(chain(entries, entries_sub)))
        #entries = entries | entries_sub

    if symbols != "":
        symbollist = symbols.split(',')
        for symbol in symbollist:
            entries = entries.filter(symbol__symbol=re.findall(r'\w+', symbol)[0])

    if cls:
        entries = entries.filter(classname=cls)

    entries = entries.order_by('-pub_date')[frm:num+frm]
    if settings.DEBUG:
        print "get_entries_list Timer: %fs" % (time.time() - st)
    return entries

@register.assignment_tag
def get_hot_entries(cid, num=1, frm=0, days=0, children=True, *args, **kwargs):
    if children:
        c = Category.objects.get(pk=cid)
        entries = EntryBase.objects.filter(publish=True, category__lft__gte=c.lft, category__rght__lte=c.rght)
    else:
        entries = EntryBase.objects.filter(publish=True, category__pk=cid)

    if days:
        entries = entries.filter(pub_date__gte=datetime.datetime.now()-datetime.timedelta(days))

    entries = entries.order_by('-hit__hit')[frm:num+frm]
    return entries

@register.assignment_tag
def get_random_entries(cid, num=1, days=0, children=True, symbols="", *args, **kwargs):
    if children:
        c = Category.objects.get(pk=cid)
        entries = EntryBase.objects.filter(publish=True, category__lft__gte=c.lft, category__rght__lte=c.rght)
    else:
        entries = EntryBase.objects.filter(publish=True, category__pk=cid)

    if days:
        entries = entries.filter(pub_date__gte=datetime.datetime.now()-datetime.timedelta(days))

    if symbols != "":
        symbollist = symbols.split(',')
        for symbol in symbollist:
            entries = entries.filter(symbol__symbol=re.findall(r'\w+', symbol)[0])

    entries = entries.order_by('?')[:num]
    return entries
