from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework import authentication, permissions

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
