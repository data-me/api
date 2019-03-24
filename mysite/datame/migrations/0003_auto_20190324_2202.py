# Generated by Django 2.1 on 2019-03-24 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datame', '0002_bill_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='offer',
        ),
        migrations.AddField(
            model_name='bill',
            name='contract',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='datame.Contract'),
        ),
    ]
