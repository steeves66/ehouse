# Generated by Django 4.0.5 on 2023-02-11 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_localite_table_alter_pays_table_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='localite',
            old_name='parent_id',
            new_name='parent',
        ),
    ]