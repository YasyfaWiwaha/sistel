from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection, DatabaseError
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

def daftar_reservasi_hotel(request):
    if request.method == 'GET':
        print('Minta daftar reservasi hotel')
        print(request.session['akun_pengguna'])

        #Fetch data reservasi hotel
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sistel.reservation_room")
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
            cursor.execute("SELECT * FROM sistel.reservation_room WHERE id ='{}'".format(pk))
            columns = [col[0] for col in cursor.description]

            data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            rsv_id = data[0]['rsv_id']
            rnum = data[0]['rnum']
            isactive = data[0]['isactive']

            context = {'rsv_id': rsv_id, 'rnum': rnum, 'isactive': isactive}

            print(context)
        return render(request, 'form_update_reservasi_hotel', context)
    
    elif request.method == 'POST':
        print('Status Update Submitted')
        print(request.session['akun_pengguna'])

        isactive = request.POST.get('isactive')

        print(request.POST)

        with connection.cursor() as cursor:
            cursor.execute("UPDATE sistel.reservation_room SET isactive = '{}'".format(pk))
            columns = [col[0] for col in cursor.description]

            data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            rsv_id = data[0]['rsv_id']
            rnum = data[0]['rnum']
            isactive = data[0]['isactive']

            try:
                cursor.execute("UPDATE sistel.reservation_room set isactive ='{}'".format(isactive,pk))
            except DatabaseError as e:
                print(e)
                msg = "Terjadi error Pastikan Data telah diubah"
                context = {'msg': msg, 'id': pk, 'rsv_id': rsv_id, 'rnum': rnum, 'isactive': isactive}
                print(context)
                return render(request, 'form_update_reservasi_hotel.html', context)

        return redirect('ungu:daftar_reservasi_hotel')
