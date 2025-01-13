from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import uuid
from utils import random_account_number
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Create your models here.
#=================== Create an Account =====================
class UserForm(models.Model):

    firstname = models.CharField(max_length=50, default="firstname")

    lastname = models.CharField(max_length=50, default="lastname")

    username = models.CharField(max_length=50, default="username")

    email = models.EmailField(max_length=70, unique=True, default="email")

    password = models.CharField(max_length=128)

    phonenumber = models.CharField(max_length=15, unique=True, default="phonenumber")


    def save(self, *args, **kwargs):
        # Call the parent save method
        super().save(*args, **kwargs)

        # Check if an Account exists for this UserForm; if not, create one
        if not hasattr(self, 'account'):
            Account.objects.create(user=self)

    def __str__(self):
        account_number = self.account.account_number if hasattr(self, 'account') else "No Account"
        return f'{self.username} - Account Number: {account_number}'

    # def __str__(self):
    #     account_number = self.account.account_number
    #     if hasattr(self, 'account'):
    #         account_number = self.acc
    #     else:
    #         account_number = 'No Account'
    #     return f'{self.username} -Account Number: {account_number}'

    def __str__(self):
    # Check if the account relationship exists
        account_number = getattr(self, 'account', None)
        if account_number:
            account_number = account_number.account_number
        else:
            account_number = 'No Account'
        return f'{self.username} - Account Number: {account_number}'
    
    
            
#================ Sign IN ================================
class SignIn(models.Model):
    username = models.CharField(max_length=50, default="username")
    password = models.CharField(max_length=15, default="password")
    
    # def check_password(self, raw_password):
    #     return check_password(raw_password, self.password)
        
    # def check_username():

#================ Account ============
#We are using a one to one field because we are only allowing a user to have only ONE account
class Account(models.Model):
    user = models.OneToOneField(UserForm, on_delete=models.CASCADE)  # One-to-One relationship with User
    account_number = models.CharField(max_length=255, null=True, unique=True, default=random_account_number, editable=False)      # Unique account number
    # account_number = random_account_number()
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Balance field

    def __str__(self):
        return f"{self.user}"

#================ Transfer ================================
class Transfer(models.Model):
    sender_name = models.ForeignKey(Account, related_name='sender_name', on_delete=models.CASCADE)
    receiver_name = models.ForeignKey(Account, related_name='receiver_name', on_delete=models.CASCADE)
    account_number = models.ForeignKey(Account, related_name='account', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    

@receiver(post_save, sender=User)
def create_user_form(sender, instance, created, **kwargs):
    if created:
        UserForm.objects.create(
            firstname=instance.first_name,
            lastname=instance.last_name,
            username=instance.username,
            email=instance.email,
            phonenumber="",  # Set a default or prompt user to update
            password=instance.password,
        )



class Deposit(models.Model):
    user = models.ForeignKey(UserForm, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def approve(self):
        """Approve deposit and update account balance."""
        self.is_approved = True
        self.approved_at = timezone.now()
        self.save()
        self.user.account.balance += self.amount
        self.user.account.save()

    def __str__(self):
        return f"{self.user.username} - {self.amount} - Approved: {self.is_approved}"
