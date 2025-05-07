from django.shortcuts import render

# Create your views here.
def register_user(request):
    return render(request, "urappiapp/register_user.html")

def login(request):
    return render(request, "urappiapp/register_user.html")