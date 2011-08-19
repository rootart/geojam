from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from django.contrib.gis.geos import *
from django.contrib.gis.utils import GeoIP

from models import Administrative, Checkin
from forms import CheckinForm

try:
    import simplejson as json
except ImportError:
    import json

def adm_details(request, adm_id, extension):
    adm = get_object_or_404(Administrative, id=int(adm_id))
    if extension == "json":
        data = adm.geodata.geojson
        mimetype = "application/json"
    elif extension == "kml":
        data = adm.geodata.kml
        mimetype = "kml"

    return HttpResponse(data, mimetype=mimetype)


def dashboard(request):
    ip = request.META['REMOTE_ADDR']
    geoip = GeoIP()
    
    try:
        country = geoip.country(ip)
    except:
        country = "Ghost"
    else:
        country = country['country_name']
    
    try:
        coords = geoip.coords(ip)
        if not coords:
            coords = "on Earth"
    except:
        coords = "on Earth"
    
    location = {
        'country': country,
        'coords': coords
    }
    
    checkins = Checkin.objects.all()
    obj_list = list()
    for item in checkins:
        item.geodata.transform(900913)
        obj_list.append(json.loads(item.geodata.geojson))
    obj_list = json.dumps(obj_list)

    last_20 = Checkin.objects.all()[:19]
    data = {
        "checkins": last_20,
        "count": Checkin.objects.all().count(),
        "obj_list": obj_list,
        "location": location
        }
    return render_to_response("index.html", data,
        context_instance=RequestContext(request, {}))


def checkin(request):
    ip = request.META['REMOTE_ADDR']
    geoip = GeoIP()
    coords = geoip.coords(ip)
    if not coords:
        coords = (0, 0)
    if request.method == "POST":
        form = CheckinForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.type = '1'
            checkin.geodata = Point(coords)
            checkin.save()
        if request.is_ajax():
            return HttpResponse("{response: 'ok'}", mimetype="application/json")
        else:
            HttpResponseRedirect('/')
    else:
        form = CheckinForm()
    return render_to_response('checkin.html', {'form':form},
        RequestContext(request))


def checkins(request):
    checkins = Checkin.objects.all()
    obj_list = list()
    for item in checkins:
        item.geodata.transform(900913)
        obj_list.append(json.loads(item.geodata.geojson))
    obj_list = json.dumps(obj_list)
    return HttpResponse(obj_list, mimetype="application/json")