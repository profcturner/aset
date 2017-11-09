from django.db import models

class ExternalBody(models.Model):
    """Information on External Bodies

    name    name of the grant providing body
    details any more details for that body"""

    name = models.CharField(max_length=300)
    details = models.TextField()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "external bodies"
        ordering = ['name']


class Category(models.Model):
    """Categories of activity

    name    whether the activity is Teaching, Research etc.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

