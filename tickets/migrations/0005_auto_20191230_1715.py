# Generated by Django 2.2.9 on 2019-12-30 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20191230_1710'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upvoted',
            old_name='ticket_voted',
            new_name='ticket',
        ),
    ]
