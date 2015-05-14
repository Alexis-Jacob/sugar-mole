from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',  'password', 'token')

class ConditionSerializer(serializers.ModelSerializer):
	class Meta:
		model = ConditionModel

class ActionSerializer(serializers.ModelSerializer):
	class Meta:
		model = ActionModel

class ScenarioSerializer(serializers.ModelSerializer):
	actions = ActionSerializer(many=True)
	conditions = ConditionSerializer(many=True)
	class Meta:
		model = ScenarioModel

class HouseSerializer(serializers.ModelSerializer):
	members = UserSerializer(many=True)
	scenarios = ScenarioSerializer(many=True)
	class Meta:
		model = HouseModel

