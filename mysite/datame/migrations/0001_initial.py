from django.db import migrations, models
import django.utils.timezone



class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('tax', models.FloatField()),
                ('total', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('PE', 'PENDING'), ('AC', 'ACEPTED'), ('RE', 'REJECTED')], max_length=8, verbose_name='Status')),
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Offer title')),
                ('description', models.CharField(max_length=200, verbose_name='Offer description')),
                ('price_offered', models.FloatField()),
                ('currency', models.CharField(choices=[(0, 'EUROS'), (1, 'DOLLARS'), (2, 'POUNDS')], max_length=1)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('limit_time', models.DateTimeField(blank=True)),
            ],
        ),
    ]
