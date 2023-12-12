from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection, DatabaseError
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import timezone

def daftar_reservasi_hotel(request):
    if request.method == 'GET':
        print('Minta daftar reservasi hotel')
        print(request.session['akun_pengguna'])

        #Fetch data reservasi hotel
        with connection.cursor() as cursor:
            cursor.execute("SELECT hotel_name FROM sistel.hotel WHERE email='{}'".format(request.session['akun_pengguna']['email']))
            hname = cursor.fetchone()[0]
            cursor.execute("""SELECT
                           RR.rsv_id,
                           RR.rnum,
                           RR.datetime,
                           RS.stat
                           FROM sistel.reservation_room AS RR
                           JOIN sistel.reservation_status_history AS RSH on RSH.r_id = RR.rsv_id
                           JOIN sistel.reservation_status AS RS on RS.id = RSH.rs_id
                           WHERE rhotelname='{}' ORDER BY rsv_id""".format(hname))
            columns = [col[0] for col in cursor.description]
            data = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            print(data)

            context = {'data': data}

            return render(request, 'daftar_reservasi_hotel.html', context)

@csrf_exempt
def update_reservasi_hotel(request, pk):
    if request.method == 'GET':
        print('Minta update reservasi hotel')
        
        #Fetch data reservasi hotel
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from sistel.reservation_room where rsv_id = '{}'".format(pk))
            data = cursor.fetchone()
            print(data)
            rsv_id = data[0]
            rnum = data[1]
            cursor.execute("SELECT * from sistel.reservation_status")
            columns = [col[0] for col in cursor.description]
            stats = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            print(stats)
            context = {'rsv_id': rsv_id, 'rnum': rnum, 'stats':stats}

        return render(request, 'form_update_reservasi_hotel.html', context)
    
    elif request.method == 'POST':
        print('Status Update Submitted')
        print(request.session['akun_pengguna'])

        status_id = request.POST.get('status')
        print(request.POST)
        print(status_id)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * from sistel.reservation_room where rsv_id = '{}'".format(pk))
            data = cursor.fetchone()
            print(data)
            rsv_id = data[0]
            rnum = data[1]
            cursor.execute("SELECT * from sistel.reservation_status")
            columns = [col[0] for col in cursor.description]
            stats = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE sistel.reservation_status_history set rs_id ='{}' WHERE r_id ='{}'".format(status_id,pk))
        except DatabaseError as e:
                print(e)
                msg = "Terjadi error! Tidak bisa mengubah status"
                context = {'rsv_id': rsv_id, 'rnum': rnum, 'stats':stats, 'msg': msg}
                print(context)
                return render(request, 'form_update_reservasi_hotel.html', context)
        
        return redirect('ungu:daftar_reservasi_hotel')
    
def detail_reservasi_hotel(request,pk):
    print('Minta Detail Reservasi')
    print(pk)
    with connection.cursor() as cursor:
        cursor.execute("""SELECT
                           RR.rsv_id,
                           RR.rnum,
                           RR.rhotelname,
                           RR.rhotelbranch,
                           RR.datetime,
                           RS.stat
                           FROM sistel.reservation_room AS RR
                           JOIN sistel.reservation_status_history AS RSH on RSH.r_id = RR.rsv_id
                           JOIN sistel.reservation_status AS RS on RS.id = RSH.rs_id
                           WHERE rsv_id ='{}'""".format(pk))
        data = cursor.fetchone()
        room_rsv_id = data[0]
        rnum = data[1]
        rhotelname = data[2]
        rhotelbranch = data[3]
        room_datetime = data[4]
        room_isactive = data[5]
        cursor.execute("SELECT * FROM sistel.reservation_shuttleservice WHERE rsv_id='{}'".format(pk))
        shuttle_data = cursor.fetchone()
        if shuttle_data == None:
            shuttle_exists = False
            context ={
                'room_rsv_id': room_rsv_id,
                'rnum': rnum,
                'rhotelname': rhotelname,
                'rhotelbranch': rhotelbranch,
                'room_datetime':room_datetime,
                'room_isactive': room_isactive,
                'shuttle_exists':shuttle_exists
            }
        else:
            shuttle_rsv_id = shuttle_data[0] 
            shuttle_vnum = shuttle_data[1]
            shuttle_phonenum = shuttle_data[2]
            shuttle_datetime = shuttle_data[3]
            shuttle_isactive = shuttle_data[4]
            shuttle_exists = True
            context ={
                'room_rsv_id': room_rsv_id,
                'rnum': rnum,
                'rhotelname': rhotelname,
                'rhotelbranch': rhotelbranch,
                'room_datetime':room_datetime,
                'room_isactive': room_isactive,
                'shuttle_rsv_id':shuttle_rsv_id,
                'shuttle_vnum': shuttle_vnum,
                'shuttle_phonenum': shuttle_phonenum,
                'shuttle_datetime': shuttle_datetime,
                'shuttle_isactive': shuttle_isactive,
                'shuttle_exists':shuttle_exists
            }
        return render(request, 'detail_reservasi_hotel.html', context)
    
def daftar_reservasi_customer(request):
    if request.method == 'GET':
        print('Minta daftar reservasi customer')
        print(request.session['akun_pengguna'])

        #Fetch data reservasi hotel
        with connection.cursor() as cursor:
            cursor.execute("SELECT r_id FROM sistel.reservation WHERE cust_email='{}'".format(request.session['akun_pengguna']['email']))
            r_id = cursor.fetchone()
            if id == None:
                r_id_exists = False
                context = {'r_id_exists': r_id_exists}
            else:
                r_id_exists = True
                cursor.execute("""SELECT
                               RR.rsv_id,
                               RR.rnum,
                               RR.datetime,
                               RS.stat
                               FROM sistel.reservation_room AS RR
                               JOIN sistel.reservation_status_history AS RSH on RSH.r_id = RR.rsv_id
                               JOIN sistel.reservation_status AS RS on RS.id = RSH.rs_id
                               WHERE rsv_id='{}' ORDER BY rsv_id""".format(r_id[0]))
                columns = [col[0] for col in cursor.description]
                data = [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]
                print(data)
                context = {'data': data,'r_id_exists': r_id_exists}

            return render(request, 'daftar_reservasi_customer.html', context)

