from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.db import connection
from .forms import ComplaintForm

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Create your views here.

def dashboard(request: HttpRequest):
    
    email = request.session["akun_pengguna"].get("email",None)
    is_hotel = request.session["akun_pengguna"].get("is_hotel",False)

    cursor = connection.cursor()
    
    sql = f"""
    select *
    from sistel.user_acc
    inner join sistel.customer
    on user_acc.email = customer.email
    where user_acc.email = '{email.lower()}';
    """
    
    if is_hotel:
        sql = f"""
        select *
        from sistel.user_acc
        inner join sistel.hotel
        on user_acc.email = hotel.email
        where user_acc.email = '{email.lower()}';
        """

    cursor.execute(sql)
    user_data = dictfetchall(cursor)[0]

    return render(request,"dashboard.html",{"title": "dashboard user",**user_data})

def complaint(request: HttpRequest,id):
    form = ComplaintForm()
    cursor = connection.cursor()
    email = request.session["akun_pengguna"].get("email",None)
    
    if request.method == "POST":
        if form.is_valid():
            hotel_name = form.cleaned_data["hotel_name"]
            hotel_chapter = form.cleaned_data["hotel_chapter"]
            description = form.cleaned_data["description"]

            sql =f"""
                INSERT INTO complaint (
                    id,
                    cust_email,
                    rv_id,
                    COMPLAINT TEXT
                ) VALUES (
                    12345,
                    '{email}',
                    {id},
                    '{description}'
                );
                """
            try:
                cursor.execute(sql)
            except Exception as e:
                print(e)
            else:
                return redirect("dashboard")


            return redirect("dashboard")
    
    return render(request,"complaint.html",{"title": "Complaint","form": form})
