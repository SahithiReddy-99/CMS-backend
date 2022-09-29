# Generated by Django 4.1.1 on 2022-09-29 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roles',
            name='role',
            field=models.CharField(choices=[('Security', 'Security'), ('Helper', 'Helper'), ('Admin', 'Admin'), ('Supervisor', 'Supervisor'), ('User', 'User')], default='Helper', max_length=10),
        ),
    ]
