from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile

def admin_required(view_func):
    """Decorator to require admin role"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        try:
            profile = request.user.userprofile
            if not profile.is_admin:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist (for existing users)
            UserProfile.objects.create(user=request.user, role='customer')
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def manager_required(view_func):
    """Decorator to require manager role or higher"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        try:
            profile = request.user.userprofile
            if not profile.has_role_or_higher('manager'):
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=request.user, role='customer')
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def staff_required(view_func):
    """Decorator to require staff role or higher"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        try:
            profile = request.user.userprofile
            if not profile.has_role_or_higher('staff'):
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=request.user, role='customer')
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def staff_or_higher_required(view_func):
    """Decorator to require staff role or higher (staff, manager, admin)"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        try:
            profile = request.user.userprofile
            if not profile.has_role_or_higher('staff'):
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=request.user, role='customer')
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def customer_or_admin_required(view_func):
    """Decorator to require either customer or admin role (authenticated users)"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist (for existing users)
            UserProfile.objects.create(user=request.user, role='customer')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(*allowed_roles):
    """Generic decorator to require specific roles"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('login')
            
            try:
                profile = request.user.userprofile
                if profile.role not in allowed_roles:
                    messages.error(request, 'You do not have permission to access this page.')
                    return redirect('home')
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=request.user, role='customer')
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
