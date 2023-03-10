# Generated by Django 4.0.5 on 2022-09-15 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('SId', models.AutoField(primary_key=True, serialize=False)),
                ('Fname', models.CharField(default='', max_length=255)),
                ('Lname', models.CharField(default='', max_length=255)),
                ('Email', models.EmailField(default='', max_length=255)),
                ('Password', models.TextField(default='', max_length=300)),
                ('ContactNo', models.CharField(default='', max_length=100)),
                ('Role', models.CharField(choices=[('superadmin', 'superadmin'), ('customer', 'customer')], default='customer', max_length=10)),
                ('Profile', models.ImageField(default='SuperAdmin/dummy.jpg', upload_to='SuperAdmin/')),
                ('Otp', models.IntegerField(default=0)),
                ('OtpStatus', models.CharField(default='False', max_length=10)),
                ('OtpCount', models.IntegerField(default=0)),
                ('passwordstatus', models.CharField(default='False', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Productinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Last_Updated', models.DateField(default='')),
                ('Link', models.TextField(default='', max_length=3000)),
                ('Brand', models.CharField(default='', max_length=255)),
                ('Model', models.CharField(default='', max_length=255)),
                ('Image_Link', models.CharField(default='', max_length=3000)),
                ('Base_Price', models.CharField(default='', max_length=55)),
                ('Type', models.CharField(default='', max_length=255)),
                ('Assembly', models.CharField(default='', max_length=255)),
                ('Included_Software', models.CharField(default='', max_length=255)),
                ('Nominal_Advertised_Size_inches_x', models.CharField(default='', max_length=255)),
                ('Nominal_Advertised_Size_inches_y', models.CharField(default='', max_length=255)),
                ('Nominal_Advertised_Size_mm_x', models.CharField(default='', max_length=255)),
                ('Nominal_Advertised_Size_mm_y', models.CharField(default='', max_length=255)),
                ('Max_Travel_inches_x', models.CharField(default='', max_length=255)),
                ('Max_Travel_inches_y', models.CharField(default='', max_length=255)),
                ('Max_Travel_inches_z', models.CharField(default='', max_length=255)),
                ('Max_Travel_mm_x', models.CharField(default='', max_length=255)),
                ('Max_Travel_mm_y', models.CharField(default='', max_length=255)),
                ('Max_Travel_mm_z', models.CharField(default='', max_length=255)),
                ('Max_Gantry_Clearance_inches', models.CharField(default='', max_length=255)),
                ('Max_Gantry_Clearance_mm', models.CharField(default='', max_length=255)),
                ('Overall_Table_Size_inches_x', models.CharField(default='', max_length=255)),
                ('Overall_Table_Size_inches_y', models.CharField(default='', max_length=255)),
                ('Overall_Table_Size_mm_x', models.CharField(default='', max_length=255)),
                ('Overall_Table_Size_mm_y', models.CharField(default='', max_length=255)),
                ('Footprint_inches_len', models.CharField(default='', max_length=255)),
                ('Footprint_inches_wid', models.CharField(default='', max_length=255)),
                ('Footprint_inches_hei', models.CharField(default='', max_length=255)),
                ('Footprint_mm_len', models.CharField(default='', max_length=255)),
                ('Footprint_mm_wid', models.CharField(default='', max_length=255)),
                ('Footprint_mm_hei', models.CharField(default='', max_length=255)),
                ('Shipping_Dimensions_inches_len', models.CharField(default='', max_length=255)),
                ('Shipping_Dimensions_inches_wid', models.CharField(default='', max_length=255)),
                ('Shipping_Dimensions_inches_hei', models.CharField(default='', max_length=255)),
                ('Shipping_Dimensions_mm_len', models.CharField(default='', max_length=255)),
                ('Shipping_Dimensions_mm_wid', models.CharField(default='', max_length=255)),
                ('Shipping_Dimensions_mm_hei', models.CharField(default='', max_length=255)),
                ('Weight_pound', models.CharField(default='', max_length=255)),
                ('Weight_kilo', models.CharField(default='', max_length=255)),
                ('Drive_Type_x', models.CharField(default='', max_length=255)),
                ('Drive_Type_y', models.CharField(default='', max_length=255)),
                ('Drive_Type_z', models.CharField(default='', max_length=255)),
                ('Ball_Screw_Dia_x', models.CharField(default='', max_length=255)),
                ('Ball_Screw_Dia_y', models.CharField(default='', max_length=255)),
                ('Ball_Screw_Dia_z', models.CharField(default='', max_length=255)),
                ('Drive_Motors_x', models.CharField(default='', max_length=255)),
                ('Drive_Motors_y', models.CharField(default='', max_length=255)),
                ('Drive_Motors_z', models.CharField(default='', max_length=255)),
                ('Motion_Guide_x', models.CharField(default='', max_length=255)),
                ('Motion_Guide_y', models.CharField(default='', max_length=255)),
                ('Motion_Guide_z', models.CharField(default='', max_length=255)),
                ('Resolution_inches', models.CharField(default='', max_length=255)),
                ('Resolution_mm', models.CharField(default='', max_length=255)),
                ('Materials_Gantry', models.CharField(default='', max_length=255)),
                ('Materials_Bed', models.CharField(default='', max_length=255)),
                ('Materials_Spoilboard', models.CharField(default='', max_length=255)),
                ('Materials_Base', models.CharField(default='', max_length=255)),
                ('Max_Cut_Speed_inches_min', models.CharField(default='', max_length=255)),
                ('Max_Cut_Speed_mm_min', models.CharField(default='', max_length=255)),
                ('Rapid_Feed_Rate_inches_min', models.CharField(default='', max_length=255)),
                ('Rapid_Feed_Rate_mm_min', models.CharField(default='', max_length=255)),
                ('Spindle_Type', models.CharField(default='', max_length=255)),
                ('Spindle_Size', models.CharField(default='', max_length=255)),
                ('Configuration', models.CharField(default='', max_length=255)),
                ('Cooling', models.CharField(default='', max_length=255)),
                ('Min_Spindle_Speed', models.CharField(default='', max_length=255)),
                ('Max_Spindle_Speed', models.CharField(default='', max_length=255)),
                ('Max_Collet_Size', models.CharField(default='', max_length=255)),
                ('ATC', models.CharField(default='', max_length=255)),
                ('ATC_Type', models.CharField(default='', max_length=255)),
                ('hash_of_Tools', models.CharField(default='', max_length=255)),
                ('Tool_Probe', models.CharField(default='', max_length=255)),
                ('Power_Requirements_Volts', models.CharField(default='', max_length=255)),
                ('Power_Requirements_Hz', models.CharField(default='', max_length=255)),
                ('Power_Requirements_Amps', models.CharField(default='', max_length=255)),
                ('Power_Requirements_Phase', models.CharField(default='', max_length=255)),
                ('Controller', models.CharField(default='', max_length=255)),
                ('PC_Required', models.CharField(default='', max_length=255)),
                ('Laser', models.CharField(default='', max_length=255)),
                ('Vacuum_Table', models.CharField(default='', max_length=255)),
                ('_4th_Axis', models.CharField(default='', max_length=255)),
                ('Pendant', models.CharField(default='', max_length=255)),
                ('Waranty_Months', models.CharField(default='', max_length=255)),
                ('Support', models.CharField(default='', max_length=255)),
                ('Orgin', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='whitelistToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('useragent', models.TextField(default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapi.account')),
            ],
        ),
    ]
