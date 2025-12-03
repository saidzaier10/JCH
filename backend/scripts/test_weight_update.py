import os
import django
import sys

# Add project root to path
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Member
from rest_framework.test import APIRequestFactory
from core.views import MemberViewSet

def test_weight_update():
    # Get or create a member
    member = Member.objects.first()
    if not member:
        print("No members found to test.")
        return

    print(f"Testing update for member: {member.first_name} {member.last_name}")
    print(f"Current weight category: {member.weight_category}")

    # Create request
    factory = APIRequestFactory()
    data = {'weight_category': '-46'} # Testing a new official weight category
    request = factory.patch(f'/api/members/{member.id}/', data, format='json')
    
    # Force authentication (bypass for this test or mock user)
    # Ideally we use a proper test user, but for quick check:
    from django.contrib.auth.models import User
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("No admin user found.")
        return
        
    from rest_framework.test import force_authenticate
    
    view = MemberViewSet.as_view({'patch': 'partial_update'})
    force_authenticate(request, user=admin_user)
    
    response = view(request, pk=member.id)
    
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.data}")
    
    # Verify DB update
    member.refresh_from_db()
    print(f"New weight category in DB: {member.weight_category}")
    
    if member.weight_category == '-66':
        print("SUCCESS: Weight category updated.")
    else:
        print("FAILURE: Weight category NOT updated.")

if __name__ == '__main__':
    test_weight_update()
