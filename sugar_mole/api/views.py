from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework import authentication, permissions
from serializers import *
from models import *
import uuid as unique_uuid

class ScenarioView(APIView):
	def get(self, request):
		return Response(ScenarioSerializer(ScenarioModel.objects.all(), many=True).data)

class ConditionView(APIView):
	def get(self, request):
		return Response(ConditionSerializer(ConditionModel.objects.all(), many=True).data)

class ActionView(APIView):
	def get(self, request):
		return Response(ActionSerializer(ActionModel.objects.all(), many=True).data)

class HouseView(APIView):
	def get(self, request, uuid=None):
		if not uuid:
			return Response(HouseSerializer(HouseModel.objects.all(), many=True).data)
		try:
			return Response(HouseSerializer(HouseModel.objects.get(unique_uuid=uuid), many=True).data)
		except HouseModel.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

	def post(self, request, uuid=None):
		while True:
			u = unique_uuid.uuid4()
			try:
				HouseModel.objects.get(unique_uuid=u)
			except HouseModel.DoesNotExist:
				house = HouseModel()
				house.unique_uuid = str(u)
				house.save()
				return Response({"response" : HouseSerializer(house).data}, status=status.HTTP_201_CREATED)


	def put(self, request, uuid):
		if not uuid:
			return Response({"response": "you need to specify the uuid of the house"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			house = HouseModel.objects.get(unique_uuid=uuid)
			if not request.data.has_key('scenario_name') or not request.data.has_key('option'):
				return Response({"response" : "missing key scenario_name or option"}, status=status.HTTP_400_BAD_REQUEST)
			try:
				scenario = ScenarioModel.objects.get(name=request.data["scenario_name"])
				if request.data['option'] == 'add':
					house.scenarios.add(scenario) #add a scenario
				else:
					house.scenario.remove(scenario)
				house.save()
				return Response(status=status.HTTP_200_OK)
			except ScenarioModel.DoesNotExist:
				return Response({"response": "scenario not found"}, status=status.HTTP_404_NOT_FOUND)

		except HouseModel.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)


class UserView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request):#DEBUG
    	rep = []
    	for user in User.objects.all():
    		rep.append("{} {} {}".format(user.username, user.password, Token.objects.filter(user=user)))
    	return Response(rep)


    def post(self, request):
    	if not request.data.has_key('username'):
    		return Response({"response": "missing field username"}, status=status.HTTP_400_BAD_REQUEST)

    	if not request.data.has_key('password'):
    		return Response({"response": "missing field password"}, status=status.HTTP_400_BAD_REQUEST)


    	if len(User.objects.filter(username=request.data["username"])) > 0:
    		return Response({"response" : "Username already in use"}, status=status.HTTP_400_BAD_REQUEST)

    	user = User.objects.create_user(username=request.data["username"], password=request.data["password"])
    	token, created = Token.objects.get_or_create(user=user)

    	return Response({"token": token.key}, status=status.HTTP_201_CREATED)

    #auth
    def put(self, request):
    	if not request.data.has_key('username'):
    		return Response({"response": "missing field username"}, status=status.HTTP_400_BAD_REQUEST)

    	if not request.data.has_key('password'):
    		return Response({"response": "missing field password"}, status=status.HTTP_400_BAD_REQUEST)

    	if len(User.objects.filter(username=request.data["username"])) == 0:
    		return Response({"response" : "Usern not found"}, status=status.HTTP_400_BAD_REQUEST)

    	user = authenticate(username=request.data["username"], password=request.data["password"])
    	if user:
	    	token, created = Token.objects.get_or_create(user=user)

	    	return Response({"token": token.key}, status=status.HTTP_200_OK)

		return Response(status=status.HTTP_401_UNAUTHORIZED)
