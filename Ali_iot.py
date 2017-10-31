from aliyunsdkcore import client
from aliyunsdkiot.request.v20170420 import RegistDeviceRequest,QueryDeviceByNameRequest,PubRequest
from aliyunsdkiot.request.v20170420 import PubRequest

accessKeyId = 'LTAIi9TJVoJnKTxd'
accessKeySecret = 'dgMCuBhhjmHC21EyUquc0u6o8W6r3Y'
clt = client.AcsClient(accessKeyId, accessKeySecret, 'cn-shanghai')

def register(productKey,deviceName):
    request = RegistDeviceRequest.RegistDeviceRequest()
    request.set_accept_format('json')
    request.set_ProductKey(productKey)
    request.set_DeviceName(deviceName)
    result = clt.do_action_with_exception(request)
    return result

def query(productKey,deviceName):
    request = QueryDeviceByNameRequest.QueryDeviceByNameRequest()
    request.set_accept_format('json')
    request.set_ProductKey(productKey)
    request.set_DeviceName(deviceName)
    result = clt.do_action_with_exception(request)
    return result

def publish(productKey,topic,msg,qos=1):
    request = PubRequest.PubRequest()
    request.set_accept_format('json')
    request.set_ProductKey(productKey)
    request.set_TopicFullName(topic)
    request.set_MessageContent(msg)
    request.set_Qos(qos)
    result = clt.do_action_with_exception(request)
    return result