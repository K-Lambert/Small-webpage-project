# Generated by Django 4.0.2 on 2022-02-03 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppOne', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofilemodel',
            old_name='second_name',
            new_name='last_name',
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='first_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='last_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]