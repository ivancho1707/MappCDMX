import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

CDMX_BOUNDING_BOX = {
    "maxLat":  19.528407,
    "maxLon": -98.977203,
    "minLat": 19.272582,
    "minLon": -99.242249
}

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
    
@require_http_methods(['GET'])
def alerts_and_routes(request):
    maxLat = CDMX_BOUNDING_BOX['maxLat']
    maxLon = CDMX_BOUNDING_BOX['maxLon']
    minLat = CDMX_BOUNDING_BOX['minLat']
    minLon = CDMX_BOUNDING_BOX['minLon']
    lat = request.GET['lat']
    lon = request.GET['lon']
    radius = request.GET['radius']
    
    base_url = "https://www.waze.com/row-rtserver/web/TGeoRSS"
    payload = {
        "ma": 600,
		"mj": 100,
		"mu": 100,
		"left": minLon,
		"right": maxLon,
		"bottom": minLat,
		"top": maxLat
	}
    alert_array = requests.get(base_url, params=payload).json()['alerts']
    
    base_url = "http://ec2-54-152-18-59.compute-1.amazonaws.com:8000/otp/routers/default/index/stops"
    payload = {
        "lat": lat,
        "lon": lon,
        "radius": radius
    }
    stop_array = requests.get(base_url, params=payload).json()

    route_array = []
    for stop in stop_array:
        base_url = "http://ec2-54-152-18-59.compute-1.amazonaws.com:8000/otp/routers/default/index/routes"
        payload = {
            "hasStop": stop['id']
        }
        route_array = route_array + requests.get(base_url, params=payload).json()
    
    route_geometry_array = []
    for route in route_array:
        trip_id = route['id'] + "T0"
        base_url = "http://ec2-54-152-18-59.compute-1.amazonaws.com:8000/otp/routers/default/index/trips/%s/geometry" % trip_id
        route_geometry_array.append(requests.get(base_url).json())
    
    response = {
        "alerts": alert_array,
        "routes": route_geometry_array
    }
    return HttpResponse(json.dumps(response), content_type="application/json")
    
def redirect_request(base_url, request):
    payload = request.GET
    r = requests.get(base_url, params=payload)
    return HttpResponse(r.text, content_type="application/json")
    
