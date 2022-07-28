import mysql.connector

#CREATE

db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='bot-saude')
cursor = db_connection.cursor()

def cadastro(nome, senha, idade, email):
	db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='bot-saude')
	cursor = db_connection.cursor()

	id = 'DEFAULT'
	
	sql = f'INSERT INTO Paciente (id_do_paciente, nome_paciente, senha_paciente, idade, email) VALUES ({id}, "{nome}", "{senha}", {idade}, "{email}")'

	cursor.execute(sql)

	return 'Cadastrado com sucesso. Gostaria de logar em sua conta?'

def consultasDisponiveis():
	
	db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='bot-saude')
	cursor = db_connection.cursor()

	sql = 'SELECT * FROM consultasDisponiveis'
	cursor.execute(sql)
	resultado = cursor.fetchall()

	
	return (resultado, 'Digite o ID da consulta que gostaria de marcar: ')

def marcarConsulta(ID_disponivel, id_paciente):
	db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='bot-saude')
	cursor = db_connection.cursor()

	sql = f'SELECT * FROM consultasDisponiveis WHERE ID = {ID_disponivel}'
	cursor.execute(sql)
	resultado = cursor.fetchall()

	resultado = resultado[0]

	ID, id_medico, data, horario, lugar_medico = resultado
	
	sql = f'SELECT * FROM Consultas WHERE id_paciente = {id_paciente}'
	cursor.execute(sql)
	res = cursor.fetchall()

	if res != '':
		sql = f'INSERT INTO Consultas (ID, id_paciente, id_medico, data_consult, horario, lugar_medico) VALUES ({ID}, {id_paciente}, {id_medico}, "{data}", "{horario}", "{lugar_medico}")'
		cursor.execute(sql)
		
		sql = f'DELETE FROM consultasDisponiveis WHERE ID = {ID_disponivel}'
		cursor.execute(sql)
	else:
		return 'Só é possível ter 1 consulta marcada.'

	return 'Consulta marcada com sucesso! No dia de sua consulta, compareça com um documento com foto.'

#READ
def validarLogin(email, senha):
	db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='bot-saude')
	cursor = db_connection.cursor()


	sql = f'SELECT * FROM Paciente WHERE (email="{email}") AND (senha_paciente="{senha}")'
	cursor.execute(sql)
	resultado = cursor.fetchall()
	

	if resultado == None:
		return 'Conta não encontrada. Gostaria de tentar entrar novamente?'
	else:
		res = resultado[0]
		id, nome, senha, idade, email = res
		retorno = ('Logado com sucesso. No que posso te ajudar? (Marcar consultas, Visualizar consultas marcadas, Desmarcar consultas', (email, id))
		
		return retorno

def consultasMarcadas(id):
	db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='bot-saude')
	cursor = db_connection.cursor()

	sql = f'SELECT * FROM Consultas WHERE id_paciente = {id}'
	
	cursor.execute(sql)
	resultado = cursor.fetchall()
	
	if resultado != []:
		res = resultado[0]
		ID, id_paciente, id_medico, data_consult, horario, lugar_medico = res

		id_medico = nomeador(id_medico)

		return (f'Consulta marcada: Médico: {id_medico}, Data: {data_consult}, {horario}, Endereço: {lugar_medico}. No que mais posso te ajudar?')
	else:
		return ('Você não tem consultas marcadas no momento. No que mais posso te ajudar?')

def cancelarConsulta(id):
	db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='bot-saude')
	cursor = db_connection.cursor()

	sql = f'SELECT * FROM Consultas WHERE id_paciente = {id}'
	cursor.execute(sql)
	resultado = cursor.fetchall()

	res = resultado[0]
	
	if res == []:
		return 'Não existe nenhuma consulta marcada. Em que posso ajudar?'
	else:
		
		ID, id_paciente, id_medico, data_consult, horario, lugar_medico = res

		if (id_paciente != id):
			return 'ID incorreto'
		else:
			sql = f'INSERT INTO consultasDisponiveis (ID, id_medico, data_consult, horario, lugar_medico) VALUES ({ID}, {id_medico}, "{data_consult}", "{horario}", "{lugar_medico}")'
			cursor.execute(sql)

			sql = f'DELETE FROM Consultas WHERE id_paciente = {id}' 
			cursor.execute(sql)
			
		
			return 'Consulta desmarcada com sucesso.' 


def nomeador(id_medico):
	if id_medico == 1:
		id_medico = 'Dra. Debora Farias Batista'
	elif id_medico == 2:
		id_medico = 'Dra. Ana Caroline Cavalcanti'
	elif id_medico == 3:
		id_medico = 'Dr. Carlos Alfandega Silva'
	return id_medico



cursor.close()
db_connection.close()
