
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
import os

def link_callback(uri, rel):

    sUrl=settings.STATIC_URL
    sRoot=settings.STATICFILES_DIRS
    mUrl=settings.MEDIA_URL
    mRoot=settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path=os.path.join(mRoot, uri.replace(mUrl, ''))
    elif uri.startswith(sUrl):
        path=os.path.join(sRoot, uri.replace(sUrl, ''))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception(
            'media url must start with %s or %s ' %(sUrl, mUrl)
        )
    return path

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), result, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None