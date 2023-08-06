=====
OTP
=====

Contains otp model

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "otp" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'otp',
    ]

2. In settings.py add 

    #Time after which new OTP can be requested after exceeding max incorrect attempts
    OTP_BLOCK_WINDOW_MIN = int(os.environ.get('OTP_BLOCK_WINDOW_MIN', 15))
     
    
    
    # max wrong attempts allowed for an otp
    OTP_REMAINING_ATTEMPTS = int(os.environ.get('OTP_REMAINING_ATTEMPTS', 5))
    


