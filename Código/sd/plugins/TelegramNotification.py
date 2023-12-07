def sendMsg(token, chat_id, text):
    import urequests
    import json
    print("sendMsg()")
    body = json.dumps({'chat_id': chat_id, 'text': text})
    print(body)
    try:
        print("==============TRY===========")
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        print("headers")
        response = urequests.post(url='https://api.telegram.org/bot' + token + '/sendMessage', data=body, headers=headers)
        print("Notification request Sent")
        print(response.text)
        response.close()
        return True
    except:
        print("Error on notification")
        return False

def sendNotification(data):
    if(data["outOfRange"]):
        valor = data["read"]
        nome = data["name"]
        from util import getConfiguration
        from medicoes import getTrigramsTable
        print("sendNotification() ")
        token = getConfiguration("TELEGRAM_TOKEN")
        chat = getConfiguration("TELEGRAM_CHAT")
        reads = "\n"
        trigstable = getTrigramsTable()
        for key in valor.keys():
            reads += trigstable[key] + ": " + valor[key] + "\n"
        print("sendNotification() definindo menssagem")
        msg = "Foi verificado um valor fora da faixa no sensor '" + nome  + reads
        print(msg)
        sendMsg(token,chat,msg)
        pass

def getHandlers():
    return { # dict with the handlers pointing to it functions
        "after_sensorReading":sendNotification}