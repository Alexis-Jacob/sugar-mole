from IAPI import IAPI
from sys import version_info
import json, time

# HTTP libraries depends upon Python 2 or 3
if version_info.major == 3 :
	import urllib.parse, urllib.request
else:
	from urllib import urlencode
	import urllib2

# Common definitions

_BASE_URL       = "https://api.netatmo.net/"
_AUTH_REQ       = _BASE_URL + "oauth2/token"
_GETUSER_REQ    = _BASE_URL + "api/getuser"
_DEVICELIST_REQ = _BASE_URL + "api/devicelist"
_GETMEASURE_REQ = _BASE_URL + "api/getmeasure"
_GETTHERMSTATE  = _BASE_URL + "/api/getthermstate"



class ClientAuth:
	"Request authentication and keep access token available through token method. Renew it automatically if necessary"

	def __init__(self, clientId,
					   clientSecret,
					   username,
					   password):

		postParams = {
				"grant_type" : "password",
				"client_id" : clientId,
				"client_secret" : clientSecret,
				"username" : username,
				"password" : password,
				"scope" : "read_station read_thermostat write_thermostat"
				}
		resp = postRequest(_AUTH_REQ, postParams)
		print resp

		self._clientId = clientId
		self._clientSecret = clientSecret
		self._accessToken = resp['access_token']
		self.refreshToken = resp['refresh_token']
		self._scope = resp['scope']
		self.expiration = int(resp['expire_in'] + time.time())

	@property
	def accessToken(self):

		if self.expiration < time.time(): # Token should be renewed

			postParams = {
					"grant_type" : "refresh_token",
					"refresh_token" : self.refreshToken,
					"client_id" : self._clientId,
					"client_secret" : self._clientSecret
					}
			resp = postRequest(_AUTH_REQ, postParams)

			self._accessToken = resp['access_token']
			self.refreshToken = resp['refresh_token']
			self.expiration = int(resp['expire_in'] + time.time())

		return self._accessToken

class User:
	def __init__(self, authData):

		postParams = {
				"access_token" : authData.accessToken
				}
		resp = postRequest(_GETUSER_REQ, postParams)
		self.rawData = resp['body']
		self.id = self.rawData['_id']
		self.devList = self.rawData['devices']
		self.ownerMail = self.rawData['mail']

class DeviceList:
	def __init__(self, authData):

		self.getAuthToken = authData.accessToken
		postParams = {
				"access_token" : self.getAuthToken,
				"app_type" : "app_station" #app_thermostat
				}
		resp = postRequest(_DEVICELIST_REQ, postParams)
		self.rawData = resp['body']
		self.stations = { d['_id'] : d for d in self.rawData['devices'] }
		self.modules = { m['_id'] : m for m in self.rawData['modules'] }
		self.default_station = list(self.stations.values())[0]['station_name']

	def modulesNamesList(self, station=None):
		res = []
		for elem in self.modules.values():
			if elem.has_key('module_name'):
				res.append(elem["module_name"])
			else:
				elem["module_name"] = "Unamed"
				res.append(elem)
		#[m['module_name'] for m in self.modules.values()]
		res.append(self.stationByName(station)['module_name'])
		return res

	def stationByName(self, station=None):
		if not station : station = self.default_station
		for i,s in self.stations.items():
			if s['station_name'] == station : return self.stations[i]
		return None

	def stationById(self, sid):
		return None if sid not in self.stations else self.stations[sid]

	def moduleByName(self, module, station=None):
		s = None
		if station :
			s = self.stationByName(station)
			if not s : return None
		for m in self.modules:
			mod = self.modules[m]
			if mod.has_key('module_name') and mod['module_name'] == module :
				if not s or mod['main_device'] == s['_id'] : return mod
		return None

	def moduleById(self, mid, sid=None):
		s = self.stationById(sid) if sid else None
		if mid in self.modules :
			return self.modules[mid] if not s or self.modules[mid]['main_device'] == s['_id'] else None

	def lastData(self, station=None, exclude=0):
		s = self.stationByName(station)
		if not s : return None
		lastD = dict()
		# Define oldest acceptable sensor measure event
		limit = (time.time() - exclude) if exclude else 0
		ds = s['dashboard_data']
		if ds['time_utc'] > limit :
			lastD[s['module_name']] = ds.copy()
			lastD[s['module_name']]['When'] = lastD[s['module_name']].pop("time_utc")
			lastD[s['module_name']]['wifi_status'] = s['wifi_status']
		for mId in s["modules"]:
			ds = self.modules[mId]['dashboard_data']
			if ds['time_utc'] > limit :
				mod = self.modules[mId]
				lastD[mod['module_name']] = ds.copy()
				lastD[mod['module_name']]['When'] = lastD[mod['module_name']].pop("time_utc")
				# For potential use, add battery and radio coverage information to module data if present
				for i in ('battery_vp', 'rf_status') :
					if i in mod : lastD[mod['module_name']][i] = mod[i]
		return lastD

	def checkNotUpdated(self, station=None, delay=3600):
		res = self.lastData(station)
		ret = []
		for mn,v in res.items():
			if time.time()-v['When'] > delay : ret.append(mn)
		return ret if ret else None

	def checkUpdated(self, station=None, delay=3600):
		res = self.lastData(station)
		ret = []
		for mn,v in res.items():
			if time.time()-v['When'] < delay : ret.append(mn)
		return ret if ret else None

	def getMeasure(self, device_id, scale, mtype, module_id=None, date_begin=None, date_end=None, limit=None, optimize=False, real_time=False):
		postParams = { "access_token" : self.getAuthToken }
		postParams['device_id']  = device_id
		if module_id : postParams['module_id'] = module_id
		postParams['scale']      = scale
		postParams['type']       = mtype
		if date_begin : postParams['date_begin'] = date_begin
		if date_end : postParams['date_end'] = date_end
		if limit : postParams['limit'] = limit
		postParams['optimize'] = "true" if optimize else "false"
		postParams['real_time'] = "true" if real_time else "false"
		return postRequest(_GETMEASURE_REQ, postParams)

	def MinMaxTH(self, station=None, module=None, frame="last24"):
		if not station : station = self.default_station
		s = self.stationByName(station)
		if not s :
			s = self.stationById(station)
			if not s : return None
		if frame == "last24":
			end = time.time()
			start = end - 24*3600 # 24 hours ago
		elif frame == "day":
			start, end = todayStamps()
		if module and module != s['module_name']:
			m = self.moduleByName(module, s['station_name'])
			if not m :
				m = self.moduleById(s['_id'], module)
				if not m : return None
			# retrieve module's data
			resp = self.getMeasure(
					device_id  = s['_id'],
					module_id  = m['_id'],
					scale      = "max",
					mtype      = "Temperature,Humidity",
					date_begin = start,
					date_end   = end)
		else : # retrieve station's data
			resp = self.getMeasure(
					device_id  = s['_id'],
					scale      = "max",
					mtype      = "Temperature,Humidity",
					date_begin = start,
					date_end   = end)
		if resp:
			T = [v[0] for v in resp['body'].values()]
			H = [v[1] for v in resp['body'].values()]
			return min(T), max(T), min(H), max(H)
		else:
			return None

