from django.shortcuts import render, redirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest
from .forms import SearchForm,ReviewForm

# Create your views here.
@csrf_exempt
def hotel(request):

    if request.method == 'GET':
        with connection.cursor() as cursor: 
            cursor.execute("SELECT hotel_name, rating FROM sistel.hotel")
            columns = [col[0] for col in cursor.description]
            data = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                    ]
            context = {'data': data}
            return render(request, 'hotels.html', context)
     
    elif request.method =='POST':
        min_price = request.POST['min_price']
        max_price = request.POST['max_price']
        with connection.cursor() as cursor: 
            cursor.execute("SELECT DISTINCT hotel_name FROM sistel.room WHERE price >= '{}' AND price <= '{}'".format(min_price, max_price))
            # columns = [col[0] for col in cursor.description]
            # data = [
            #         dict(zip(columns, row))
            #         for row in cursor.fetchall()
            #         ]
            data = cursor.fetchall()

            fetched_data = []
            for hotel in data:
                print(hotel[0])
                hotel_name = hotel[0]
                cursor.execute("SELECT * FROM sistel.hotel WHERE hotel_name = '{}'".format(hotel_name))
                result = cursor.fetchone()  
                if result:
                    fetched_data.append(result)
            print(fetched_data)
            
            if fetched_data: 
                right_wrong = True 
            else: 
                right_wrong = False
            context = {}
            context['fetched_data'] = fetched_data
            context['right_wrong'] = right_wrong    
            return render(request, 'hotels.html', context)
    

def review(request: HttpRequest):
    form = ReviewForm()
    
    return render(request,"review.html",{"title": "Review","form": form})