def update_reservasi_customer(request, pk):
    if request.method == 'GET':
        print('Minta update reservasi customer')
        
        #Fetch data reservasi hotel
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sistel.reservation_room WHERE rsv_id ='{}'".format(pk))
            data = cursor.fetchone()
            print(data)
            rsv_id = data[0]
            rnum = data[1]
            isactive = data[5]

            context = {'rsv_id': rsv_id, 'rnum': rnum, 'isactive': isactive}

            print(context)
        return render(request, 'form_update_reservasi_customer.html', context)
    
    elif request.method == 'POST':
        print('Status Update Submitted')
        print(request.session['akun_pengguna'])

        isactive = request.POST.get('isactive')
        print(request.POST)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE sistel.reservation_room set isactive ='{}' WHERE rsv_id ='{}'".format(isactive,pk))

        return redirect('ungu:daftar_reservasi_customer')

def detail_reservasi_customer(request,pk):
    print('Minta Detail Reservasi')
    print(pk)
    with connection.cursor() as cursor:
        cursor.execute("""SELECT
                           RR.rsv_id,
                           RR.rnum,
                           RR.rhotelname,
                           RR.rhotelbranch,
                           RR.datetime,
                           RS.stat
                           FROM sistel.reservation_room AS RR
                           JOIN sistel.reservation_status_history AS RSH on RSH.r_id = RR.rsv_id
                           JOIN sistel.reservation_status AS RS on RS.id = RSH.rs_id
                           WHERE rsv_id ='{}'""".format(pk))
        data = cursor.fetchone()
        room_rsv_id = data[0]
        rnum = data[1]
        rhotelname = data[2]
        rhotelbranch = data[3]
        room_datetime = data[4]
        room_isactive = data[5]
        cursor.execute("SELECT * FROM sistel.reservation_shuttleservice WHERE rsv_id='{}'".format(pk))
        shuttle_data = cursor.fetchone()
        if shuttle_data == None:
            shuttle_exists = False
            context ={
                'room_rsv_id': room_rsv_id,
                'rnum': rnum,
                'rhotelname': rhotelname,
                'rhotelbranch': rhotelbranch,
                'room_datetime':room_datetime,
                'room_isactive': room_isactive,
                'shuttle_exists':shuttle_exists
            }
        else:
            shuttle_exists = True
            shuttle_rsv_id = shuttle_data[0]
            shuttle_vnum = shuttle_data[1]
            shuttle_phonenum = shuttle_data[2]
            shuttle_datetime = shuttle_data[3]
            shuttle_isactive = shuttle_data[4]
            context ={
                'room_rsv_id': room_rsv_id,
                'rnum': rnum,
                'rhotelname': rhotelname,
                'rhotelbranch': rhotelbranch,
                'room_datetime':room_datetime,
                'room_isactive': room_isactive,
                'shuttle_rsv_id':shuttle_rsv_id,
                'shuttle_vnum': shuttle_vnum,
                'shuttle_phonenum': shuttle_phonenum,
                'shuttle_datetime': shuttle_datetime,
                'shuttle_isactive': shuttle_isactive,
                'shuttle_exists':shuttle_exists
            }
        return render(request, 'detail_reservasi_customer.html', context)

def cancel_reservasi(request,pk):
    pass

def form_buat_reservasi_shuttle(request,pk):
    if request.method == 'GET':
        print('Minta form buat reservasi shuttle')
        print(request.session['akun_pengguna'])
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sistel.reservation_room WHERE rsv_id ='{}'".format(pk))
            data = cursor.fetchone()
            rsv_id = data[0]

            cursor.execute("SELECT * FROM sistel.vehicle")
            columns = [col[0] for col in cursor.description]
            vehicle = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            context ={'rsv_id': rsv_id, 'vehicle': vehicle}
        return render(request, 'form_buat_reservasi_shuttle.html', context)


    elif request.method == 'POST':
        plat_kendaraan = request.POST.get('vehicle')
        print("Mengambil data kendaraan")
        current_datetime = timezone.now()
        isactive = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sistel.reservation_room WHERE rsv_id ='{}'".format(pk))
            data = cursor.fetchone()
            rsv_id = data[0]

            cursor.execute("SELECT * FROM sistel.vehicle")
            columns = [col[0] for col in cursor.description]
            vehicle = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            
            cursor.execute("SELECT driver_phonenum from sistel.shuttle_service where vehicle_platnum ='{}'".format(plat_kendaraan))
            driver_phonenum = cursor.fetchone()[0]
            try:
                cursor.execute("insert into sistel.reservation_shuttleservice values ('{}','{}','{}', '{}','{}') "
                           .format(pk,plat_kendaraan,driver_phonenum,current_datetime,isactive))
            except DatabaseError as e:
                print(e)
                msg = "Terjadi error! Tidak bisa membuat reservasi shuttle"
                context ={'rsv_id': rsv_id, 'vehicle': vehicle, 'msg': msg}
                print(context)
                return render(request, 'form_buat_reservasi_shuttle.html', context)
            
            return redirect('ungu:daftar_reservasi_customer')


