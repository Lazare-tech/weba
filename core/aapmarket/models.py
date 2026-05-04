from django.db import models

# Create your models here.
from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    reponse = models.TextField()
    ordre = models.IntegerField(default=0)

    class Meta:
        verbose_name = "FAQ"
        ordering = ['ordre']

    def __str__(self):
        return self.question