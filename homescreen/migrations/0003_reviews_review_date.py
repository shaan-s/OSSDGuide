# Generated by Django 5.1.1 on 2024-09-24 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homescreen', '0002_courses_reviews_delete_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='review_date',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
