# Generated by Django 4.2.16 on 2024-11-21 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='userProduct',
        ),
    ]
