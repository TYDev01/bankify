from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from register.models import UserForm, Account
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from register.forms import DepositForm
from register.models import Deposit

# Create your views here.
# @login_required
def dashboard_view(request):
    user = request.user
    user_form, created = UserForm.objects.get_or_create(
        username=user.username,
        defaults={
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'password': user.password,
            'phonenumber': '',  # Set default or handle separately
        }
    )

    # Get account or handle the case where it's missing
    account = getattr(user_form, 'account', None)
    if not account:
        account = Account.objects.create(user=user_form)

    context = {
        'username': user.username,
        'account_number': account.account_number,
        'balance': account.balance,
    }
    return render(request, 'dashboard/index.html', context)


# Deposit View
@login_required
def deposit(request):
    user = request.user

    try:
        # Fetch the UserForm associated with the logged-in user
        user_form = UserForm.objects.get(username=user.username)

        # Fetch the user's account
        account = Account.objects.get(user=user_form)

        if request.method == 'POST':
            amount = request.POST.get('amount')

            # Ensure the amount is valid
            if not amount or float(amount) <= 0:
                messages.error(request, "Invalid deposit amount!")
                return redirect('deposit')

            # Create a deposit record for admin approval (using user_form, not account)
            Deposit.objects.create(user=user_form, amount=amount)

            messages.success(request, "Deposit request submitted successfully! Awaiting admin approval.")
            return redirect('dashboard')

    except UserForm.DoesNotExist:
        messages.error(request, "User profile not found!")
        return redirect('signin')

    except Account.DoesNotExist:
        messages.error(request, "Account not found!")
        return redirect('dashboard')

    return render(request, 'dashboard/deposit.html')





@staff_member_required
def approve_deposit(request, deposit_id):
    deposit = get_object_or_404(Deposit, id=deposit_id)
    if not deposit.is_approved:
        deposit.approve()
        messages.success(request, f"Deposit of {deposit.amount} has been approved.")
    else:
        messages.warning(request, "Deposit is already approved.")
    return redirect('admin_dashboard')  # Replace 'admin_dashboard' with your admin view



def logout_user(request):
    logout(request)
    return redirect('register:signin')