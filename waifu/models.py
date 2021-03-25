from django.db import models


class UrlModel(models.Model):
    main_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=255)
    time_add = models.CharField(max_length=255)
    click = models.IntegerField()

    def __str__(self):
        return f'{self.short_url} -- {self.time_add} -- {self.click} -- {self.main_url}'