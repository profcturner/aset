# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader


def index(request):
    '''Main index page for non admin views'''

    template = loader.get_template('index.html')
    context = {
        'home_page': True,
    }
    return HttpResponse(template.render(context, request))


def forbidden(request):
    '''General permissions failure warning'''

    template = loader.get_template('forbidden.html')

    return HttpResponse(template.render({}, request))
