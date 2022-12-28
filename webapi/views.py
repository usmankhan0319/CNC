from lib2to3.pytree import Base
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from django.conf import settings
import webapi.usable as uc
from .models import *
from passlib.hash import django_pbkdf2_sha256 as handler
import jwt 
import datetime
from decouple import config
import webapi.emailpattern as em
import pandas as pd
import csv
from django.db.models import Q



# Create your views here.


###signup
class Signup(APIView):
    def post(self, request):
        try:

            requireFields = ['Fname','Lname','Email','Password','ContactNo','Profile','Role']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            
            if validator:
                return Response(validator,status = 200)
            else:
                Fname = request.data.get('Fname')
                Lname = request.data.get('Lname')
                Email = request.data.get('Email')
                Password = request.data.get('Password')
                ContactNo = request.data.get('ContactNo')
                Role = request.data.get('Role')
                Profile = request.data.get('Profile')

                if Role == 'superadmin':
                    if uc.checkemailforamt(Email):
                        if not uc.passwordLengthValidator(Password):
                            return Response({"status":False,"message":"Password should not be less than 8 or greater than 20"})
                        checkemail = Account.objects.filter(Email = Email).first()
                        if checkemail:
                            return Response({"status":False,"message":"Email alreay exist"})
                        checkphone = Account.objects.filter(ContactNo = ContactNo).first()
                        if checkphone:
                            return Response({"status":False,"message":"Phone number already registered please enter different number"})
                        
                        data = Account(Fname=Fname,Lname=Lname,Email=Email,Password=handler.hash(Password),ContactNo=ContactNo,Role=Role,Profile=Profile)
                        data.save()
                        return Response({"status":True,"message":"Account Created Successfully"})
                    else:
                        return Response({"status":False,"message":"Email Format Is Incorrect"})
                else:
                    my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
                    if my_token:
                        if not uc.checkemailforamt(Email):
                            return Response({"status":False,"message":"Email Format Is Incorrect"})
                        if not uc.passwordLengthValidator(Password):
                            return Response({"status":False,"message":"Password should not be less than 8 or greater than 20"})

                        checkemail = Account.objects.filter(Email = Email).first()
                        if checkemail:
                            return Response({"status":False,"message":"Email alreay exist"})
                
                        checkphone = Account.objects.filter(ContactNo = ContactNo).first()
                        if checkphone:
                            return Response({"status":False,"message":"Phone number already registered please enter different number"})

                        data = Account(Fname=Fname,Lname=Lname,Email=Email,Password=handler.hash(Password),ContactNo=ContactNo,Role=Role,Profile=Profile)
                        data.save()
                        return Response({"status":True,"message":"Account Created Successfully"})
                    else:
                        return Response({"status":False,"message":"Unauthenticated"})
        
        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)


###customer Signup byself
class cus_signup(APIView):
    def post(self, request):
        try:

            requireFields = ['Fname','Lname','Email','Password','ContactNo','Profile']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            
            if validator:
                return Response(validator,status = 200)
            else:
                Fname = request.data.get('Fname')
                Lname = request.data.get('Lname')
                Email = request.data.get('Email')
                Password = request.data.get('Password')
                ContactNo = request.data.get('ContactNo')
                Profile = request.data.get('Profile')

                if uc.checkemailforamt(Email):
                    if not uc.passwordLengthValidator(Password):
                        return Response({"status":False,"message":"Password should not be less than 8 or greater than 20"})
                    checkemail = Account.objects.filter(Email = Email).first()
                    if checkemail:
                        return Response({"status":False,"message":"Email alreay exist"})
                    checkphone = Account.objects.filter(ContactNo = ContactNo).first()
                    if checkphone:
                        return Response({"status":False,"message":"Phone number already registered please enter different number"})
                    
                    data = Account(Fname=Fname,Lname=Lname,Email=Email,Password=handler.hash(Password),ContactNo=ContactNo,Role='customer',Profile=Profile)
                    data.save()
                    return Response({"status":True,"message":"Signup Successfully"})
                else:
                    return Response({"status":False,"message":"Email Format Is Incorrect"})

        
        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)





