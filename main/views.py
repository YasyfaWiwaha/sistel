from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection, DatabaseError
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

import json

# Class USER
class User:
    def __init__(self, email, is_hotel, is_customer):
        self.email = email
        self.is_hotel = is_hotel
        self.is_customer = is_customer

    def getJson(self):
        return {
            'email': self.email,
            'is_hotel': self.is_hotel,
            'is_customer': self.is_customer,
        }
    
def setLoginSession(request, email):
    user = None
    isHotel = True
    isCustomer = True
    cursor = connection.cursor()

    #Get email
    cursor.execute("select * from sistel.user where email = '{}'".format(email))

    row = cursor.fetchone()
    email = row[0]

    # Cek if hotel
    cursor.execute("select * from sistel.hotel where email = '{}'".format(email))

    row = cursor.fetchone()

    if row == None: isHotel = False

    # Cek if customer
    cursor.execute("select * from sistel.customer where email = '{}'".format(email))

    row = cursor.fetchone()

    if row == None: isCustomer = False

    # Cek cek

    if isHotel:
        user = User(email, True, False)

    if isCustomer:
        user = User(email, False, True)
    
    if user:
        request.session['akun_pengguna'] = user.getJson()
@csrf_exempt
def show_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('password')
        with connection.cursor() as cursor:
            try:
                cursor.execute("select * from sistel.user where email = '{}'".format(email))

                row = cursor.fetchall()


                password  = row[0][1]
                if password != passw: raise Exception

                setLoginSession(request, email)

                if(request.session['akun_pengguna']['is_customer']):
                    print("hello")
                    return redirect('pink:hotel')

            except Exception as e:
                print(e)
                msg = "Terjadi error! Pastikan anda sudah mendaftar dan memasukkan email serta password yang benar"
                context = {'msg': msg}
                return render(request, 'login.html', context)

    return render(request, "login.html")

@csrf_exempt
def logout(request):
    request.session.flush()
    return redirect("main:show_login")

def show_register(request):
    return render(request, "register.html")

@csrf_exempt
def show_register_hotel(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        nohp =request.POST.get('notelp')
        hname =request.POST.get('hname')
        hbranch =request.POST.get('hbranch')
        nib =request.POST.get('nib')
        street =request.POST.get('jalan')
        district =request.POST.get('kecamatan')
        city =request.POST.get('kota')
        province =request.POST.get('provinsi')
        rating = 0
        with connection.cursor() as cursor:
            try:
                cursor.execute("insert into sistel.user values ('{}','{}','{}', '{}') "
                                               .format(email, password,fname,lname))
                cursor.execute("insert into sistel.reservation_actor values ('{}','{}') "
                    .format(email,nohp))
                cursor.execute("insert into sistel.hotel values ('{}','{}','{}', '{}', '{}', '{}', '{}', '{}', '{}') "
                    .format(email, hname, hbranch, nib, rating, street, district, city, province))
            except DatabaseError as e:
                print(e)
                msg = "Terjadi error! Pastikan semua sudah sesuai ketentuan"
                context = {'msg': msg}
                return render(request, 'registerHotel.html', context)

        setLoginSession(request, email)
        return redirect('main:show_login')

    return render(request, "registerHotel.html")

@csrf_exempt
def show_register_customer(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        nohp = request.POST.get('nohp')
        nik = request.POST.get('nik')

        with connection.cursor() as cursor:
            try:
                cursor.execute("insert into sistel.user values ('{}','{}','{}', '{}') "
                    .format(email,password,fname,lname))
                cursor.execute("insert into sistel.reservation_actor values ('{}','{}') "
                    .format(email,nohp))
                cursor.execute("insert into sistel.customer values ('{}','{}') "
                    .format(email,nik))
            except DatabaseError as e:
                print(e)
                msg = "Terjadi error! Pastikan semua sudah sesuai ketentuan"
                context = {'msg': msg}
                return render(request, 'registerCustomer.html', context)

        setLoginSession(request, email)
        return redirect('main:show_login')
    return render(request, "registerCustomer.html")