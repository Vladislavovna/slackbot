# Generated by Django 3.0.5 on 2020-05-03 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_pollusermeta'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollusermeta',
            name='response_url',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
