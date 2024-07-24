from django.db import models

class CitySearchCount(models.Model):
    city = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('city', 'user')

    def __str__(self):
        return f"{self.city} ({self.user}): {self.count}"
