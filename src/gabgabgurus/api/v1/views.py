from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("Hello from API v1!")
