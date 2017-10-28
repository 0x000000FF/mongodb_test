from flask import Flask, url_for
from flask import request
from flask import json
import hashlib
import time
import pymongo

from copy import deepcopy

WRONG_REQUEST_MSG = "Wrong message type,the message must be a json!"
WRONG_JSON_FORMAT = "Wrong json format"

db_user_profile = {u"username":u"",u"pswd":"",u"uuid":u"",u"token":u"",u"tel":u"",u"devices":[]}

reply_failed = {u"message":u"failed",u"detail":"ERROR MESSAGE"} 

template_new_user = {u"username":u"",u"tel":u""} 
reply_new_user = {u"message":u"success",u"detail":""} 

template_user_regitste = {u"username":u"",u"pswd":u"",u"checknumber":u""} 
reply_user_regitste = {u"message":u"success",u"detail":{u"uuid":u"",u"token":u""}} 

template_login = {u"username":u"",u"pswd":u""} 
reply_login = {u"message":u"success",u"detail":{u"username":u"",u"uuid":u"",u"token":""}} 

template_get_profile = {u"uuid":u"",u"token":""} 
reply_get_profile = {u"message":u"success",u"detail":{u"username":u"",u"uuid":u"",u"tel":u""}} 

template_change_pswd = {u"uuid":u"",u"token":"",u"oldpswd":"",u"newpswd":""} 
reply_change_pswd = {u"message":u"success",u"detail":""} 

template_find_pswd = {u"uuid":u"",u"token":"",u"tel":u""} 
reply_find_pswd = {u"message":u"success",u"detail":""} 

template_reset_pswd = {u"uuid":u"",u"token":"",u"tel":u"",u"checknumber":u"",u"newpswd":u""} 
reply_reset_pswd = {u"message":u"success",u"detail":""} 

template_get_devices = {u"uuid":u"",u"token":"",u"devicetype":u"",u"devicename":u""} 
reply_get_devices = {u"message":u"success",u"detail":
						{"devices": [{"deviceType":"","image":"","mqttBroker":"","productKey":"","deviceName":"","customName":"","showSwitch":True}]
						}} 

template_add_device = {u"uuid":u"",u"token":"",u"devicetype":u"",u"devicename":u""} 
reply_add_device = {u"message":u"success",u"detail":""} 

template_del_device = {u"uuid":u"",u"token":"",u"devicetype":u"",u"devicename":u""} 
reply_del_device = {u"message":u"success",u"detail":""} 

connection = pymongo.MongoClient("127.0.0.1",27017)
db = connection.test
db_set = db.test_set

# template_new_user = {u"username":u"",u"pswd":u"",u"tel":u"",u"E-mail":u""}
# template_login = {u"username":u"",u"pswd":u""}
# template_get_user_profile = {u"uuid":u"",u"token":""}
# template_change_pswd = {u"uuid":u"",u"token":"",u"oldpswd":"",u"newpswd":0}
# template_find_pswd = {u"uuid":u"",u"token":"",u"tel":u""}
# template_reset_pswd = {u"uuid":u"",u"token":"",u"tel":u"",u"checknumber":u"",u"newpswd":u""}
# template_add_devices = {u"uuid":u"",u"token":"",u"devicetype":u"",u"devicename":u""}
# template_del_device = {u"uuid":u"",u"token":"",u"devicetype":u"",u"devicename":u""}

app = Flask(__name__)


def format_check(jsonstr,dircform):
	j_d = json.loads(jsonstr)

	print j_d.keys()
	print dircform.keys()
	print template_new_user.keys()
	for k in j_d.keys():
		if(k in dircform.keys()):
			if(type(j_d[k]) != type(dircform[k])):
				print "value type missmath"
				return False
		else:
			print k
			print "keys missmath"
			return False
	return True

def generate_UUID(codestr):
	md5_obj = hashlib.md5()
	md5_obj.update(codestr+str(time.time()))
	return str(md5_obj.hexdigest())

#check phone message checknumber
def check_checknumber(checknumber):
	return True

#check if the username is repeated
def check_username(username):
	return True

def generate_failed_mesg(mesg):
	failed_mesg = deepcopy(reply_failed)
	failed_mesg["detail"] = mesg
	return json.dumps(failed_mesg)


#{"username":"testname","pawd":"hkgadjfhasdgfds","tel":"","E-mail":""}
@app.route('/user/newuser')
def user_new():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_new_user)):
			j_d = json.loads(json.dumps(request.json))
			db_resoult = db_set.find(j_d)


			else:
				return generate_failed_mesg("no such user")
			return "TRUE\n"
		return WRONG_JSON_FORMAT
	else:
		return WRONG_REQUEST_MSG

@app.route('/user/registe')
def user_registe():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_user_regitste)):
			j_d = json.loads(json.dumps(request.json))
			# print (j_d)
			if not (check_checknumber(j_d["checknumber"])):
				return generate_failed_mesg("check number ERROR")

			uuid = generate_UUID(str(j_d["username"]+j_d["pswd"]));
			token = "asdasfd"

			re_msg = deepcopy(reply_user_regitste)
			re_msg["detail"]["uuid"] = uuid
			re_msg["detail"]["token"] = token
			# print (re_msg)
			db_data = deepcopy(db_user_profile)
			for i in j_d.keys():
				db_data[i] = j_d[i]
			db_data["uuid"] = uuid
			db_data["token"] = token

			# print db_data
	
			db_set.insert(db_data)

			for i in db_set.find():
				print i
			return json.dumps(re_msg)
		else:
			return generate_failed_mesg(WRONG_JSON_FORMAT)
	else:
		return generate_failed_mesg(WRONG_REQUEST_MSG)

@app.route('/user/login')
def user_login():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_login)):
			j_d = json.loads(json.dumps(request.json))
			db_resoult = db_set.find(j_d)
			if (db_resoult.count == 0):
				return generate_failed_mesg("password error")

			re_msg = deepcopy(reply_login)
			re_msg["username"] = db_resoult["username"]
		return WRONG_JSON_FORMAT
	else:
		return WRONG_REQUEST_MSG

@app.route('/user/getprofile')
def user_get_profile():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_get_profile)):
			return "TRUE\n"
		return WRONG_JSON_FORMAT
	else:
		return WRONG_REQUEST_MSG

@app.route('/user/changepswd')
def user_changepswd():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_change_pswd)):
			return "TRUE\n"
		return WRONG_JSON_FORMAT
	else:
		return WRONG_REQUEST_MSG

@app.route('/user/findpswd')
def user_findpswd():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_find_pswd)):
			return "TRUE\n"
		return WRONG_JSON_FORMAT
	else:
		return WRONG_REQUEST_MSG

@app.route('/user/resetpswd')
def user_resetpswd():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_reset_pswd)):
			return "TRUE\n"
		return WRONG_JSON_FORMAT
	else:
		return WRONG_REQUEST_MSG

@app.route('/user/getdevices')
def get_users_devices():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_reset_pswd)):
			return "TRUE\n"
		return WRONG_JSON_FORMAT
	else:
		return WRONG_REQUEST_MSG

@app.route('/device/add')
def add_new_device():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_add_device)):
			return "TRUE\n"
		return WRONG_JSON_FORMAT
	else:
		return WRONG_REQUEST_MSG

@app.route('/device/del')
def del_device():
	if request.headers['Content-Type'] == 'application/json':
		if(format_check(json.dumps(request.json),template_del_device)):
			return "TRUE\n"
		return WRONG_JSON_FORMAT
	else:
		return WRONG_REQUEST_MSG

if __name__ == '__main__':
	app.run()






def ali_add_new_device():
	pass


