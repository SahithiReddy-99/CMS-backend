# Generated by Django 4.1.1 on 2022-09-23 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_flatowner_alter_employees_mobileno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatowner',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]