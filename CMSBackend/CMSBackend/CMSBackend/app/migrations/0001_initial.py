# Generated by Django 4.1.1 on 2022-09-29 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('maintenance', 'maintenance'), ('others', 'others')], default='electricity', max_length=20)),
                ('date', models.DateField(auto_now=True)),
                ('description', models.CharField(max_length=50)),
                ('billNumber', models.IntegerField()),
                ('isPaid', models.BooleanField(default=False)),
                ('totalBill', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('flatNo', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('type', models.CharField(max_length=50)),
                ('blockId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.block')),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Security', 'Security'), ('Helper', 'Helper'), ('Admin', 'Admin'), ('Supervisor', 'Supervisor')], default='Helper', max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('flatId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.flat')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True)),
                ('firstName', models.CharField(max_length=15, null=True)),
                ('lastName', models.CharField(max_length=15, null=True)),
                ('password', models.CharField(max_length=30)),
                ('mobileNo', models.CharField(max_length=10)),
                ('confirm_password', models.CharField(max_length=30)),
                ('occupation', models.CharField(blank=True, max_length=30, null=True)),
                ('image', models.ImageField(blank=True, default=None, upload_to='pictures')),
                ('isAdmin', models.BooleanField(default=False)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('user_type', models.CharField(choices=[('owner', 'owner'), ('staff', 'staff')], default='customer', max_length=8)),
                ('roleId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.roles')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('reviews', models.TextField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Reciept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('paymentType', models.CharField(choices=[('UPI', 'UPI'), ('Cash', 'Cash'), ('Card', 'Card')], default='Cash', max_length=5)),
                ('billId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.bill')),
            ],
        ),
        migrations.CreateModel(
            name='FlatServicedByEmployees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeeId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.user')),
                ('flatNo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.flat')),
            ],
        ),
        migrations.AddField(
            model_name='flat',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.user'),
        ),
        migrations.AddField(
            model_name='bill',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.user'),
        ),
    ]
