import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


# Create your views here.
@require_http_methods(['GET'])
def alerts(request):
    base_url = "https://www.waze.com/row-rtserver/web/TGeoRSS"
    return redirect_request(base_url, request)
    
@require_http_methods(['GET'])
def plan_trip(request):
    base_url = "http://ec2-54-152-18-59.compute-1.amazonaws.com:8000/otp/routers/default/plan"
    return redirect_request(base_url, request)
    
@require_http_methods(['GET'])
def stops(request):
    base_url = "http://ec2-54-152-18-59.compute-1.amazonaws.com:8000/otp/routers/default/index/stops"
    return redirect_request(base_url, request)
    
@require_http_methods(['GET'])
def routes(request):
    base_url = "http://ec2-54-152-18-59.compute-1.amazonaws.com:8000/otp/routers/default/index/routes"
    return redirect_request(base_url, request)
    
@require_http_methods(['GET'])
def geometry(request, tripId):
    base_url = "http://ec2-54-152-18-59.compute-1.amazonaws.com:8000/otp/routers/default/index/trips/%s/geometry" % tripId
    return redirect_request(base_url, request)
    
def redirect_request(base_url, request):
    payload = request.GET
    r = requests.get(base_url, params=payload)
    return HttpResponse(r.text, content_type="application/json")