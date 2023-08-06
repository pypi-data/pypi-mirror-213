
# AFEX SSO (DJANGO)




## Simple Integration (usage)

instantiate the SSO class


      from AFEX_SSO import SSO
      sso = SSO()

      def get_user_details(View):
        sso_instance = sso.check_credentials(session_key)
        get_user = sso_instance['data'].get('user')
        '''
            # other codes
        '''
      
       def logout(View):
           # get user email
            email = " "
            signout = sso.sign_out(email)
        '''
            # other codes
        '''

## Keys

- session_key : sent from the service provider client (frontend) after successful authentication on the sso 

## SETTINGS

- set the sso details on settings.py as shown below 
  - SSO_URL = ""
  - SSO_API_KEY = ""
  - SSO_SECRET_KEY = ""

### Sample Response

    {
    "responseCode": "100",
    "data": {
        "session_identifier": "SES_2c73ff51cfe5c5a68fc58934c9be3b",
        "user": {
            "email": "example@africaexchange.com",
            "first_name": "Ayodeji",
            "last_name": "Balogun",
            "photo": null,
            "tribe": null,
            "designation": "Software Developer",
            "email_aliases": [
                "example@afexnigeria.com",
            ]
        }
    },

    "message": "Successfully Retrieved"

    }