###login, update , delete
class login (APIView):
    ###superadmin get
    def get(self,request):
        try:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                data = Account.objects.filter(SId = my_token['id']).first()
                if data:
                    obj = ({"SId": data.SId, "Fname": data.Fname, "Lname": data.Lname , "Email":data.Email, "ContactNo":data.ContactNo, "Role":data.Role, "Profile":str(data.Profile)})  ###,"Profile":data.Profile.url0
                    return Response({"status":True,"data":obj})
                else:
                    return Response({"status":False,"message":"Account not Found"})
            else:
                return Response({"status":False,"message":"Unauthenticated"})


        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)

    def post(self,request):
        try: 
            requireFields = ['Email','Password']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            
            if validator:
                return Response(validator,status = 200)
            
            else:
                Email = request.data.get('Email')
                Password = request.data.get('Password')
                fetchAccount = Account.objects.filter(Email=Email).first()
                if fetchAccount:
                    if handler.verify(Password,fetchAccount.Password):
                        if fetchAccount.Role == "superadmin":

                            
                            access_token_payload = {
                                    'id':fetchAccount.SId,
                                    'Fname':fetchAccount.Fname, 
                                    'email':fetchAccount.Email, 
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                    'iat': datetime.datetime.utcnow(),

                                }

                            
                            access_token = jwt.encode(access_token_payload,config('superadminkey'),algorithm = 'HS256')
                            data = {'SId':fetchAccount.SId,'Fname':fetchAccount.Fname,'Lname':fetchAccount.Lname,'Email':fetchAccount.Email,'ContactNo':fetchAccount.ContactNo,'Role':fetchAccount.Role,'Profile':fetchAccount.Profile.url}

                            whitelistToken(user = fetchAccount,token = access_token,useragent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now()).save()

                            
                            return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data})

                        elif fetchAccount.Role == "customer":
                            
                            access_token_payload = {
                                        'id':fetchAccount.SId,
                                            'Fname':fetchAccount.Fname, 
                                            'email':fetchAccount.Email, 
                                            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                            'iat': datetime.datetime.utcnow(),
                                            }

                            access_token = jwt.encode(access_token_payload,config('customerkey'),algorithm = 'HS256')
                            data = {'SId':fetchAccount.SId,'Fname':fetchAccount.Fname,'Lname':fetchAccount.Lname,'Email':fetchAccount.Email,'ContactNo':fetchAccount.ContactNo,'Role':fetchAccount.Role,'Profile':str(fetchAccount.Profile)}

                            whitelistToken(user = fetchAccount,token = access_token,useragent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now()).save()

                            return Response({"status":True,"message":"Login Successlly","token":access_token,"businessdata":data})

                        else:
                            return Response({"status":False,"message":"Please Enter correct role"})
                    else:
                        return Response({"status":False,"message":"Please Enter a correct Password"})
                else:
                    return Response({"status":False,"message":"Please Enter a correct email"})
        
        
        
        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)




    ###update profile
    def put (self,request):
        try:
            requireFields = ['SId','Fname','Lname','ContactNo','Profile']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            
            if validator:
                return Response(validator,status = 200)
            else:
                my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
                if my_token:
                    SId = request.data.get('SId')
                    Fname = request.data.get('Fname')
                    Lname = request.data.get('Lname')
                    ContactNo = request.data.get('ContactNo')
                    Profile = request.data.get('Profile')
                    checkaccount = Account.objects.filter(SId = SId).first()
                    if checkaccount:
                        checkaccount.Fname =Fname
                        checkaccount.Lname =Lname
                        checkaccount.ContactNo = ContactNo

                        if request.data.get('Profile',False):
                            checkaccount.Profile = request.data.get('Profile')

                        checkaccount.save()
                        return Response({"status":True,"message":"Account Updated Successfully"})
                    else:
                        return Response({"status":True,"message":"Data not found"})
                else:
                    my_token = uc.custumertokenauth(request.META['HTTP_AUTHORIZATION'][7:])
                    if my_token:
                        SId = request.data.get('SId')
                        checkaccount = Account.objects.filter(SId = SId).first()
                        if checkaccount:
                            checkaccount.Fname = request.data.get('Fname') 
                            checkaccount.Lname = request.data.get('Lname') 
                            checkaccount.ContactNo = request.data.get('ContactNo')

                            if request.data.get('Profile',False):
                                checkaccount.Profile = request.data.get('Profile')

                            checkaccount.save()
                            return Response({"status":True,"message":"Account Updated Successfully"})
                        else:
                            return Response({"status":True,"message":"Data not found"})
                    else:
                        return Response({"status":False,"message":"Unauthenticated"})
       
       
        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)



    ###delete customer
    def delete(self,request):
        try:
            requireFields = ['SId']
            validator = uc.keyValidation(True,True,request.GET,requireFields)
            
            if validator:
                return Response(validator,status = 200)
            else:
                my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
                if my_token:
                    SId = request.GET['SId']
                    data = Account.objects.filter(SId=SId).first()
                    if data:
                        data.delete()
                        return Response({"status":True,"message":"Account Deleted Successfully"})
                    else:
                        return Response({"status":False,"message":"Account not Found"})
                else:
                    return Response({"status":False,"message":"Unauthenticated"})
        
        
        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)



