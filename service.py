import json
import connection
import main
from google_auth_oauthlib.flow import Flow
from flask import Flask, request, jsonify, render_template
import time

class values:
    token = ""
    email = ""
    id = ""

app = Flask(__name__)
appflow = Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['openid', 'https://www.googleapis.com/auth/dialogflow',
            'https://www.googleapis.com/auth/cloud-platform'],
    redirect_uri='http://127.0.0.1:5000/login')  # Aqui tá redirecionando apos o login com google pra pasta padrao



@app.route('/')  # , methods=['POST'])
def home():
    auth_uri = appflow.authorization_url()
    print(auth_uri)
    
    return render_template('/LandingPage/index.html')

@app.route('/login')
def login():

    code = request.args.get('code')
    print(code)
    appflow.fetch_token(code=code)
    credentials = appflow.credentials
    values.token = credentials.token

    return render_template('login.html')

#Recebe requisições do front (manipula, responde)
@app.route('/chatbot')
def chat():
    if request.is_json:
        text = request.args.get('input_text')
        credencial = values.token

        retorno = main.Conversa(credencial, text)

        print('retorno: ', retorno)
        
        #Cadastro
        if retorno[0] == 'cadastro':
            nome = retorno[1]
            senha = retorno[2]
            idade = retorno[3]
            email = retorno[4]

            retorno = connection.cadastro(nome, senha, idade, email)

        elif (retorno[0] == 'login'):
            
            email = retorno[1]
            senha = retorno[2]
            
            retorno = connection.validarLogin(email, senha)

            res = retorno[1]
            values.email = res[0]
            values.id = res[1]
            
            retorno = retorno[0]
        elif retorno == 'consulta-marcar':
            retorno = connection.consultasDisponiveis()
            #Lembrar de retornar uma lista pra o ajax aq
            
            
        elif (retorno[0] == 'marcar'):
            id = retorno[1]
            retorno = connection.marcarConsulta(id, values.id)
        
        elif retorno == 'visualizar-consultas':
            retorno = connection.consultasMarcadas(values.id)
            #retorno = retorno[0]

        elif (retorno == 'cancelar'):
            retorno = connection.cancelarConsulta(values.id)

        return {'res': retorno}

        
    return render_template('/chatbot/index.html')


"""
    # Enviar um valor via AJAX
    if request.is_json:
        nome = 'josue'
        return jsonify({'nome': nome})

    return render_template('/chatbot/index.html')

    # Pegando dados de um botão
    text = request.args.get('button_text')
    print('\n')
    print('Button text:', text)
    print('\n')
    return render_template('/chatbot/index.html')
"""

# run Flask app
if __name__ == "__main__":
    # app.debug = False
    app.run()