# Utilities routines

def postRequest(url, params):
	if version_info.major == 3:
		req = urllib.request.Request(url)
		req.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
		params = urllib.parse.urlencode(params).encode('utf-8')
		resp = urllib.request.urlopen(req, params).readall().decode("utf-8")
	else:
		params = urlencode(params)
		headers = {"Content-Type" : "application/x-www-form-urlencoded;charset=utf-8"}
		req = urllib2.Request(url=url, data=params, headers=headers)
		resp = urllib2.urlopen(req).read()
	return json.loads(resp)

def toTimeString(value):
	return time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(value)))

def toEpoch(value):
	return int(time.mktime(time.strptime(value,"%Y-%m-%d_%H:%M:%S")))

def todayStamps():
	today = time.strftime("%Y-%m-%d")
	today = int(time.mktime(time.strptime(today,"%Y-%m-%d")))
	return today, today+3600*24

# Global shortcut

def getStationMinMaxTH(station=None, module=None):
	authorization = ClientAuth()
	devList = DeviceList(authorization)
	if not station : station = devList.default_station
	if module :
		mname = module
	else :
		mname = devList.stationByName(station)['module_name']
	lastD = devList.lastData(station)
	if mname == "*":
		result = dict()
		for m in lastD.keys():
			if time.time()-lastD[m]['When'] > 3600 : continue
			r = devList.MinMaxTH(module=m)
			result[m] = (r[0], lastD[m]['Temperature'], r[1])
	else:
		if time.time()-lastD[mname]['When'] > 3600 : result = ["-", "-"]
		else : result = [lastD[mname]['Temperature'], lastD[mname]['Humidity']]
		result.extend(devList.MinMaxTH(station, mname))
	return result

class NetAtmo(IAPI):
	def __init__(self):
		self.name = "netatmo"

	def __purify__(self, device):
		tmp = {}
		data = device["dashboard_data"]
		if device["type"] == "NAModule4" or device["type"] == "NAModule1":
			tmp = {"name" : device["module_name"], "data" : json.dumps({"api" : "netatmo", "device_id" : device["_id"]})}
			tmp["type"] = 1
			tmp["desc"] = {"temperature" : data["Temperature"], "humidity" : data["Humidity"]}
			if data.has_key("CO2"): tmp["desc"]["CO2"] = data["CO2"]
		elif device["type"] == "NAModule2":
			tmp = {"name" : device["module_name"], "data" : json.dumps({"api" : "netatmo", "device_id" : device["_id"]})}
			tmp["type"] = 2
			tmp["desc"] =  {"GustStrength" : data["GustStrength"], "WindStrength" : data["WindStrength"], "GustAngle" : data["GustAngle"], "WindAngle" : data["WindAngle"]}
		return tmp

	def auth(self, kwargs):
		self.clt = ClientAuth(**kwargs)

	def name(self):
		return self.name

	def getDevicesList(self):
		rep = []
		devList = DeviceList(self.clt)
		for d in devList.modulesNamesList():
			device = devList.moduleByName(d)
			if device:
				print device["main_device"], device["_id"], device["module_name"], device["type"]
				tmp = self.__purify__(device)
				if len(tmp) > 0:
					rep.append(tmp)
		return rep

	def getDeviceInfo(self, data):
		devList = DeviceList(self.clt)
		return self.__purify__(devList.moduleById(data))
