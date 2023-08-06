from django.http import JsonResponse, HttpResponse

import pyp8s


def IndexView(request):
    pyp8s.MetricsHandler.inc("django_pyp8s_view", 1, view="IndexView")
    return JsonResponse({'application': 'django-pyp8s'})


def VersionView(request):
    pyp8s.MetricsHandler.inc("django_pyp8s_view", 1, view="VersionView")
    return JsonResponse({'version': pyp8s.__version__})


def MetricsView(request):
    pyp8s.MetricsHandler.inc("django_pyp8s_view", 1, view="MetricsView")
    content = pyp8s.MetricsHandler.render()

    return HttpResponse(content)
