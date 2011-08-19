from core.views import *


def fetch_checkins(token):
    api = 'users/self/checkins'
    
    link = API_URL + api + "?oauth_token=" + token
    try:
        f = urllib.urlopen(link)
    except:
        pass
    else:
        return json.loads(f.read())