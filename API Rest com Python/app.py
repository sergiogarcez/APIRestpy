#Primeiramente deve instalar o flask no cmd = "pip install flask"
import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__) #coloca a aplicação flask na variavel

db = mysql.connector.connect( #conexão com o banco de dados mysql
    host='localhost',
    user='root',
    password='sergio',
    database='dbapi',
    port='3306'
)

@app.route('/usuarios',methods=['GET']) #este @ indica a URL pra chegar naquele local
def obter_usuarios():
    cursor = db.cursor() #funcionalidade cursor funciona como um cursor dentro do database
    msgsql = f'Select * from usuarios' #formalizando a mensagem a ser enviada para o database
    cursor.execute(msgsql) #executa a mensagem enviada
    usuarios_adq = cursor.fetchall() #armazena o resultado da mensagem enviada
    cursor.close()
    usuarios_list = list() #deixo em formato list para ficar mais agradavel na amostra
    for x in usuarios_adq:
        usuarios_list.append( #O x evidencia o looping, listando assim todos os usuarios do db
            {
            'id': x[0],
            'nome': x[1],
            'login': x[2],
            'senha': x[3]
            }
        )
    return jsonify(info = 'Lista dos usuarios:', dados = usuarios_list)


@app.route('/usuarios/id/<int:id>', methods=['GET'])
def obter_usuarios_id(id):
    cursor = db.cursor()
    msgsql = f'Select id,nome,login,senha from usuarios where id = {id}'
    cursor.execute(msgsql)
    usuario_adq = cursor.fetchall()
    cursor.close()
    if usuario_adq != []:
            userlist = list()
            userlist.append(
            {
            'id': usuario_adq[0][0],
            'nome': usuario_adq[0][1],
            'login': usuario_adq[0][2],
            'senha': usuario_adq[0][3]
            }
        )
            return jsonify (dados = userlist, info = 'Usuario selecionado listado')
    else:
        return jsonify (info = 'Usuario não encontrado!')



@app.route('/usuarios/login/<string:login>', methods=['GET'])
def obter_usuarios_login(login):
    cursor = db.cursor()
    msgsql = f"Select id,nome,login,senha from usuarios where login = '{login}'"
    cursor.execute(msgsql)
    usuario_adq = cursor.fetchall()
    cursor.close()
    
    if usuario_adq != []:
            userlist = list()
            userlist.append(
            {
            'id': usuario_adq[0][0],
            'nome': usuario_adq[0][1],
            'login': usuario_adq[0][2],
            'senha': usuario_adq[0][3]
            }
        )
            return jsonify (dados = userlist, info = 'Usuario selecionado listado')
    else:
        return jsonify (info ='Usuario não encontrado! Digite o login correto')



@app.route('/usuarios', methods=['POST']) #tenho que fazer uma manutenção
def add_usuario():
    novouser = request.json #armazenar o json informado no postman ou derivados
    cursor = db.cursor()
    msgsql = f"Insert into usuarios (id,nome,login,senha) values ('{novouser['id']}','{novouser['nome']}','{novouser['login']}','{novouser['senha']}')"
    cursor.execute(msgsql)
    cursor.close()
    db.commit()
    return jsonify (info ='Usuario cadastrado com sucesso!')




@app.route('/usuarios',methods=['DELETE'])
def deletar_usuarios():
    cursor = db.cursor() #funcionalidade cursor funciona como um cursor dentro do database
    msgsql = f'Delete * from usuarios'
    cursor.execute(msgsql)
    cursor.close()
    return jsonify (info = 'Todos os usuarios foram apagados com sucesso!')





@app.route('/usuarios/id/<int:id>',methods=['DELETE'])
def deletar_usuario_id(id):
    cursor = db.cursor()
    msgsql_true = f'Select id from usuarios where id = {id}'
    msgsql = f'Delete from usuarios where id = {id}'
    cursor.execute(msgsql_true)
    verificacao = cursor.fetchall()
    if verificacao != []:
        cursor.execute(msgsql)
        cursor.close()
        db.commit()
        return jsonify (info = 'Usuario deletado com sucesso!')
    else:
        return jsonify (info = 'Usuario não encontrado!')
    


@app.route('/usuarios/id/<int:id>', methods=['PUT'])
def atualizar_usuario_id(id):
     cursor = db.cursor()
     atualizacao = request.json
     msgsql_true = f'Select id from usuarios where id = {id}'
     cursor.execute(msgsql_true)
     verificacao = cursor.fetchall()
     if verificacao != []:
          sql_att = f"update usuarios set nome ='{atualizacao['nome']}', login ='{atualizacao['login']}', senha = '{atualizacao['senha']}' where id = {id}"
          cursor.execute(sql_att)
          db.commit()
          return jsonify (info = 'Usuario Atualizado com Sucesso')
     else: 
          return jsonify (info = 'Não foi possivel atualizar o Usuario')

app.run(port=5000, host= 'localhost', debug= True) 