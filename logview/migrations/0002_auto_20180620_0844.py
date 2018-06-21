# Generated by Django 2.0.6 on 2018-06-20 08:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('logview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logfileentry',
            name='time',
            field=models.TimeField(db_index=True, default=django.utils.timezone.now, verbose_name='time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logfileentry',
            name='date',
            field=models.DateField(db_index=True, verbose_name='date'),
        ),
    ]