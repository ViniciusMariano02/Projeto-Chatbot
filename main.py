

from google_auth_oauthlib.flow import Flow
import requests
from utils import CONST
import json
import time

def Google():
    appflow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['openid', 'https://www.googleapis.com/auth/dialogflow',
                'https://www.googleapis.com/auth/cloud-platform'],
        redirect_uri='http://127.0.0.1:5000/login') #Aqui tá redirecionando apos o login com google pra pasta padrao

    auth_uri = appflow.authorization_url()
    print(auth_uri)
    
    code = input('digite: ')
    appflow.fetch_token(code=code)
    credencial = appflow.credentials

    return credencial #auth_uri


def Conversa(credencial, txt): #receber txt como
#while(True):
    #txt = input("Mensagem: ")
    payload = payload = {
        "queryParams": {
            "source": "DIALOGFLOW_CONSOLE",
            "timeZone": "America/Fortaleza",
            "sentimentAnalysisRequestConfig": {
                "analyzeQueryTextSentiment": True
            }
        },
        "queryInput": {
            "text": {"text": txt, "languageCode": "pt-br"}
        }
    }

    headers = {
        'accept': 'application/json text/plain, */*',
        'content-type': 'application/json; charset=UTF-8',
        'authorization': 'Bearer ' + credencial
    }

    res = requests.post(CONST.URL, headers=headers, json=payload)
    if(res.status_code == 200):
        resp = json.loads(res.text)
        resp_message = resp['queryResult']['fulfillmentMessages']
 
        if len(resp_message) > 1:
            c = 0
            re = []
            for i in resp_message:
                contagem = resp_message[c]['text']['text'][0]
                re.append(contagem)
                c += 1
        else:
            re = contagem = resp_message[0]['text']['text'][0]
        
        
        return re

