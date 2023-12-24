# Microservice

# Setup the project

## Clone the Repository:
Start by cloning the repository to your local machine:

```sh
git https://github.com/parthsoni2909/Microservice.git
```

## Check the python version
```sh
python --version
```

## If you have not python then install the python
```sh
Visit the official Python website at https://www.python.org/, and go to the "Downloads" section. Choose the latest version of Python for Windows, and download the installer 
```

## create a viertual environment
```sh
pip install virtualenv
python -m venv venv
```

## Activate virtual environment
```sh
venv\Scripts\activate
```

## Install requirenment.txt
```sh
pip install -r requirenment.txt
```

## Run the Project
```sh
python manage.py runserver
```

## Create a super admin user
```sh
python manage.py createsuperuser
```

## Admin Panel URL
```sh
http://localhost:8000/admin/
```

## API collection
```sh
http://localhost:8000/api-docs/
```

## Project description

## API End-Points:

1. http://localhost:8000/api/v1/users/register/ - API for User Registration.
    ### Sample Request Data
        {
            "first_name": "Parth",
            "last_name": "Soni",
            "email": "soniparth2909@gmail.com",
            "phone_number": 919427654588,
            "password": "Secure@098"
        }
    ### Success Response Data
        {
            "success": true,
            "message": "User register successfully. PLease check you email for the account verification."
        }

2. http://localhost:8000/api/v1/users/AccountVetification/ - API for User Account verify.
    ### Sample Request Data
        {
            "email": "soniparth2909@gmail.com",
            "otp": "921359"
        }

    ### Success Response Data
        {
            "success": true,
            "message": "Your account verified successfully"
        }
    
    ### Invadil OTP Response Data
        {
            "success": false,
            "message": "Invalid OTP"
        }
    
    ### Invadil Eamil Response Data
        {
            "success": false,
            "message": "Invalid Email Address"
        }

3. http://localhost:8000/api/v1/users/LogInOTP/ - API for get otp via SMS for login.
    ### Sample Request Data
        {
            "phone_number": "919427654588"
        }

    ### Success Response Data
        {
            "success": true,
            "message": "OTP sent successfully"
        }
    
    ### User not found with thw phone number Response Data
        {
            "success": false,
            "message": "User not found with this phone number"
        }

4. http://localhost:8000/api/v1/users/LogIn/ - API for login.
    ### Sample Request Data
        {
            "phone_number": "919427654588",
            "otp": "661163"
        }

    ### Success Response Data
        {
            "success": true,
            "message": "Loggedin successfully",
            "payload": {
                "id": 2,
                "token": "3383e07d5af243fc9de2c966cff129959f7e410b",
                "first_name": "Parth",
                "last_name": "Soni",
                "email": "soniparth2909@gmail.com",
                "phone_number": 919427654588,
                "password": "pbkdf2_sha256$320000$MtHS1aaIdwNwiW2847J5A6$c/9U6LYZdzFS6Wi5OKZ4NQ2pDsqCFc/NhIcwB78fAy8="
            }
        }
    
    ### Invadil OTP Response Data
        {
            "success": false,
            "message": "Invalid OTP"
        }
    
    ### Invadil Eamil Response Data
        {
            "success": false,
            "message": "Invalid Phone number"
        }

5. http://localhost:8000/api/v1/users/GetUser/ - API for get user data.
    ### Success Response Data
        {
            "success": true,
            "message": "Get User Data Successfully",
            "payload": {
                "id": 2,
                "token": "3383e07d5af243fc9de2c966cff129959f7e410b",
                "first_name": "Parth",
                "last_name": "Soni",
                "email": "soniparth2909@gmail.com",
                "phone_number": 919427654588,
                "password": "pbkdf2_sha256$320000$MtHS1aaIdwNwiW2847J5A6$c/9U6LYZdzFS6Wi5OKZ4NQ2pDsqCFc/NhIcwB78fAy8="
            }
        }

6. http://localhost:8000/api/v1/users/UpdateUserAccount/{user_id}/ - API for update user data. Only Admin User role Access this API.

    ### Sample Request Data
        {
            "first_name": "Parth S",
            "last_name": "Soni",
            "phone_number": 916355361115
        }

    ### Success Response Data
        {
            "success": true,
            "message": "Account information updated successfully",
            "payload": {
                "first_name": "Parth S",
                "last_name": "Soni",
                "phone_number": 916355361115
            }
        }

    ### If you have no permission to this API
        {
            "detail": "You do not have permission to perform this action."
        }


7. http://localhost:8000/api/v1/users/ChangePassword/{user_id}/ - API for change password. Only Admin User role Access this API.

    ### Sample Request Data
        {
            "old_password": "Secure@098",
            "new_password": "Parth@2909"
        }

    ### Success Response Data
        {
            "success": true,
            "message": "Your Password Changed Successfully."
        }
    
    ### Old Password wrong Response Data
        {
            "success": false,
            "meaasage": "Old password id wrong"
        }

    ### New Password is same as old password Response Data
        {
            "success": false,
            "message": "New password cannot be the same as the old password."
        }
    
    ### If you have no permission to this API
        {
            "detail": "You do not have permission to perform this action."
        }

8. http://localhost:8000/api/v1/users/ResetPasswordEmail/ - API for request reset password.
    ### Sample Request Data
        {
            "email": "soniparth2909@gmail.com"
        }

    ### Success Response Data
        {
            "success": true,
            "message": "Password reset link sent to your email address. Please check your email."
        }
    
    ### Email wrong Response Data
        {
            "success": false,
            "message": "User not found with the provided email address."
        }

9. http://localhost:8000/api/v1/users/ResetPassword/ - API for reset password.
    ### Sample Request Data
        {
            "email": "soniparth2909@gmail.com",
            "password": "Secure@098"
        }

    ### Success Response Data
        {
            "success": true,
            "message": "User Password Updated"
        }