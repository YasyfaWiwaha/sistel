from django.shortcuts import render
from django.db import connection, DatabaseError

def reservasipenjemputan(request):
    return render(request, "reservasi_penjemputan.html")