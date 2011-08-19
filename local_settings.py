DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'geojam',                      # Or path to database file if using sqlite3.
        'USER': 'gis_user',                      # Not used with sqlite3.
        'PASSWORD': 'rootart',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

FOURSQUARE_CONSUMER_KEY = 'QG2SEDCCIW2LNWG1DR21C2TXF3E1ICMACMG1GD50PWWUXA4P'
FOURSQUARE_CONSUMER_SECRET = 'VUI41JADP0SMI4XRVFFTWG2CF5BX4FJ3QK2XS0IUQ1R5K3IN'

