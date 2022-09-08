from django.http import HttpResponse
import test


def create_tender(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return HttpResponse("Home")

def test(request):
    test.print_test()
    return HttpResponse("App runned")