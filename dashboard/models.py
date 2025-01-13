from django.db import models
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from register.models import UserForm


# class Deposit(models.Model):
#     user = models.ForeignKey(UserForm, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     approved_at = models.DateTimeField(null=True, blank=True)

#     def approve(self):
#         """Approve deposit and update account balance."""
#         self.is_approved = True
#         self.approved_at = timezone.now()
#         self.save()
#         self.user.account.balance += self.amount
#         self.user.account.save()

#     def __str__(self):
#         return f"{self.user.username} - {self.amount} - Approved: {self.is_approved}"
