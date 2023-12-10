from django.shortcuts import render
from django.http import HttpRequest
from application.decorators import _login_required
from .forms import ComplaintForm

# Create your views here.

@_login_required
def dashboard(request: HttpRequest):
    return render(request,"dashboard.html",{"title": "dashboard user"})

def complaint(request: HttpRequest):
    form = ComplaintForm()
    
    return render(request,"complaint.html",{"title": "Complaint","form": form})
