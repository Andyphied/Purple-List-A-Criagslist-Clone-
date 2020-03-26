from django.shortcuts import render

# Create your views here.
def home(request):
    return render (request, template_name='base.html')

def new_search(request):
    return render (request, template_name='my_app/new_search.html')