"""
FDAWS User Management
Here FDAWs stands for Functions Doing All Work
Here all the major works and logic that a view will use will be implemented.

"""
from tenants.models import User


def get_user_details_for_dashboard(request) -> list:
    user_details = []
    user = request.user
    if user:
        user_details.append({
            "id": user.id,
            "name":user.name,
            "username":user.username,
            "email":user.email,
            "phone":str(user.phone_number) # django's PhoneNumberField stores the number as PhoneNumber object
        })
    return user_details
        
    
    
   
