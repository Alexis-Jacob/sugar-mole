from django.db import models
from django.contrib.auth.models import User

class APIModel(models.Model):
	name = models.CharField(max_length=200, blank=False)
	data = models.TextField() #json data about the auth

class ConditionModel(models.Model):
	name = models.CharField(max_length=200, blank=False)
	api  = models.CharField(max_length=200, blank=False)
	cond = models.TextField(blank=False) #json

class ActionModel(models.Model):
	name = models.CharField(max_length=200, blank=False)
	api  = models.CharField(max_length=200, blank=False)
	cond = models.TextField(blank=False) #json

class ScenarioModel(models.Model):
	name = models.CharField(max_length=200, blank=False) 
	type = models.BooleanField(default=True) #true -> recurrent / false -> ponctuel
	conditions = models.ManyToManyField(ConditionModel)
	actions = models.ManyToManyField(ActionModel)

class HouseModel(models.Model):
	unique_uuid = models.CharField(max_length=200, blank=False)
	members = models.ManyToManyField(User, blank=True)
	api_available = models.ManyToManyField(APIModel, blank=True)
	scenarios = models.ManyToManyField(ScenarioModel, blank=True)

class UserExtraData(models.Model):
	user = models.ForeignKey(User)
	push_data = models.TextField(blank=True)
