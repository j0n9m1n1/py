# Generated by Django 2.1.1 on 2018-11-08 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0003_auto_20181108_0741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='device_token',
            field=models.CharField(default='null', max_length=200),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='old_reports',
            field=models.CharField(default='null', max_length=200),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='old_subjects',
            field=models.CharField(default='null', max_length=200),
        ),
    ]