###update customer 
class updatecustomer(APIView):
    def put (self,request):
        try:
            requireFields = ['SId','Fname','Lname','ContactNo']
            validator = uc.keyValidation(True,True,request.data,requireFields)
                
            if validator:
                return Response(validator,status = 200)
            else:
                my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
                if my_token:
                    SId = request.data.get('SId')
                    Fname = request.data.get('Fname')
                    Lname = request.data.get('Lname')
                    ContactNo = request.data.get('ContactNo')

                    checkaccount = Account.objects.filter(SId = SId).first()
                    if checkaccount:
                        checkaccount.Fname = Fname
                        checkaccount.Lname = Lname
                        checkaccount.ContactNo = ContactNo
                        checkaccount.save()
                        return Response({"status":True,"message":"Account Updated Successfully"})
                    else:
                        return Response({"status":False,"message":"Account not found"})
                else:
                    return Response({"status":True,"message":"Unauthenticated"})

        

        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)




###change password
class UpdatePassword(APIView):

    def put(self,request):
        try:
            ###superadmin
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                requireFields = ['Password','oldpassword']
                validator = uc.keyValidation(True,True,request.data,requireFields)
                if validator:
                    return Response(validator,status=200)
                else:
                    Password = request.data.get('Password')
                    oldpassword = request.data.get('oldpassword')
                    data = Account.objects.filter(SId = my_token['id']).first()
                    if handler.verify(request.data['oldpassword'],data.Password):
                    ##check if user again use old password
                        if not handler.verify(request.data['Password'],data.Password):     
                            checkpassword = uc.passwordLengthValidator(request.POST['Password'])
                            if not checkpassword:
                                return Response({'status':False,'message':'Password must be 8 or less than 20 characters'})
                            
                            data.Password = handler.hash(Password)
                            data.save()
                            return Response({'status':True,'message':'Change Password Successfully'})
                        else:
                            return Response({'status':False,'message':'You choose old password try another one'})
                    else:
                        return Response({'status':False,'message':'You old password is incorrect'})

            ###customer
            else:
                my_token = uc.custumertokenauth(request.META['HTTP_AUTHORIZATION'][7:])
                if my_token:
                    requireFields = ['Password','oldpassword']
                    validator = uc.keyValidation(True,True,request.data,requireFields)
                    if validator:
                        return Response(validator,status=200)
                    else:
                        Password = request.data.get('Password')
                        oldpassword = request.data.get('oldpassword')
                        data = Account.objects.filter(SId = my_token['id']).first()
                        if handler.verify(oldpassword,data.Password):
                        ##check if user again use old password
                            if not handler.verify(Password,data.Password):
                                checkpassword = uc.passwordLengthValidator(request.POST['Password'])
                                if not checkpassword:
                                    return Response({'status':False,'message':'Password must be 8 or less than 20 characters'})
                                
                                data.Password = handler.hash(Password)
                                data.save()
                                return Response({'status':True,'message':'Change Password Successfully'})
                            else:
                                return Response({'status':False,'message':'You choose old password try another one'})
                        else:
                            return Response({'status':False,'message':'You old password is incorrect'})


        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)




