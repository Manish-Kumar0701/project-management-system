from django.urls import path
from .views import login_view, dev_dashboard, user_logout, pm_dashboard, bod_dashboard , coo_dashboard,add_project
urlpatterns = [
    # path('manager/',project_manager, name='manager'),
    path('', login_view, name='login'),
    path('accounts/logout',user_logout, name='logout'),
    path('add_project/', add_project, name='add_project'),
    
    path('dev-dashboard/', dev_dashboard, name='dev_dashboard', kwargs={'required_role': 'dev'}),
    path('pm_dashboard/', pm_dashboard, name='pm_dashboard', kwargs={'required_role': 'pm'}),
    path('bod_dashboard/', bod_dashboard, name='bod_dashboard', kwargs={'required_role': 'bod'}),
    path('coo_dashboard/', coo_dashboard, name='coo_dashboard', kwargs={'required_role': 'coo'}),
]
