from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout




def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("admin_dashboard")
            if user.is_approved:
                return redirect("user_dashboard")
            else:
                messages.error(request, 'Your account is not approved yet.')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')



def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def admin_dashboard(request):
    pending_users = CustomUser.objects.filter(is_approved=False)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        
        try:
            user = CustomUser.objects.get(id=user_id)
            if action == 'approve':
                user.is_approved = True
                user.save()
                
                
                send_mail(
                    'Your account has been approved!',
                    'Hello, your account has been approved. You can now log in to the platform.',
                    'mahanorali124@gmail.com',  
                    [user.email],  
                    fail_silently=False,
                )
                messages.success(request, f'User {user.username} has been approved.')
            elif action == 'reject':
                user.delete() 
                messages.success(request, f'User {user.username} has been rejected and removed.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
        
        return redirect('admin_dashboard')
    
    return render(request, 'admin_dashboard.html', {'pending_users': pending_users})


def user_logout(request):
    logout(request)
    return redirect("home")

def user_dashboard(request):
    return render(request, "user_dashboard.html")