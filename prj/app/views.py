from django.shortcuts import render

#nas kontroler
def render_about(request): 
    return render(request, 'home.html')

