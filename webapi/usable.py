import re
from decouple import config
import jwt
import random



def checkemailforamt(Email):
    emailregix = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.match(emailregix, Email)):

        return True

    else:
       return False




def passwordLengthValidator(passwd):
    if len(passwd) >= 8 and len(passwd) <= 20:
        return True

    else:
        return False


#Token Expire
def admintokenauth(token):

    try:
       
        my_token = jwt.decode(token,config('superadminkey'), algorithms=["HS256"])
        return my_token

    except jwt.ExpiredSignatureError:
        return False

    except:
        return False

def custumertokenauth(token):

    try:
       
        my_token = jwt.decode(token,config('customerkey'), algorithms=["HS256"])
        return my_token

    except jwt.ExpiredSignatureError:
        return False

    except:
        return False


def requireKeys(reqArray,requestData):
    try:
        for j in reqArray:
            if not j in requestData:
                return False
            
        return True

    except:
        return False


def allfieldsRequired(reqArray,requestData):
    try:
        for j in reqArray:
            if len(requestData[j]) == 0:
                return False

        
        return True

    except:
        return False

##both keys and required field validation

def keyValidation(keyStatus,reqStatus,requestData,requireFields):


    ##keys validation
    if keyStatus:
        keysStataus = requireKeys(requireFields,requestData)
        if not keysStataus:
            return {'status':False,'message':f'{requireFields} all keys are required'}



    ##Required field validation
    if reqStatus:
        requiredStatus = allfieldsRequired(requireFields,requestData)
        if not requiredStatus:
            return {'status':False,'message':'All Fields are Required'}



def emailrandomcodegenrator():

    randomcode = random.randint(99999,9999999)
    return randomcode