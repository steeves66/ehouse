# Generated by Django 4.0.5 on 2023-02-11 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_localite_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='localite',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.localite'),
        ),
    ]
