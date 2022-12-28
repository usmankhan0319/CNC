from django.urls import path,include
from webapi.views import *

urlpatterns = [

#web urls  home
path('',Signup.as_view()),
path('Signup',Signup.as_view()),
path('login',login.as_view()),
###customer all data
path('GetCustomerData',GetCustomerData.as_view()),
###customer get profile
path('customer_profile',customer_profile.as_view()),
###customer Signup byself
path('cus_signup',cus_signup.as_view()),
###updatecustomer
path('updatecustomer',updatecustomer.as_view()),
###change password
path('UpdatePassword',UpdatePassword.as_view()),
###forget password
path('forgetpasswords',forgetpasswords.as_view()),
path('VerifyCode',VerifyCode.as_view()),
path('ChangePassword',ChangePassword.as_view()),
###all products
path('getProductData',getProductData.as_view()),
###logout
# path('Logout',Logout.as_view()),

# path('importfile',importfile.as_view()),
path('uploadcsv',uploadcsv.as_view()),
path('product',product.as_view()),

]





