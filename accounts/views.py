import datetime
from gc import get_stats
from sqlite3 import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, ProjectMembers, ProjectTasks
from django.contrib import messages
from .models import Project
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

# Create your views here.

from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from.models import Account  # Assuming Account model has a role field

def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/login.html')  # Assuming you have a dashboard template for authenticated users

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                account = Account.objects.get(user=user)
                role = account.role
                if role == Account.DEVELOPER:
                    return redirect('dev_dashboard')
                elif role == Account.PROJECT_MANAGER:
                    return redirect('pm_dashboard')
                elif role == Account.BOD:
                    return redirect('bod_dashboard')
                elif role == Account.COO:
                    return redirect('coo_dashboard')
                else:
                    messages.error(request, "Your role does not have a dashboard.")
                    return redirect('login')
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



#api_view for View_daily_assigned_task

@api_view(['GET'])
def view_daily_assigned_task(request):
    username = request.user.username  # Get the username of the logged-in user
    
    try:
        # Retrieve the user object using the username
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # Retrieve all project tasks assigned to the user
    assigned_tasks = ProjectTasks.objects.filter(assigned_to=user)
    
    # Prepare a list to hold the project names and tasks
    projects_and_tasks = []
    
    # Iterate over the assigned tasks to get the project names
    for task in assigned_tasks:
        project_name = task.project_id.project_name  # Ensure this attribute exists in your Project model
        task_title = task.task_id.title  # Ensure this attribute exists in your Task model
        projects_and_tasks.append({'project_name': project_name, 'task_title': task_title})
    
    # Return the response including the username and the list of projects and tasks
    return Response({'username': username, 'projects_and_tasks': projects_and_tasks}, status=status.HTTP_200_OK)





#view_assign_project_views

@api_view(['GET'])
def view_assigned_projects(request):
    username = request.user.username  # Get the username of the logged-in user
    
    try:
        # Retrieve the user object using the username
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # Retrieve all project tasks assigned to the user
    assigned_tasks = ProjectTasks.objects.filter(assigned_to=user)
    
    # Prepare a set to hold the unique project names
    assigned_projects = set()
    
    # Iterate over the assigned tasks to get the unique project names
    for task in assigned_tasks:
        project_name = task.project_id.project_name
        assigned_projects.add(project_name)
    
    # Return the response including the username and the list of assigned projects
    return Response({'username': username, 'assigned_projects': list(assigned_projects)}, status=status.HTTP_200_OK)


#view_project_status_api
@api_view(['GET'])
def view_project_status(request):
    # Retrieve the username from the logged-in user
    username = request.user.username

    try:
        # Retrieve the user object using the username
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve all project tasks assigned to the user
    assigned_tasks = ProjectTasks.objects.filter(assigned_to=user)

    # Prepare a list to hold project statuses
    project_statuses = []

    # Iterate over the assigned tasks to get project names and statuses
    for task in assigned_tasks:
        project_name = task.project_id.project_name
        project_status = task.project_id.status
        project_statuses.append({'project_name': project_name, 'status': project_status})

    # Return the response including the username and the list of project statuses
    return Response({'username': username, 'project_statuses': project_statuses}, status=status.HTTP_200_OK)



# api_view for BOD_view
@api_view(['GET'])
def view_all_project_details(request):
    # Retrieve all project tasks
    all_tasks = ProjectTasks.objects.all()

    # Prepare a list to hold project details
    project_details = []

    # Iterate over all tasks to gather project details
    for task in all_tasks:
        project_name = task.project_id.project_name
        project_status = task.project_id.status
        task_title = task.task_id.title
        assigned_to = task.assigned_to.username if task.assigned_to else None
        project_details.append({
            'project_name': project_name,
            'status': project_status,
            'task_title': task_title,
            'assigned_to': assigned_to
        })

    # Return the response including the list of project details
    return Response({'project_details': project_details}, status=status.HTTP_200_OK)