###customer get profile
class customer_profile(APIView):
    
    def get(self,request):
        try:
            my_token = uc.custumertokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                data = Account.objects.filter(SId = my_token['id']).first()
                if data:
                    obj = ({"SId": data.SId, "Fname": data.Fname, "Lname": data.Lname , "Email":data.Email, "ContactNo":data.ContactNo, "Role":data.Role, "Profile":str(data.Profile)})  ###,"Profile":data.Profile.url0
                    return Response({"status":True,"data":obj})
                else:
                    return Response({"status":False,"message":"Account not Found"})
            else:
                return Response({"status":False,"message":"Unauthenticated"})


        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)



####forget password
class forgetpasswords (APIView):

    def post(self,request):
        try:
            requireFields = ['Email']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            if validator:
                return Response(validator,status=200)
            else:
                Email = request.data.get('Email')
                checkEmailExist = Account.objects.filter(Email=Email).first()
                if checkEmailExist:
                    token = uc.emailrandomcodegenrator()
                    checkSendEmail = em.forgetPassword('Account Recovery',config('fromemail'),Email,token)
                    checkEmailExist.Otp = token
                    checkEmailExist.OtpStatus = "True"
                    checkEmailExist.OtpCount = 0
                    checkEmailExist.save()
                    return Response({'status':True,'message':"Please Check Your Email",'Email':Email})
                else:
                    return Response({'status':False,'message':"Email Doesnot Exist"})



        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)



class VerifyCode(APIView):

    def post(self,request):
        try:

            requireFields = ['Email','Code']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            if validator:
                return Response(validator,status=200)
            else:
                Email = request.data.get('Email')
                Code = int(request.data.get('Code'))
                userObj = Account.objects.filter(Email=Email).first()
                if userObj:
                    if userObj.OtpStatus == "True":
                        if userObj.OtpCount < 5:
                            if userObj.Otp == Code:
                                userObj.OtpCount = 0
                                userObj.OtpStatus = "False"
                                userObj.passwordstatus = "False"
                                userObj.save()
                                return Response({'status':True,'message':"Access Granted",'Email':Email})
                            else:
                                userObj.OtpCount = userObj.OtpCount + 1
                                userObj.save()
                                return Response({'status':False,'message':"Invalid Code"})
                        else:
                            return Response({'status':False,'message':"Code is expire"})
                    else:
                        return Response({'status':False,'message':"Code is expire"})
                else:
                    return Response({'status':False,'message':"Account Doesnot Exist"})



        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)



class ChangePassword(APIView):

    def post(self,request):
        try:
            requireFields = ['Email','Password']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            if validator:
                return Response(validator,status=200)
            else:
                Email = request.data.get('Email')
                Password = request.data.get('Password')
                if Email:
                    checkpassword = uc.passwordLengthValidator(request.POST['Password'])
                    if not checkpassword:
                        return Response({'status':False,'message':'Password must be 8 or less than 20 characters'})
                    data = Account.objects.filter(Email=Email).first()
                    if data:
                        if data.passwordstatus == "False":
                            data.Password = handler.hash(Password)
                            data.passwordstatus = "True"
                            data.save()
                            return Response({'status':True,'message':'Password Change Sussessfully'})
                        else:
                            return Response({'status':False,'message':"You have not rights to change Password Please follow the steps"})     

                    else:
                        return Response({'status':False,'message':"Email Doesnot Exist"})
                else:
                    return Response({'status':False,'message':"You have not rights to change Password Please follow the steps"})


        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)



