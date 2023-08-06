from django.db import models

class Area(models.Model):
    area_code = models.CharField(max_length=20)
    zone_code = models.CharField(max_length=5)
    zone = models.CharField(max_length=10)
    country_alpha2 = models.CharField(max_length=2)
    country_alpha3 = models.CharField(max_length=3)
    country_code = models.CharField(max_length=3)
    country = models.CharField(max_length=100)
    subdivision_code = models.CharField(max_length=6)
    subdivision_th = models.CharField(max_length=100)
    subdivision_en = models.CharField(max_length=100)
    year = models.CharField(max_length=4)

    def __str__(self) -> str:
        return f"{self.area_code}"
    