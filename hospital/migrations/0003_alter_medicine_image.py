# Generated by Django 5.1.2 on 2024-10-18 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_alter_medicine_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='image',
            field=models.ImageField(upload_to='medicines/'),
        ),
    ]
