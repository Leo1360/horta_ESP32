import urequests
import json

def sendMsg(token, chat_id, text):
    print("sendMsg")
    body = json.dumps({'chat_id': chat_id, 'text': text})
    print(body)
    try:
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        response = urequests.post(url='https://api.telegram.org/bot' + token + '/sendMessage', data=body, headers=headers)
        print(response.text)
        response.close()
        return True
    except:
        return False
