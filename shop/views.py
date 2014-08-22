from django.http import HttpResponse


def home(request):
    return HttpResponse('<html>My Icecream Shop</html>')