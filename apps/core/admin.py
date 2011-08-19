from django.contrib.gis import admin

from models import Administrative, Checkin

admin.site.register(Administrative, admin.GeoModelAdmin)
admin.site.register(Checkin, admin.GeoModelAdmin)
