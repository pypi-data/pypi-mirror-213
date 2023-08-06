from django.db import models

# Create your models here.
class HScode(models.Model):
    hscode8 = models.CharField(max_length=8, primary_key=True)
    hscode2 = models.CharField(max_length=2)
    hscode4 = models.CharField(max_length=4)
    description = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.hscode8}"
    
    class Meta:
        verbose_name = 'HScode'