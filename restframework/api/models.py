from django.db import models


class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title