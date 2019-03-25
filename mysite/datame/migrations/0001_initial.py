# Generated by Django 2.1 on 2019-03-25 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Apply title')),
                ('description', models.TextField(verbose_name='Apply description')),
                ('date', models.DateTimeField(blank=True)),
                ('status', models.CharField(choices=[('PE', 'PENDING'), ('AC', 'ACEPTED'), ('RE', 'REJECTED')], max_length=8, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('tax', models.FloatField()),
                ('total', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('PE', 'PENDING'), ('AC', 'ACCEPTED'), ('RE', 'REJECTED')], max_length=8, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(blank=True)),
                ('limit_date', models.DateTimeField(blank=True)),
                ('accepted_ds', models.BooleanField(default=False)),
                ('accepted_company', models.BooleanField(default=True)),
                ('expiration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DataScientist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('surname', models.CharField(max_length=50, verbose_name='Surname')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('path', models.CharField(max_length=200, verbose_name='Path')),
                ('apply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datame.Apply')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
                ('entity', models.CharField(max_length=50, verbose_name='Entity')),
                ('date_start', models.DateTimeField(verbose_name='Start date')),
                ('date_finish', models.DateTimeField(blank=True, null=True, verbose_name='End date')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Offer title')),
                ('description', models.TextField(verbose_name='Offer description')),
                ('price_offered', models.FloatField(verbose_name='Price offered')),
                ('currency', models.CharField(choices=[('0', '€'), ('1', '$'), ('2', '£')], max_length=1, verbose_name='Currency type')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('limit_time', models.DateTimeField(blank=True)),
                ('company', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='datame.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Section name')),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='datame.CV')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='datame.Section'),
        ),
        migrations.AddField(
            model_name='file',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datame.Offer'),
        ),
        migrations.AddField(
            model_name='cv',
            name='owner',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='datame.DataScientist'),
        ),
        migrations.AddField(
            model_name='contract',
            name='dataScientist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datame.DataScientist'),
        ),
        migrations.AddField(
            model_name='contract',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datame.Offer'),
        ),
        migrations.AddField(
            model_name='bill',
            name='contract',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='datame.Contract'),
        ),
        migrations.AddField(
            model_name='apply',
            name='dataScientist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datame.DataScientist'),
        ),
        migrations.AddField(
            model_name='apply',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datame.Offer'),
        ),
    ]
