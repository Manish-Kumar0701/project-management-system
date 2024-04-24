from rest_framework import serializers
from accounts.models import Account, ProjectTasks

class AccountSerializers(serializers.Serializer):
   class Meta:
       model=Account
       fields='__all__'
    
class ProjectTasksSerializers(serializers.ModelSerializer):
    class Meta:
        model=ProjectTasks
        fields='__all__'
        
        
# add other serializers here 