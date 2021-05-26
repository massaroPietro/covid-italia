from django.db import models
from django.urls import reverse
# Create your models here.

class Regione(models.Model):
    codice_regione = models.IntegerField(primary_key=True, verbose_name="codice Istat")
    nome = models.CharField(max_length=300, db_index=True, verbose_name='nome')

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('regione_detail', kwargs={'codice_istat': self.codice_regione})

    class Meta:
        ordering = ['nome']
        verbose_name = 'regione'
        verbose_name_plural = 'regioni'

class Provincia(models.Model):
    codice_provincia = models.IntegerField(primary_key=True, verbose_name="codice Istat")
    nome = models.CharField(max_length=300, db_index=True, verbose_name="Nome")
    codice_targa = models.CharField(max_length=2, db_index=True)
    regione = models.ForeignKey(Regione, db_index=True, on_delete=models.PROTECT)

    def __str__(self):
        return '%s - %s' % (self.nome, self.regione.nome)

    class Meta:
        ordering = ['nome']
        verbose_name = 'provincia'
        verbose_name_plural = 'province'