#Api_view for Create_project
#check this not working
@api_view(['POST'])
def create_project(request):
    try:
        # Extract data from the request
        project_name = request.data.get('project_name')
        created_by_id = request.data.get('created_by')
        status = request.data.get('status')  # Assuming you're passing status in the request
        
        # Check if project_name and created_by_id are provided
        if not project_name or not created_by_id:
            return Response({'error': 'Both project_name and created_by are required.'}, status=get_stats.HTTP_400_BAD_REQUEST)
        
        # Check if the user exists
        created_by = User.objects.filter(id=created_by_id).first()
        if not created_by:
            return Response({'error': 'User with the provided created_by ID does not exist.'}, status=get_stats.HTTP_400_BAD_REQUEST)
        
        # Create the project
        project = Project.objects.create(project_name=project_name, created_by=created_by, status=status)
        return Response({'project_id': project.id}, status=get_stats.HTTP_201_CREATED)
    
    except IntegrityError as e:
        return Response({'error': str(e)}, status=get_stats.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'error': str(e)}, status=get_stats.HTTP_500_INTERNAL_SERVER_ERROR)



# Api_view for Assign_lead
@api_view(['POST'])
def assign_team_lead(request):
    # Extract project_id and team_lead_username from request data
    project_id = request.data.get('project_id') 
    team_lead_username = request.data.get('team_lead_username')

    # Check if project_id and team_lead_username are provided
    if not project_id or not team_lead_username:
        return Response({'error': 'Please provide both project_id and team_lead_username'}, status=400)

    try:
        # Retrieve project and team lead user objects
        project = Project.objects.get(pk=project_id)
        team_lead = User.objects.get(username=team_lead_username)
        
        # Update the project member as team lead
        ProjectMembers.objects.create(project_id=project, member_id=team_lead, is_project_lead=True)
        
        return Response({
            'message': f'{team_lead_username} assigned as team lead for project {project.project_name}',
            'username': team_lead_username,
            'project_name': project.project_name
        }, status=200)
    
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    



#api_view view_activity_log
@api_view(['GET'])
def view_activity_log(request, project_id):
    try:
        # Retrieve the project
        project = Project.objects.get(pk=project_id)
        
        # Query activity logs related to the project
        activity_logs = ActivityLog.objects.filter(project=project) # type: ignore
        
        # Prepare data to be returned
        logs_data = []
        for log in activity_logs:
            log_data = {
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'user': log.user.username,
                'action': log.action,
                'details': log.details
            }
            logs_data.append(log_data)
        
        return JsonResponse({'project_id': project_id, 'activity_logs': logs_data}, status=200)
    
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    


#view_project_status
@api_view(['GET'])
def view_pm_dashboard_status(request):
    # Retrieve all projects
    projects = Project.objects.all()

    # Prepare a list to hold project statuses, team leads, and project names
    project_status = []

    for project in projects:
        # Retrieve the team lead for the project
        team_lead = ProjectMembers.objects.filter(project_id=project, is_project_lead=True).first()
        team_lead_username = team_lead.member_id.username if team_lead else None

        # Prepare the project status data
        project_status_data = {
            'project_name': project.project_name,
            'status': project.get_status_display(), # Assuming status is a ChoiceField
            'team_lead': team_lead_username
        }

        # Append the project status data to the list
        project_status.append(project_status_data)

    # Return the response including the list of project statuses
    return Response({'project_status': project_status}, status=200)


#api_view for Creating Deadline of the project

@api_view(['POST'])
def create_deadline(request):
    try:
        # Extract project_name, starting_date, and deadline from the request data
        project_name = request.data.get('project_name')
        starting_date = request.data.get('starting_date')
        deadline = request.data.get('deadline')

        # Check if starting_date and deadline are not None
        if starting_date is None or deadline is None:
            return Response({'error': 'Starting date and deadline must be provided'}, status=400)

        # Correctly use the datetime class to parse the starting_date and deadline strings into datetime objects
        starting_date_datetime = datetime.strptime(starting_date, '%Y-%m-%d')
        deadline_datetime = datetime.strptime(deadline, '%Y-%m-%d')

        # Retrieve the project by name
        project = Project.objects.get(project_name=project_name)

        # Update the project's starting_date and deadline
        project.starting_date = starting_date_datetime
        project.deadline = deadline_datetime
        project.save()

        # Return a success response
        return Response({'message': 'Starting date and deadline set successfully', 'project_name': project_name, 'starting_date': starting_date, 'deadline': deadline}, status=200)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
