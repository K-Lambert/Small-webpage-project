# Generated by Django 4.0.2 on 2022-02-08 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppOne', '0002_rename_second_name_studentprofilemodel_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofilemodel',
            name='parent',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserProfileModel',
        ),
    ]