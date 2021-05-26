# Generated by Django 3.1.7 on 2021-03-26 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comuni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('codice_provincia', models.IntegerField(primary_key=True, serialize=False, verbose_name='codice Istat')),
                ('nome', models.CharField(db_index=True, max_length=300, verbose_name='Nome')),
                ('codice_targa', models.CharField(db_index=True, max_length=2)),
                ('regione', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comuni.regione')),
            ],
            options={
                'verbose_name': 'provincia',
                'verbose_name_plural': 'province',
                'ordering': ['nome'],
            },
        ),
    ]
