def sendMsg(token, chat_id, text):
    import urequests
    import json
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


def validarLeitura(faixas,values):
    print(faixas)
    for key in values:
        valor = values[key]
        print("validarLeitura(): verificando " + key)
        if (faixas[key]["max"]<valor or faixas[key]["min"]>valor):
            print("Fora da faixa")
            return False
    return True


def sendNotification(sensor,valor):
    from util import getConfiguration
    print("sendNotification() ")
    print(sensor)
    token = getConfiguration("TELEGRAM_TOKEN")
    chat = getConfiguration("TELEGRAM_CHAT")
    print("sendNotification() definindo menssagem")
    msg = "Foi verificado um valor fora da faixa no sensor '" + sensor["nome"] + "' - valor= " + valor
    print(msg)
    sendMsg(token,chat,msg)
    pass
