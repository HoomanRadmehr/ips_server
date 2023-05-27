from rest_framework import serializers
from rules.models import Rule


class ListRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id','name','is_verified','version']
        
        
class RetrieveRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id','name','code','description','is_verified','version']

        
class AdminRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        