from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .forms import *

def index(request):
    if(request.session['akun_pengguna']['is_hotel']):
        response = {}
        email = request.session['akun_pengguna']['email']

        with connection.cursor() as c:
            c.execute(f"SELECT hotel_name, hotel_branch FROM sistel.HOTEL WHERE email ='{email}'")
            hotel = c.fetchall()
            hotel_name = hotel[0][0]
            hotel_branch = hotel[0][1]

        with connection.cursor() as c:
            c.execute(f"SELECT * FROM sistel.ROOM WHERE hotel_name = '{hotel_name}' AND hotel_branch = '{hotel_branch}'")
            response['rooms'] = c.fetchall()

        return render(request, 'index_kamar.html', response)

    return HttpResponseRedirect(reverse('main:show_login'))



def add_room(request):
    if(request.session['akun_pengguna']['is_hotel']):
        if (request.method == "POST"):
            form = CreateRoomForm(request.POST)
            if form.is_valid():
                with connection.cursor() as c:
                    # Get hotel data from user's session
                    email = request.session['akun_pengguna']['email']
                    c.execute(f"SELECT hotel_name, hotel_branch FROM sistel.HOTEL WHERE email ='{email}'")
                    hotel = c.fetchall()

                    hotel_name = hotel[0][0]
                    hotel_branch = hotel[0][1]
                    room_number = request.POST['nomor_kamar']
                    price = request.POST['harga']
                    floor = request.POST['lantai']

                    c.execute(f"INSERT INTO sistel.ROOM VALUES ('{hotel_name}', '{hotel_branch}', '{room_number}', {price}, {floor})")
                
                return redirect("/room/")
        form = CreateRoomForm()
        response = {}
        response['room_form'] = form
        return render(request, 'create_kamar.html', response)
    return redirect("")




def update_room(request, room_number):
    if(request.session['akun_pengguna']['is_hotel']):
        # Get hotel data from user's session
        email = request.session['akun_pengguna']['email']
        with connection.cursor() as c:
            c.execute(f"SELECT hotel_name, hotel_branch FROM sistel.HOTEL WHERE email ='{email}'")
            hotel = c.fetchall()
            hotel_name = hotel[0][0]
            hotel_branch = hotel[0][1]
            if (request.method == "POST"):
                form = UpdateRoomForm(request.POST)
                if form.is_valid():
                    price = request.POST['harga']
                    floor = request.POST['lantai']
                    c.execute(f"UPDATE sistel.ROOM SET price = {price}, floor = {floor} WHERE hotel_name = '{hotel_name}' AND hotel_branch = '{hotel_branch}' AND room_number = '{room_number}'")
                    return redirect("/room/")
            

            data = {}
            response = {}
            c.execute(f"SELECT * FROM sistel.ROOM WHERE hotel_name = '{hotel_name}' AND hotel_branch = '{hotel_branch}' AND room_number = '{room_number}'")
            room = c.fetchone()
            data['room_number'] = room[2]
            data['price'] = room[2]
            data['floor'] = room[2]

            form = UpdateRoomForm(data)

            response['room_form'] = form
            response['room_number'] = room_number
            return render(request, 'update_kamar.html', response)
    return redirect("")

def delete_room(request, room_number):
    with connection.cursor() as c:
        email = request.session['akun_pengguna']['email']
        c.execute(f"SELECT hotel_name, hotel_branch FROM sistel.HOTEL WHERE email ='{email}'")
        hotel = c.fetchall()

        hotel_name = hotel[0][0]
        hotel_branch = hotel[0][1]
        c.execute(f"DELETE FROM sistel.ROOM R WHERE R.hotel_name = '{hotel_name}' AND R.hotel_branch = '{hotel_branch}' AND R.room_number = '{room_number}'")
    return redirect("/room/")

