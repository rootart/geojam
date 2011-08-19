from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    HttpResponseForbidden
    )
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse

from django.contrib.gis.geos import *

import oauth2 as oauth
import urllib
try:
    import simplejson as json
except ImportError:
    import json


from core.models import Checkin


SERVER = getattr(settings, 'OAUTH_SERVER', 'foursquare.com')
AUTHENTICATE_URL = getattr(settings, 'OAUTH_REQUEST_TOKEN_URL', 'http://%s/oauth2/authenticate' % SERVER)
ACCESS_TOKEN_URL = getattr(settings, 'OAUTH_ACCESS_TOKEN_URL', 'http://%s/oauth2/access_token' % SERVER)
API_URL= "https://api.foursquare.com/v2/"

FOURSQUARE_CONSUMER_KEY = getattr(settings, 'FOURSQUARE_CONSUMER_KEY', 'YOUR_KEY')
FOURSQUARE_CONSUMER_SECRET = getattr(settings, 'FOURSQUARE_CONSUMER_SECRET', 'YOUR_SECRET')


def auth(request):
    params = {
        'response_type': 'code',
        'client_id': FOURSQUARE_CONSUMER_KEY,
        'redirect_uri': 'http://geojam.djangostars.com/auth/return/'
    }
    url = AUTHENTICATE_URL + "?" + urllib.urlencode(params)

    return HttpResponseRedirect(url)

def logout_(request):
    request.session.clear()
    logout(request)
    return HttpResponseRedirect(reverse('dashboard'))

def fetch_data(api, token):
    link = API_URL + api + "?oauth_token=" + token
    try:
        f = urllib.urlopen(link)
    except:
        pass
    else:
        return json.loads(f.read())


def fetch_checkins(token):
    api = 'users/self/checkins'

    link = API_URL + api + "?oauth_token=" + token
    try:
        f = urllib.urlopen(link)
    except:
        pass
    data = json.loads(f.read())
    
    for item in data['response']['checkins']['items']:
        geodata = Point(
            item['venue']['location']['lng'],
            item['venue']['location']['lat'])
        # import pdb
        # pdb.set_trace()
        checkin = Checkin(
            type = 2,
            title = item['venue']['name'],
            geodata = geodata
        )
        
        checkin.save()


def return_(request):
    code = request.GET.get('code', None)
    if code:
        params = {
            'client_id': FOURSQUARE_CONSUMER_KEY,
            'client_secret': FOURSQUARE_CONSUMER_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://geojam.djangostars.com/auth/return/',
            'code': code,
        }

        params = urllib.urlencode(params)
        f = urllib.urlopen(ACCESS_TOKEN_URL+"?"+params)
        token = f.read()
        token = json.loads(token)['access_token']
        
        # Get user information using api request
        data = fetch_data('users/self', token)
        foursquare_user_data = data['response']['user']

        user = authenticate(foursquare_user_data=foursquare_user_data, 
            access_token=token)
        login(request, user)
        request.session['token_%s' % user.username] = token
        
        # Fetch last 100 checkins from foursquare
        fetch_checkins(token)

        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return HttpResponseForbidden("Hei, Go away!")
