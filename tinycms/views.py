import time
import datetime
import os
import hashlib

from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, RequestContext
from django.db.models.fields import DateTimeField
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from conf import settings as tinycms_settings
from models import Category, EntryBase, Article, Video, Media, Link

def home(request, template_name=tinycms_settings.TEMPLATE_DEFAULT+"/home.html"):
    active = 1
    links = Link.objects.filter(active=True)
    context = RequestContext(request)
    
    return render_to_response(template_name, locals(), context)

def category_detail(request, slugs, tree_id=1, template_name=tinycms_settings.TEMPLATE_DEFAULT+"/category_list.html"):
    slugs = slugs.split('/')
    top_level = 1
    i = 0

    top_category = get_object_or_404(Category, slug__exact=slugs[0], level=top_level, active=True, tree_id=tree_id)
    slugs.pop(0)
    c = top_category

    for slug in slugs:
        try:
            c, = c.get_children().filter(slug__exact=slug, active=True)
        except:
            raise Http404

    if c.url:
        return HttpResponseRedirect(c.url)

    if c.template:
        template_name = "default/%s" % c.template
    entries = EntryBase.objects.filter(publish=True, category__lft__gte=c.lft, category__rght__lte=c.rght)
    entries_sub = c.sub_category.all()
    if entries_sub:
        entries = entries | entries_sub
    entries = entries.order_by('-pub_date')

    active = c.pk
    c_siblings  = c.get_siblings(include_self=True).filter(active=True)
    c_ancestors = c.get_ancestors(ascending=False, include_self=False).filter(active=True)
    c_children  = c.get_children().filter(active=True)

    return render_to_response(template_name,
                              locals(),
                              context_instance=RequestContext(request))

def entry_detail(request, year, month, day, hour, 
        entry_id, date_field='pub_date', 
        template_name=None, template_object_name='object', 
        allow_future=False, page=1, ):

    if not int(entry_id):   
        raise Http404

    entry = get_object_or_404(EntryBase, pk=entry_id)
    print entry.classname
    print globals()
    getclass = globals()[entry.classname]
    queryset = getclass.objects.filter(publish=True)

    page = request.GET.get("page")
    u = request.get_full_path().split('?')
    url_clean = u[0]
    if not page:
        page = 1
    else:
        page = int(page)

    try:
        tt = time.strptime('%s-%s-%s-%s' % (year, month, day, hour),
                           '%s-%s-%s-%s' % ('%Y', '%m', '%d', '%H'))
        dt = datetime.datetime(*tt[:4])
    except ValueError:
        raise Http404

    now = datetime.datetime.now()
    model = queryset.model

    if isinstance(model._meta.get_field(date_field), DateTimeField):
        lookup_kwargs = {'%s__range' % date_field: (dt, dt+datetime.timedelta(hours=1))}
    else:
        lookup_kwargs = {date_field: dt}

    if dt >= now and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now

    lookup_kwargs['%s__exact' % 'pk'] = int(entry_id)

    try:
        obj = queryset.get(**lookup_kwargs)
    except ObjectDoesNotExist:
        raise Http404("No %s found for" % model._meta.verbose_name)

    if page == 1:
        obj.hit.hit += 1
        obj.hit.save()

    if obj.jump and obj.jump_to_url:
        return HttpResponseRedirect(obj.jump_to_url)

    if obj.template:
        template_name = obj.template

    if obj.classname == 'Article':
        split_string = "<!-- pagebreak -->"
        content = obj.content.split(split_string.decode('utf8'))

        if not template_name:
            template_name = tinycms_settings.TEMPLATE_DEFAULT + "/article_detail.html"

        if page > len(content):
            raise Http404

        obj.content = content[page-1]

        if len(content) > 1:
            multi_pages = 1

            pagelist_html = "<ul>"
            if page != 1:
                pagelist_html += "<li class=\"ptext\"><a href=\"%s?page=%s\">" % (url_clean, page-1) + unicode(_("prev")) + "</a></li>"
            for i in range(1, len(content)+1):
                if page == i:
                    pagelist_html += "<li class=\"pc\">%s</li>" % i
                else:
                    pagelist_html += "<li><a href=\"%s?page=%i\">%s</a></li>" % (url_clean, i, i)

            if page != len(content):
                pagelist_html += "<li class=\"ptext\"><a href=\"%s?page=%s\">" % (url_clean, page+1) + unicode(_("next")) + "</a></li>"
            pagelist_html += "</ul>"

    elif obj.classname == 'Video':
        if not template_name:
            template_name = tinycms_settings.TEMPLATE_DEFAULT + "/video_detail.html"

    c_ancestors = obj.category.get_ancestors(ascending=False, include_self=True)
    c_top, = c_ancestors.filter(level=1)
    c_menu = obj.category.get_siblings(include_self=True)

    return render_to_response(template_name,
                              locals(),
                              context_instance=RequestContext(request, {
                                  template_object_name: obj,
                              }))

def preview_entries(request, entry_id, template_name=None, template_object_name='object'):
    if not request.user.is_authenticated():
        raise Http404

    entry = get_object_or_404(EntryBase, pk=entry_id)
    getclass = globals()[entry.classname]
    queryset = getclass.objects.all()

    obj = queryset.get(pk=entry_id)

    if obj.classname == 'Article':
        if not template_name:
            template_name = tinycms_settings.TEMPLATE_DEFAULT + "/article_detail_preview.html"
    elif obj.classname == 'Video':
        if not template_name:
            template_name = tinycms_settings.TEMPLATE_DEFAULT + "/video_detail_preview.html"

    c_ancestors = obj.category.get_ancestors(ascending=False, include_self=True)
    c_top, = c_ancestors.filter(level=1)
    c_menu = obj.category.get_siblings(include_self=True)

    return render_to_response(template_name,
                              locals(),
                              context_instance=RequestContext(request, {
                                  template_object_name: obj,
                              }))

@login_required
def upload_page(request, extra_context=None):
    csrf_token = get_token(request)
    session_id = request.session.session_key
    context = RequestContext(request)

    template_name = "upload_image.html"
    return render_to_response(template_name, locals(), context)

@csrf_exempt
@login_required
def upload(request):
    if request.method == 'POST':
        for field_name in request.FILES:
            uploaded_file = request.FILES[field_name]

            datedir = time.strftime('/%Y/%m/%d/', time.localtime(time.time()))
            destination_dir = settings.MEDIA_ROOT + 'images' + datedir
            url_path = settings.MEDIA_URL + 'images' + datedir

            if not os.path.exists(str(destination_dir)):
                os.makedirs(str(destination_dir))

            salt = str(time.time()) + uploaded_file.name
            if isinstance(salt, unicode):
                salt = salt.encode('utf8')
            filename = hashlib.md5(salt).hexdigest()

            fn_ext = uploaded_file.name.split('.')[-1]
            destination_path = destination_dir + filename + '.' + fn_ext
            url_path = url_path + filename + '.' + fn_ext

            destination = open(str(destination_path), 'wb+')

            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()

        media = Media()
        media.title = uploaded_file
        media.uploader = request.user
        media.image = 'images' + datedir + filename + '.' + fn_ext
        media.save()

        return HttpResponse(url_path, mimetype="text/plain")
    else:
        raise Http404
