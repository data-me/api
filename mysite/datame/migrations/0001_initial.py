# Generated by Django 2.1 on 2019-03-27 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PE', 'PENDING'), ('AC', 'ACEPTED'), ('RE', 'REJECTED')], max_length=8, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('description', models.TextField(max_length=50, verbose_name='Description')),
                ('nif', models.CharField(max_length=9, verbose_name='NIF')),
                ('logo', models.URLField(verbose_name='Logo URL')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='title')),
                ('body', models.TextField(max_length=100, verbose_name='body')),
                ('moment', models.DateTimeField(auto_now=True)),
                ('receiver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
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
                ('finished', models.BooleanField(default=False)),
                ('files', models.URLField()),
                ('contract', models.TextField(verbose_name='Contract')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datame.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='datame.CV')),
            ],
        ),
        migrations.CreateModel(
            name='Section_name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_name', to='datame.Section_name'),
        ),
        migrations.AddField(
            model_name='item',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='datame.Section'),
        ),
        migrations.AddField(
            model_name='cv',
            name='owner',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='datame.DataScientist'),
        ),
        migrations.AddField(
            model_name='apply',
            name='dataScientist',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='datame.DataScientist'),
        ),
        migrations.AddField(
            model_name='apply',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datame.Offer'),
        ),
    ]