###customer all data
class GetCustomerData(APIView):
    def get (self, request):
        try:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                data = Account.objects.filter(Role="customer").values('SId','Fname','Lname','Email','Password','ContactNo','Profile','Role').order_by('-SId')
                return Response({"status":True,"data":data})
            else:
                return Response({"status":False,"message":"Unauthenticated"})


        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)


###all products
class getProductData(APIView):
    def get (self, request):
        try:
            data = Productinfo.objects.values('id','Last_Updated','Link','Brand','Model','Image_Link','Base_Price','Type','Assembly','Included_Software').order_by('-id')
            return Response({"status":True,"data":data})


        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)
             


# class Logout(APIView):
#      def post(self,request):
#         try:
#             my_token = uc.custumertokenauth(request.META['HTTP_AUTHORIZATION'][7:])
#             if my_token:
#                 requirePassword = request.POST.get('password',False)
#                 tokencatch = request.META['HTTP_AUTHORIZATION'][7:]
#                 getWhistlisttoken = whitelistToken.objects.get(user =  my_token['id'],token = tokencatch)
#                 if not requirePassword:
#                     getWhistlisttoken.delete()
#                     return Response({"status":True,"message":"logout successfully"})
#                 else:
#                     data = Account.objects.filter(uid = request.GET['token']['id']).first()
#                     if data:
#                         if handler.verify(requirePassword,data.password):
#                             getWhistlisttoken.delete()
#                             return Response({"status":True,"message":"logout another browser successfully"})
#                         else:
#                             return Response({'status':False,'message':'Password is Wrong'})
#                     else:
#                         return Response({'status':False,'message':'something went wrong','details':'User doesnot exist'})


#         except Exception as e:
#             message = {'status':False}
#             message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
#             return Response(message,status=500)



class uploadcsv(APIView):

    def post (self,request): 
        try:
            file = request.FILES.get("file")
            if not file:
                return Response({'status':'warning','message':'File is required'})
            
            if not file.name.endswith('csv'):
                return Response({'status':False,'message':"Your File Format is Incorrect"})

            columnFormat = ['last_updated', 'link', 'brand', 'model', 'image_link', 'base_price','type', 'assembly', 'included_software']
            convertDataFrame = pd.read_csv(file)
            convertDataFrame = pd.DataFrame(convertDataFrame)
            ###remove duplicate from upload file
            bool_series = convertDataFrame["Model"].duplicated(keep = 'first')
            convertDataFrame = convertDataFrame[~bool_series]# passing NOT of bool series to see unique values only

            convertDataFrame.columns = [x.lower() for x in convertDataFrame.columns]
            dataColumns = convertDataFrame.columns
            # print("columnFormat",columnFormat)
            # print("dataColumns",dataColumns)
            if list(dataColumns) == columnFormat:
                LastUpdated = convertDataFrame[columnFormat[0]]
                Link = convertDataFrame[columnFormat[1]]
                Brand = convertDataFrame[columnFormat[2]]
                Model = convertDataFrame[columnFormat[3]]
                ImageLink = convertDataFrame[columnFormat[4]]
                BasePrice= convertDataFrame[columnFormat[5]]
                Type = convertDataFrame[columnFormat[6]]
                Assembly = convertDataFrame[columnFormat[7]]
                IncludedSoftware = convertDataFrame[columnFormat[8]]

                bulklist = list()
                # for a,b,c,d,e,f,g,h,i in zip(LastUpdated,Link,Brand,Model,ImageLink,BasePrice,Type,Assembly,IncludedSoftware):
                #     bulklist.append(Productinfo(Last_Updated=a,Link=b,Brand=c,Model=d,Image_Link=e,Base_Price=f,Type=g,Assembly=h,Included_Software=i))
                for a,b,c,d,e,f,g,h,i in zip(LastUpdated,Link,Brand,Model,ImageLink,BasePrice,Type,Assembly,IncludedSoftware):
                    Productinfo.objects.filter(Model=d).delete()  ###delete duplicate from database         
                    bulklist.append(Productinfo(Last_Updated=a,Link=b,Brand=c,Model=d,Image_Link=e,Base_Price=f,Type=g,Assembly=h,Included_Software=i))
            
                Productinfo.objects.bulk_create(bulklist)
                return Response({'status':True,'message':"Data Uploaded Successfully"})


            else:
                return Response({'status':False,'message':"Your File Column Format is Incorrect"},)



        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))if settings.DEBUG else message.update(message='Internal server error')
            return Response(message,status=500)




