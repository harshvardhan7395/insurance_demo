import json

from django.core import serializers
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import PermissionDenied
# Create your views here.
from policy.models import Policy
from users.models import User


@csrf_exempt
def app_login(request):
    if request.method =='POST':
        json_data = json.loads(request.body)
        print(json_data)
        user = authenticate(username=json_data.get('username'),password=json_data.get('password'))
        if not user:
            raise PermissionDenied()
        if user:
            login(request,user)
        return HttpResponse('200 Ok')
    elif request.method =='GET':
        return HttpResponse('Access Denied')



@csrf_exempt
def logot(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponse("LOG OUT")
    elif request.method == 'GET':
        return HttpResponse('INVALID ACCESS')


@csrf_exempt
def dashboard(request):
    policy = Policy.objects.all().select_related('customer')
    data={}
    for po in policy:
        if po.customer.region in data:
            value = data[po.customer.region]
            data[po.customer.region] = value + 1
        else:
            data[po.customer.region] = 1

    print(data)
    policy_month=Policy.objects.annotate(month=ExtractMonth('date_of_purchase')).values('month').annotate(count=Count('id')).values('month', 'count')
    print(policy_month)
    dict=[]
    for poli in policy_month:
        dict.append(poli)

    obj={
        "data":data,
        "policy_month": dict
    }
    return HttpResponse(json.dumps(obj), content_type='application/json')


@csrf_exempt
def list(request):

    users = User.objects.all()
    data = serializers.serialize('json', users)
    return HttpResponse(data, content_type='application/json')