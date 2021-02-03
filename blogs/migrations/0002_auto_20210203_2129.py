# Generated by Django 3.1.5 on 2021-02-03 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='avatar',
            field=models.ImageField(max_length=250, null=True, upload_to='images/%Y/%m/%d/%H/%M/%S/', verbose_name='Аватарка'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(max_length=250, null=True, upload_to='images/%Y/%m/%d/%H/%M/%S/'),
        ),
    ]