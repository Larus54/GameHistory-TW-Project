from django.http import HttpResponseNotAllowed
from django.shortcuts import render


# per pagine errore 405
def handle_405(get_response):
    def middleware(request):
        response = get_response(request)
        if isinstance(response, HttpResponseNotAllowed):
            return render(request, 'error/405.html')
        return response
    return middleware


# Per pagine errore 404
class NotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, 'error/404.html')
        return response

# Per pagine errore 403
class ForbiddenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 403:
            return render(request, 'error/403.html')
        return response