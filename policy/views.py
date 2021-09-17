import json
from django.core.paginator import Paginator
from django.core import serializers
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from policy.models import Policy


@csrf_exempt
def edit(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        fields = json_data.get('fields')
        print(fields)

        policy = Policy.objects.filter(id=json_data.get('pk')).update(premium=fields.get('premium'),
                                                                      vehicle_segment=fields.get('vehicle_segment'),
                                                                      fuel=fields.get('fuel')
                                                                      , bodily_injury_liability=fields.get(
                'bodily_injury_liability'), personal_injury_protection=fields.get('personal_injury_protection'),
                                                                      property_damage_liability=fields.get(
                                                                          'property_damage_liability'),
                                                                      collision=fields.get('collision'),
                                                                      comprehensive=fields.get('comprehensive'))

        return HttpResponse('200 ok')

    elif request.method == 'GET':
        return HttpResponse('Access Denied')


@csrf_exempt
def list(request):
    policies = Policy.objects.all().order_by('date_of_purchase').select_related('customer')
    qs_json = serializers.serialize('json', policies)
    return HttpResponse(qs_json, content_type='application/json')


@csrf_exempt
def search(request, policy_id):
    policy = Policy.objects.filter(id=policy_id)
    qs_json = serializers.serialize('json', policy)
    return HttpResponse(qs_json, content_type='application/json')


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
    lis=[]
    for d in data:
        if d in data:
            obj={"month":d,"count":data[d]}
            lis.append(obj)
    print(lis)
    policy_month=Policy.objects.annotate(month=ExtractMonth('date_of_purchase')).values('month').annotate(count=Count('id')).values('month', 'count')
    print(policy_month)
    dict=[]
    for poli in policy_month:
        dict.append(poli)

    obj={
        "data":lis,
        "policy_month": dict
    }
    return HttpResponse(json.dumps(obj), content_type='application/json')
