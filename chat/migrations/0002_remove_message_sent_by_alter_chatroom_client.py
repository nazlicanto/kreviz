# Generated by Django 4.2.1 on 2023-12-15 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='sent_by',
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='client',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
