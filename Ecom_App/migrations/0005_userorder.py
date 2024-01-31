# Generated by Django 4.2.2 on 2023-06-30 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom_App', '0004_userdetails_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default=None, max_length=100)),
                ('Total', models.CharField(default=None, max_length=100)),
                ('Items', models.CharField(default=None, max_length=100)),
                ('Status', models.CharField(default=None, max_length=100)),
            ],
            options={
                'db_table': 'UserOrder',
            },
        ),
    ]