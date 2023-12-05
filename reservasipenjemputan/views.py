from django.shortcuts import render
from django.db import connection, DatabaseError
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def reservasipenjemputan(request):
    return render(request, "reservasi_penjemputan,html")