from django.db import models
from django.db.models import Lookup

# Create your models here.


class Rand(models.Model):
    curs = models.CharField(max_length=100,default=None, blank=True, null=True)
    zi = models.CharField(max_length=25,default=None, blank=True, null=True)
    ora_inceput = models.TimeField(default=None, blank=True, null=True)
    ora_sfarsit = models.TimeField(default=None, blank=True, null=True)
    grupa = models.CharField(max_length=60,default=None, blank=True, null=True)
    tip = models.CharField(max_length=20,default=None, blank=True, null=True)
    sala = models.CharField(max_length=50,default=None, blank=True, null=True)
    profesor = models.CharField(max_length=200,default=None, blank=True, null=True)
    pachet = models.CharField(max_length=3,default=0, blank=True, null=True)

    def __str__(self):
        return str(self.id)+" "+self.zi+" "+self.curs+" "+self.sala+" "+str(self.ora_inceput)+" "+str(self.ora_sfarsit)

    def get_sala(self):
        return self.sala

    def get_materie(self):
        return self.curs

    def get_profesor(self):
        return self.profesor

    def get_zi(self):
        return self.zi