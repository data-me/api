# Generated by Django 2.1 on 2019-03-21 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datame', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply_model',
            name='dataScientist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='datame.DataScientist_model'),
        ),
    ]
