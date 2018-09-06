from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from .models import Greeting, Stock, User, UserXStock
import requests
import os, sys

try:
    import config
    account_sid = config.ACCOUNT_SID
    auth_token  = config.AUTH_TOKEN
    twlo_cell = config.TWLO_CELL
except:
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token  = os.environ.get('AUTH_TOKEN')
    twlo_cell = os.environ.get('TWLO_CELL')

client = Client(account_sid, auth_token)

# Pretty view for starter
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    return HttpResponse('<pre>' + r.text + '</pre>')

@csrf_exempt
def get_one(request):
    if request.method == "POST":
        stock_table = Stock()
        from_cell = request.body.decode('utf-8').split()[0]
        code = request.body.decode('utf-8').split()[2]
        price = stock_table.get_price(code.upper())

        if price is False:
            price = "Code not valid"
        message = client.messages.create(
            to=from_cell,
            from_=twlo_cell,
            body=price)

    return HttpResponse(200)

@csrf_exempt
def get_all(request):
    if request.method == "POST":
        phone_number = request.body.decode('utf-8')

        try:
            stock_list = list(UserXStock.objects.filter(uid=User.objects.get(phone=phone_number).id))
            stock_id_list = [i.sid.id for i in stock_list]
            stock_code_list = [i.code for i in list(Stock.objects.filter(id__in=stock_id_list))]
            stock_market = Stock()
            if len(stock_code_list) == 1:
                result_string = stock_market.get_list_price(stock_code_list)
            else:
                result = stock_market.get_list_price(stock_code_list)
                result_string = ""
                for i, v in result.items():
                    result_string += (i+" price: $"+str(v)+"\n")
            message = client.messages.create(
                to=phone_number,
                from_=twlo_cell,
                body=result_string)
            return HttpResponse(200)
        except Exception as e:

            # sys.stdout.flush()
            message = client.messages.create(
                to=phone_number,
                from_=twlo_cell,
                body="No records found")
            return HttpResponse(400)

@csrf_exempt
def refresh(request):
    if request.method == "POST":
        if request.body.decode('utf-8') == "refresh":
            user_list = list(User.objects.all().values_list('phone', flat=True))
            print(user_list)
            for phone_number in user_list:
                try:
                    stock_list = list(UserXStock.objects.filter(uid=User.objects.get(phone=phone_number).id))
                    stock_id_list = [i.sid.id for i in stock_list]
                    stock_code_list = [i.code for i in list(Stock.objects.filter(id__in=stock_id_list))]
                    stock_market = Stock()
                    if len(stock_code_list) == 1:
                        result_string = stock_market.get_list_price(stock_code_list)
                    else:
                        result = stock_market.get_list_price(stock_code_list)
                        result_string = ""
                        for i, v in result.items():
                            result_string += (i+" price: $"+str(v)+"\n")
                    message = client.messages.create(
                        to=phone_number,
                        from_=twlo_cell,
                        body=result_string)
                except Exception as e:
                    continue

    return HttpResponse(200)

@csrf_exempt
def add(request):
    if request.method == "POST":

        from_cell = request.body.decode('utf-8').split()[0]
        code = request.body.decode('utf-8').split()[2]

        stock_table = Stock()
        result = stock_table.add_stock(code.upper())
        if result == False:
            message = client.messages.create(
                to=from_cell,
                from_=twlo_cell,
                body="Code Not Valid")
            return HttpResponse(400)

        user_table = User()
        user_table.add_user(from_cell)

        cross_table = UserXStock()
        result = cross_table.link(from_cell, code.upper())
        if result == False:
            message = client.messages.create(
                to=from_cell,
                from_=twlo_cell,
                body="Error occured, please try again")
            return HttpResponse(400)

        message = client.messages.create(
            to=from_cell,
            from_=twlo_cell,
            body="Successfully added "+code.upper())

    return HttpResponse(200)

@csrf_exempt
def remove_stock(request):
    if request.method == "POST":

        from_cell = request.body.decode('utf-8').split()[0]
        code = request.body.decode('utf-8').split()[2]

        cross_table = UserXStock()
        result = cross_table.unlink(from_cell, code.upper())
        if result == False:
            message = client.messages.create(
                to=from_cell,
                from_=twlo_cell,
                body="Error occured when trying to remove " + code.upper())
            return HttpResponse(200)
        else:
            message = client.messages.create(
                to=from_cell,
                from_=twlo_cell,
                body="Successfully removed "+code.upper())

    return HttpResponse(200)

@csrf_exempt
def unsubscribe(request):
    if request.method == "POST":
        from_cell = request.body.decode('utf-8')
        try:
            user_table = User()
            user_object = user_table.get_user(from_cell)

            cross_table = UserXStock.objects.filter(uid=user_object.id).delete()
            user_object.delete()
        except:
            message = client.messages.create(
                to=from_cell,
                from_=twlo_cell,
                body="Not subscribed or no stocks in record")
            return HttpResponse(400)
        message = client.messages.create(
            to=from_cell,
            from_=twlo_cell,
            body="Successfully unsubscribed")

    return HttpResponse(200)