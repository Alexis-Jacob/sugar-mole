from django.db import models

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
	action = models.ManyToManyField(ActionModel)