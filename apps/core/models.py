from django.contrib.gis.db import models
from django.db.models.signals import post_save

import redis

try:
    import simplejson as json
except:
    import json

class Administrative(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    admin_level = models.CharField(max_length=100, blank=True, null=True)
    geodata = models.LineStringField()
    updated = models.DateTimeField(auto_now=True)

    objects = models.GeoManager()

    class Meta:
        verbose_name = "Administrative"
        verbose_name_plural = "Administratives"
        ordering = ("-updated",)

    def __unicode__(self):
        return str(self.id)


CHECKIN_TYPE = (
    ('1', 'Direct'),
    ('2', 'Foursquare')
    )


class Checkin(models.Model):
    type = models.CharField(max_length=1, choices=CHECKIN_TYPE)
    title = models.CharField(max_length=400, blank=True, null=True)
    geodata = models.PointField()
    updated = models.DateTimeField(auto_now=True)

    objects = models.GeoManager()

    class Meta:
        verbose_name = "Checkin"
        verbose_name_plural = "Checkins"
        ordering = ("-updated",)

    def get_absolute_url(self):
        return "ok"

    def __unicode__(self):
        return self.title

def publish_checkin(sender, **kwargs):
    checkin = kwargs['instance']
    r = redis.Redis()
    r.publish('geojam', checkin.title)

post_save.connect(publish_checkin, sender=Checkin,
    dispatch_uid="checkin.publish.to.redis")
