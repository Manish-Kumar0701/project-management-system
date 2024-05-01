from django.urls import path
from .views import login_view, dev_dashboard, user_logout, pm_dashboard, bod_dashboard , coo_dashboard,add_project,view_daily_assigned_task, view_assigned_projects,view_project_status,view_all_project_details, assign_team_lead,create_project,view_activity_log,view_pm_dashboard_status,create_deadline
urlpatterns = [
    # path('manager/',project_manager, name='manager'),
    path('', login_view, name='login'),
    path('accounts/logout',user_logout, name='logout'),
    path('add_project/', add_project, name='add_project'),
    path('view_assigned_projects/', view_assigned_projects, name='view_assigned_projects'),
    path('view_project_status/', view_project_status, name='view_project_status'),
    path('view_all_project_details/', view_all_project_details, name='view_all_project_details'),
    path('view_daily_assigned_task/',view_daily_assigned_task,name='view_daily_assigned_task'),
    path('assign_team_lead/',assign_team_lead,name='assign_team_lead'),
    path('create_project/',create_project,name='create_project'),
    path('view_pm_dashboard_status/', view_pm_dashboard_status, name='view_pm_dashboard_status'),
    path('create_deadline/', create_deadline, name='create_deadline'),
    
    




    path('dev-dashboard/', dev_dashboard, name='dev_dashboard', kwargs={'required_role': 'dev'}),
    path('pm_dashboard/', pm_dashboard, name='pm_dashboard', kwargs={'required_role': 'pm'}),
    path('bod_dashboard/', bod_dashboard, name='bod_dashboard', kwargs={'required_role': 'bod'}),
    path('coo_dashboard/', coo_dashboard, name='coo_dashboard', kwargs={'required_role': 'coo'})
    
]
