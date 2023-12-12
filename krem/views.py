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

def reservation_list(request: HttpRequest):
    email = request.session["akun_pengguna"].get("email",None)

    cursor = connection.cursor()
    sql = f"select * from sistel.reservation inner join sistel.reservation_room on sistel.reservation.r_id = sistel.reservation_room.rsv_id where sistel.reservation.cust_email = '{email}';   "
    cursor.execute(sql)
    
    reservation_data = dictfetchall(cursor)

    return render(request,"reservation_list.html",{"title": "Reservation list","reservation_data": reservation_data})

def reservation_detail(request: HttpRequest,id):
    cursor = connection.cursor()
    sql = f"select * from sistel.reservation_room where rsv_id='{id}'"
    cursor.execute(sql)
    reservation_data = dictfetchall(cursor)[0]
    
    sql = f"select * from sistel.RESERVATION_SHUTTLESERVICE"
    cursor.execute(sql)
    reservation_shuttle = dictfetchall(cursor)[0] if len(dictfetchall(cursor)) > 0 else {}

    return render(request,"reservation_details.html",{"title": "Reservation detail",**reservation_data,**reservation_shuttle})

def reservation_cancel(request: HttpRequest,id):
    cursor = connection.cursor()
    sql = f"update sistel.reservation_room set  isactive=false where rsv_id='{id}'"
    cursor.execute(sql)
    return redirect("reservationlist")