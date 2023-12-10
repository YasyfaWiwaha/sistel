from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection, DatabaseError
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


