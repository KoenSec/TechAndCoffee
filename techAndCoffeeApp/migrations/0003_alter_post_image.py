# Generated by Django 3.2.6 on 2021-09-07 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techAndCoffeeApp', '0002_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]