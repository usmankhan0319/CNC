from pyexpat import model
from django.db import models

# Create your models here.

role = (

    ('superadmin','superadmin'),
    ('customer','customer')
   
)

class Account(models.Model):

    SId = models.AutoField(primary_key=True)
    Fname=models.CharField(max_length=255, default="")
    Lname=models.CharField(max_length=255, default="")
    Email=models.EmailField(max_length=255, default="")
    Password=models.TextField(max_length=300, default="")
    ContactNo=models.CharField(max_length=100, default="")
    Role = models.CharField(max_length=10,choices=role, default="customer") 
    Profile= models.ImageField(upload_to='SuperAdmin/',default="SuperAdmin/dummy.jpg")
    Otp = models.IntegerField(default=0)
    OtpStatus = models.CharField(max_length=10, default="False")
    OtpCount = models.IntegerField(default=0)
    passwordstatus = models.CharField(max_length=10,default="False")

    def __str__(self):
        return self.Email

class whitelistToken(models.Model):
    user = models.ForeignKey(Account, on_delete =models.CASCADE)
    token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    useragent = models.TextField(default="")

class Productinfo(models.Model):
    Last_Updated = models.DateField(default="")
    Link = models.TextField(max_length=3000, default="")
    Brand = models.CharField(max_length=255, default="")
    Model = models.CharField(max_length=255, default="")
    Image_Link = models.ImageField(max_length=3000, default="")
    Base_Price = models.CharField(max_length=55, default="")
    Type = models.CharField(max_length=255, default="")
    Assembly = models.CharField(max_length=255, default="")
    Included_Software = models.CharField(max_length=255, default="")
    ###extra feilds
    Nominal_Advertised_Size_inches_x = models.CharField(max_length=255, default="")
    Nominal_Advertised_Size_inches_y = models.CharField(max_length=255, default="")
    Nominal_Advertised_Size_mm_x = models.CharField(max_length=255, default="")
    Nominal_Advertised_Size_mm_y = models.CharField(max_length=255, default="")
    Max_Travel_inches_x = models.CharField(max_length=255, default="")
    Max_Travel_inches_y = models.CharField(max_length=255, default="")
    Max_Travel_inches_z = models.CharField(max_length=255, default="")
    Max_Travel_mm_x = models.CharField(max_length=255, default="")
    Max_Travel_mm_y = models.CharField(max_length=255, default="")
    Max_Travel_mm_z = models.CharField(max_length=255, default="")
    Max_Gantry_Clearance_inches = models.CharField(max_length=255, default="")
    Max_Gantry_Clearance_mm = models.CharField(max_length=255, default="")
    Overall_Table_Size_inches_x = models.CharField(max_length=255, default="")
    Overall_Table_Size_inches_y = models.CharField(max_length=255, default="")
    Overall_Table_Size_mm_x = models.CharField(max_length=255, default="")
    Overall_Table_Size_mm_y = models.CharField(max_length=255, default="")
    Footprint_inches_len = models.CharField(max_length=255, default="")
    Footprint_inches_wid = models.CharField(max_length=255, default="")
    Footprint_inches_hei = models.CharField(max_length=255, default="")
    Footprint_mm_len = models.CharField(max_length=255, default="")
    Footprint_mm_wid = models.CharField(max_length=255, default="")
    Footprint_mm_hei = models.CharField(max_length=255, default="")
    Shipping_Dimensions_inches_len = models.CharField(max_length=255, default="")
    Shipping_Dimensions_inches_wid = models.CharField(max_length=255, default="")
    Shipping_Dimensions_inches_hei = models.CharField(max_length=255, default="")
    Shipping_Dimensions_mm_len = models.CharField(max_length=255, default="")
    Shipping_Dimensions_mm_wid = models.CharField(max_length=255, default="")
    Shipping_Dimensions_mm_hei = models.CharField(max_length=255, default="")
    Weight_pound = models.CharField(max_length=255, default="")
    Weight_kilo = models.CharField(max_length=255, default="")
    Drive_Type_x = models.CharField(max_length=255, default="")
    Drive_Type_y = models.CharField(max_length=255, default="")
    Drive_Type_z = models.CharField(max_length=255, default="")
    Ball_Screw_Dia_x = models.CharField(max_length=255, default="")
    Ball_Screw_Dia_y = models.CharField(max_length=255, default="")
    Ball_Screw_Dia_z = models.CharField(max_length=255, default="")
    Drive_Motors_x = models.CharField(max_length=255, default="")
    Drive_Motors_y = models.CharField(max_length=255, default="")
    Drive_Motors_z = models.CharField(max_length=255, default="")
    Motion_Guide_x = models.CharField(max_length=255, default="")
    Motion_Guide_y = models.CharField(max_length=255, default="")
    Motion_Guide_z = models.CharField(max_length=255, default="")
    Resolution_inches = models.CharField(max_length=255, default="")
    Resolution_mm = models.CharField(max_length=255, default="")
    Materials_Gantry = models.CharField(max_length=255, default="")
    Materials_Bed = models.CharField(max_length=255, default="")
    Materials_Spoilboard = models.CharField(max_length=255, default="")
    Materials_Base = models.CharField(max_length=255, default="")
    Max_Cut_Speed_inches_min = models.CharField(max_length=255, default="")
    Max_Cut_Speed_mm_min = models.CharField(max_length=255, default="")
    Rapid_Feed_Rate_inches_min = models.CharField(max_length=255, default="")
    Rapid_Feed_Rate_mm_min = models.CharField(max_length=255, default="")
    Spindle_Type = models.CharField(max_length=255, default="")
    Spindle_Size = models.CharField(max_length=255, default="")
    Configuration = models.CharField(max_length=255, default="")
    Cooling = models.CharField(max_length=255, default="")
    Min_Spindle_Speed = models.CharField(max_length=255, default="")
    Max_Spindle_Speed = models.CharField(max_length=255, default="")
    Max_Collet_Size = models.CharField(max_length=255, default="")
    ATC = models.CharField(max_length=255, default="")
    ATC_Type = models.CharField(max_length=255, default="")
    hash_of_Tools = models.CharField(max_length=255, default="")
    Tool_Probe = models.CharField(max_length=255, default="")
    Power_Requirements_Volts = models.CharField(max_length=255, default="")
    Power_Requirements_Hz = models.CharField(max_length=255, default="")
    Power_Requirements_Amps = models.CharField(max_length=255, default="")
    Power_Requirements_Phase = models.CharField(max_length=255, default="")
    Controller = models.CharField(max_length=255, default="")
    PC_Required = models.CharField(max_length=255, default="")
    Laser = models.CharField(max_length=255, default="")
    Vacuum_Table = models.CharField(max_length=255, default="")
    _4th_Axis = models.CharField(max_length=255, default="")
    Pendant = models.CharField(max_length=255, default="")
    Waranty_Months = models.CharField(max_length=255, default="")
    Support = models.CharField(max_length=255, default="")
    Orgin = models.CharField(max_length=255, default="")



    def __str__(self):
        return self.Model
