import urllib
import json
from decimal import Decimal

from django.db import models


class Marker(models.Model):
    """
    Abstract model that provides geocoding for models with address.
    """
    address = models.CharField(max_length=200, blank=True,
                               help_text="Separate address items with commas.")
    latitude = models.DecimalField(max_digits=8, decimal_places=6,
                                   null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    null=True, blank=True)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(Marker, self).__init__(*args, **kwargs)
        self._original_address = self.address

    def save(self, *args, **kwargs):
        if self._original_address != self.address:
            self.latitude, self.longitude = 0, 0
        if self.address and (not self.latitude or not self.longitude):
            self.latitude, self.longitude = self.geocode(self.address)
            # print self.latitude, self.longitude
        super(Marker, self).save(*args, **kwargs)

    def geocode(self, address):
        address = urllib.quote_plus(address.encode('utf-8'))
        base_url = "http://maps.googleapis.com/maps/api/geocode/json?"
        request = base_url + "address=%s" % address
        if self.country:
            request += "&region=%s" % self.country.code
        data = json.loads(urllib.urlopen(request).read())
        if data['status'] == 'OK':
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return Decimal(latitude), Decimal(longitude)
        return 0, 0
