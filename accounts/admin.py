from django.contrib import admin
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_users']

def approve_users(self, request, queryset):
    print("=== Approve Users Action Triggered ===")
    queryset.update(is_approved=True)

    for user in queryset:
        try:
            send_mail(
                'Account Approved',
                f'Hello {user.first_name}, your account has been approved.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            print(f"Email sent to: {user.email}")
        except Exception as e:
            print(f"Error sending email to {user.email}: {e}")

    self.message_user(request, "Selected users have been approved")

admin.site.register(CustomUser, CustomUserAdmin)