class product(APIView):

    def get (self, request):
        my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
            data = Productinfo.objects.values('id','Last_Updated','Link','Brand','Model','Image_Link','Base_Price','Type','Assembly','Included_Software').order_by('-id')
            return Response({"status":True,"data":data})
        else:
            return Response({"status":False,"message":"Unauthenticated"})

    def post(self, request):
        requireFields = ['Last_Updated','Link','Brand','Model','Image_Link','Base_Price','Type','Assembly','Included_Software']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        if validator:
            return Response(validator)
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                Model = request.data.get('Model')
                checkdulp = Productinfo.objects.filter(Model=Model).first()
                if checkdulp:
                    return Response({"status":False, "message": "Duplicate Model"})
                else:
                
                    Last_Updated = request.data.get('Last_Updated')
                    Link = request.data.get('Link')
                    Brand = request.data.get('Brand')
                    Image_Link = request.data.get('Image_Link')
                    Base_Price = request.data.get('Base_Price')
                    Type = request.data.get('Type')
                    Assembly = request.data.get('Assembly')
                    Included_Software = request.data.get('Included_Software')

                    data = Productinfo(Last_Updated=Last_Updated, Link=Link, Brand=Brand, Model=Model, Image_Link=Image_Link, Base_Price=Base_Price, Type=Type, Assembly=Assembly, Included_Software=Included_Software)
                    data.save()

                    return Response({"status":True, "message":"Added Succesfully"})
            else:
                return Response({"status":False, "message":"Unauthenticated"})




    def put (self,request):
        requireFields = ['id','Last_Updated','Link','Brand','Model','Image_Link','Base_Price','Type','Assembly','Included_Software']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                Model = request.data.get('Model')
                checkdulp = Productinfo.objects.filter(Model=Model).first()
                if checkdulp:
                    return Response({"status":False, "message": "Duplicate Model"})
                else:
                    id = request.data.get('id')
                    
                    checkproduct = Productinfo.objects.filter(id = id).first()
                    if checkproduct:
                        checkproduct.Last_Updated = request.data.get('Last_Updated') 
                        checkproduct.Link = request.data.get('Link') 
                        checkproduct.Brand = request.data.get('Brand')
                        checkproduct.Image_Link = request.data.get('Image_Link')
                        checkproduct.Base_Price = request.data.get('Base_Price')
                        checkproduct.Type = request.data.get('Type')
                        checkproduct.Assembly = request.data.get('Assembly')
                        checkproduct.Included_Software = request.data.get('Included_Software')

                        checkproduct.save()
                        return Response({"status":True,"message":"Account Updated Successfully"})
                    else:
                        return Response({"status":True,"message":"Data not found"})
            else:
                return Response({"status":True,"message":"Unauthenticated"})




    def delete(self,request):
        requireFields = ['id']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        else:
            my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET['id']
                data = Productinfo.objects.filter(id=id).first()
                if data:
                    data.delete()
                    return Response({"status":True,"message":"Product Deleted Successfully"})
                else:
                    return Response({"status":False,"message":"Product not Found"})
            else:
                return Response({"status":False,"message":"Unauthenticated"})