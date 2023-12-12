from django.shortcuts import render,redirect
from django.http import HttpRequest
from uuid import uuid4
from django.db import connection
from .forms import ReservationForm

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Create your views here.

def reservation(request: HttpRequest,id):
    form = ReservationForm()
    cursor = connection.cursor()
    email = request.session["akun_pengguna"].get("email",None)
    
    sql = f"select * from sistel.room where room_number= '{id}' "
    cursor.execute(sql)

    room_value = dictfetchall(cursor)[0]
    
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data["check_in"]
            check_out = form.cleaned_data["check_out"]
            rent_period = check_out - check_in
            price = room_value["price"] * rent_period
            sql = f"""
                        INSERT INTO RESERVATION (
                            r_id,
                            total_price,
                            check_in,
                            check_out,
                            payment,
                            cust_email
                        ) VALUES (
                            '{uuid4()}',
                            {price},
                            '{check_in}',
                            '{check_out}',
                            'PAY-001',
                            '{email}'
                            
                        );
                        """
            return redirect("reservation")

    return render(request,"reservation.html",{"title": "Reservation","form": form})

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
    
def reservation_cancel(request: HttpRequest,id):
    cursor = connection.cursor()
    sql = f"update sistel.reservation_room set  isactive=false where rsv_id='{id}'"
    cursor.execute(sql)
    return redirect("daftar_reservasi_customer")
    
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
