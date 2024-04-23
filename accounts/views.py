from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from django.contrib import messages
from .models import Project
from django.http import HttpResponseRedirect

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return render(request,'accounts/login.html') 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Get the role of the logged-in user
            try:
                account = Account.objects.get(user=user)
                role = account.role
                # Redirect based on role
                if role:
                    if Account.DEVELOPER:
                        return redirect('dev_dashboard')
                    elif Account.PROJECT_MANAGER:
                        return redirect('pm_dashboard')
                    elif Account.BOD:
                        return redirect('bod_dashboard')
                    elif Account.COO:
                        return redirect('coo_dashboard')
                    # elif _ :
                    #     # Default case if none of the above matches
                    #     return redirect('default_dashboard')
            except Account.DoesNotExist:
                messages.error(request, "User account not found.")
                return redirect('login')
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    if not request.user.is_authenticated:
        return redirect('login') 
  

@login_required
def dev_dashboard(request, required_role=None):
    # user_groups = request.user.groups.all()

    # print(request.user.account.role == 'dev')
    if not request.user.account.role == 'dev':
        # print("ppppp")
        return redirect('login') # Redirect to login if the user is not in the Developers group
    return render(request, 'dashboard/dev_dashboard.html')

@login_required
def pm_dashboard(request, required_role=None):
    if not request.user.account.role == 'pm':
        return redirect('login') # Redirect to login if the user is not in the Project Managers group
    return render(request, 'dashboard/pm_dashboard.html')

@login_required
def coo_dashboard(request, required_role=None):
    if not request.user.account.role == 'coo':
        return redirect('login') # Redirect to login if the user is not in the Chief Operating Officers group
    return render(request, 'dashboard/coo_dashboard.html')

@login_required
def bod_dashboard(request, required_role=None):
    if not request.user.account.role == 'bod':
        return redirect('login') # Redirect to login if the user is not in the Board of Directors group
    return render(request, 'dashboard/bod_dashboard.html')


def add_project(request):
    return render(request,'accounts/add_project.html')   



@login_required
def add_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        # Assuming the user is authenticated and you want to set the current user as the creator
        created_by = request.user

       
        # Create and save the project instance
        project = Project(project_name=project_name, created_by=created_by, created_at=created_at)
        created_at = request.POST.get('created_at') 
        project.save()

        # Redirect to a success page or back to the form
        return HttpResponseRedirect('/success/')
    else:
        # Handle the case where the request is not a POST request

        return render(request, 'add_project.html')


# def view_daily_assigned_task(request):
#     # request should contain username
#     # use the name to query the database
#     # fetch user id
#     # according to user id fetch all the information of the tasks



