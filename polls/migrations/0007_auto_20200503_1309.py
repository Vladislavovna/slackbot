# Generated by Django 3.0.5 on 2020-05-03 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_pollusermeta_response_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollusermeta',
            name='response_url',
            field=models.TextField(null=True),
        ),
    ]
