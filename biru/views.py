from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.db import connection
#from application.utils import dictfetchall
from .forms import FacilityForm
from django.views.decorators.csrf import csrf_exempt 

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# Create your views here.
@csrf_exempt

def facility(request: HttpRequest):
    cursor = connection.cursor()
    email = request.session["akun_pengguna"].get("email",None)

    sql = f"select * from sistel.hotel_facilities inner join sistel.hotel on sistel.hotel_facilities.hotel_name = sistel.hotel.hotel_name where sistel.hotel.email= '{email}' "
    cursor.execute(sql)
    facility_data = dictfetchall(cursor)

    return render(request,"facility.html",{"title": "Fasilitas hotel","facility_data": facility_data})
    
def add_facility(request: HttpRequest):
    form = FacilityForm()
    cursor = connection.cursor()
    email = request.session["akun_pengguna"].get("email",None)

    if request.method == "POST":
        form = FacilityForm(request.POST)
        if form.is_valid():
            sql = f"select * from sistel.hotel where email = '{email}'"
            cursor.execute(sql)
            print(email)
            hotel_data = dictfetchall(cursor)[0]
            print(hotel_data)

            hotel_name = hotel_data["hotel_name"]
            hotel_branch = hotel_data["hotel_branch"]
            facility_name = form.cleaned_data["facility_name"]

            sql = f"select * from sistel.hotel_facilities where hotel_name= '{hotel_name}' and hotel_branch= '{hotel_branch}' and facility_name= '{facility_name}'  "
            cursor.execute(sql)
            check_faciltiy = dictfetchall(cursor)
            
            if len(check_faciltiy) > 0:
                print(check_faciltiy)
                return redirect("facility")
            try:
                sql = f"insert into sistel.hotel_facilities(hotel_name,hotel_branch,facility_name) values('{hotel_name}','{hotel_branch}','{facility_name}') "
                cursor.execute(sql)
            except Exception as e:
                print(e)
            print("a")
            return redirect("facility")

    return render(request,"add_facility.html",{"title": "Add facility","form": form})

def delete_facility(request: HttpRequest,facility_name):
    cursor = connection.cursor()
    email = request.session["akun_pengguna"].get("email",None)
    
    sql = f"delete from sistel.hotel_facilities where facility_name = '{facility_name}'"
    cursor.execute(sql)
    
    return redirect("facility")


def update_facility(request: HttpRequest,facility_name):
    form = FacilityForm()
    cursor = connection.cursor()
    email = request.session["akun_pengguna"].get("email",None)

    if request.method == "POST":
        form = FacilityForm(request.POST)
        if form.is_valid():
            sql = f"select * from sistel.hotel where email = '{email}'"
            cursor.execute(sql)
            hotel_data = dictfetchall(cursor)[0]

            hotel_name = hotel_data["hotel_name"]
            hotel_branch = hotel_data["hotel_branch"]
            update_name = form.cleaned_data["facility_name"]

            sql = f"select * from sistel.hotel_facilities where hotel_name= '{hotel_name}' and hotel_branch= '{hotel_branch}' and facility_name= '{update_name}'  "
            cursor.execute(sql)
            check_faciltiy = dictfetchall(cursor)
            
            if len(check_faciltiy) > 0:
                print(check_faciltiy)
                return redirect("facility")
            try:
                print(facility_name)
                sql = f"update sistel.hotel_facilities set facility_name= '{update_name}' where   hotel_name= '{hotel_name}' and hotel_branch= '{hotel_branch}' and facility_name= '{facility_name}' "
                cursor.execute(sql)
            except Exception as e:
                print(e)
            print("a")
            return redirect("facility")

    return render(request,"add_facility.html",{"title": "Update facility","form": form})