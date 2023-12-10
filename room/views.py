from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .forms import *

def index(request):
    if(request.session['akun_pengguna']['is_hotel']):
        response = {}
        with connection.cursor() as c:
            c.execute('SELECT * FROM ROOM')
            response['rooms'] = c.fetchall()
        return render(request, 'index_kamar.html', response)

    return HttpResponseRedirect(reverse('main:show_login'))



def add_room(request):
    if(request.session['akun_pengguna']['is_hotel']):
        if (request.method == "POST"):
            form = CreateRoomForm(request.POST)
            if form.is_valid():
                with connection.cursor() as c:
                    room_number = request.POST['nomor_kamar']
                    price = request.POST['harga']
                    floor = request.POST['lantai']





def update_room(request):
    response = {}
    return render(request, 'update_kamar.html', response)

def delete_room(request):
    response = {}
    return render(request, 'index_kamar.html', response)
