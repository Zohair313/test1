from django.shortcuts import render

# All functionality is handled in the Django Admin for this simple project.
def index(request):
    return render(request, 'admin/')
