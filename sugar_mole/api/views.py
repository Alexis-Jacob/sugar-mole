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
import json
from apis import Netatmo

class APIDetails(APIView):
    #TODO generic stuff
    def get(self, request):
        netatmo = ["secret_access_key", "secret_id", "username", "password"]

        rep = {
        "netatmo" : netatmo,
        }

        return Response({"response": rep})

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
        """
        Return the list of the house
        """
        if not uuid:
            return Response(HouseSerializer(HouseModel.objects.all(), many=True).data)
        try:
            return Response(HouseSerializer(HouseModel.objects.get(unique_uuid=uuid)).data)
        except HouseModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, uuid=None):
        """
        create an house and return an uuid
        """
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
        """
        Execute action on an house according to the parameters:<br /> 
        - (scenario_name) (option) to do something with a scenario <br />
        - (api) and extra data in order to register an api <br />
        - (add_member) in order to add a member
        ---
        parameters:
            - name: scenario_name
              type: string
              required: no
            - name: option
              type: string
              required: no
            - name: add_member
              type: string
              required: no
        """
        if not uuid:
            return Response({"response": "you need to specify the uuid of the house"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            house = HouseModel.objects.get(unique_uuid=uuid)
            if request.data.has_key('scenario_name') and request.data.has_key('option'):
                try:
                    scenario = ScenarioModel.objects.get(name=request.data["scenario_name"])
                    if request.data['option'] == 'add':
                        house.scenarios.add(scenario) #add a scenario
                    elif request.data["option"] == "remove":
                        house.scenario.remove(scenario)
                    house.save()
                    return Response(status=status.HTTP_200_OK)
                except ScenarioModel.DoesNotExist:
                    return Response({"response": "scenario not found"}, status=status.HTTP_404_NOT_FOUND)
            elif request.data.has_key('api'):
                if request.data["api"] == "netatmo":
                    if request.data.has_key('secret_id') and request.data.has_key('secret_access_key') and request.data.has_key('username') and request.data.has_key('password'):
                        #todo : check auth, don't register an other api if it already exist 
                        data = {
                            "clientId" : request.data["secret_id"], 
                            "clientSecret" : request.data["secret_access_key"],
                            "username" : request.data["username"],
                            "password" : request.data["password"]
                            }
                        api = APIModel(name="netatmo", data=json.dumps(data)) #TODO : crypt this stuff :D 
                        api.save()
                        house.api_available.add(api) 
                        house.save()
                        return Response(status=status.HTTP_200_OK)

            elif request.data.has_key('add_member'):
                if request.user:
                    house.members.add(request.user)
                    house.save()
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response({"response" : "missing an option"}, status=status.HTTP_400_BAD_REQUEST)

        except HouseModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({"response" : "missing an option{}".format(request.data)}, status=status.HTTP_400_BAD_REQUEST)

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
        """
        create an user and get the auth token
        ---
        parameters:
            - name: username
              type: string
              required: true
            - name: password
              type: password
              required: true
        """

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
        """
        Connect a user and get the auth token
        ---
        parameters:
        - name: username
          type: string
          required: true
        - name: password
          type: password
          required: true
        """
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



class DevicesInfos(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    apiLst = {"netatmo" : Netatmo.NetAtmo}
    def get(self, request):
        """
        Get the list of device
        ---
        """
        if not request.data.has_key("api_name") or not request.data.has_key('data'):
            for house in HouseModel.objects.all():##Check in the orm if best way to do it 
                for user in house.members.all():
                    if user == request.user:
                        rep = []
                        for api in house.api_available.all():
                            if self.apiLst.has_key(api.name):
                                tmp = self.apiLst[api.name]()
                                authData = json.loads(api.data)
                                tmp.auth(authData)
                                rep = rep + tmp.getDevicesList()
                        return Response(rep)
        #api_name = request.data["api_name"]


    def put(self, request):
        """
        Return a specifique devices according to the date field returned by the "data" field in the get request 
        ---
        parameters:
        - name: data
          type: text
          required: true
        """        
        if request.data.has_key("data"):
            try:
                data = json.loads(request.data["data"])
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            api_name = data["api"]
            for house in HouseModel.objects.all():##Check in the orm if best way to do it 
                for user in house.members.all():
                    if user == request.user:
                        for api in house.api_available.all():
                            if self.apiLst.has_key(api.name) and api.name == api_name:
                                tmp = self.apiLst[api.name]()
                                authData = json.loads(api.data)
                                tmp.auth(authData)
                                return Response(tmp.getDeviceInfo(data['device_id']))
        return Response(status=status.HTTP_404_NOT_FOUND)
