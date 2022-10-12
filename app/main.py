#libs
import sqlite3
from hashlib import sha256

# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# server
import uvicorn

app = FastAPI()

def db_commands(command):
    con = sqlite3.connect('cadastro-user-fastapi-test.db')
    cur = con.cursor()
    try:
        cur.execute('CREATE TABLE users(ID integer primary key autoincrement, NOME text ,CPF text);')
    except: pass

    # outros comandos
    cur.execute(command)
    con.commit()
    con.close()

def db_select(command):
    con = sqlite3.connect('cadastro-user-fastapi-test.db')
    cur = con.cursor()
    cur.execute(command)
    found = cur.fetchall()
    return found

# Cadastrar
@app.post('/user/register/{name}-{cpf}', response_class = HTMLResponse, status_code = 201)
async def register(name: str, cpf: str):
    user = []
    validationCPF = 0
    shaCPF = ''
    userName = name
    userCPF = cpf

    user.append(userName)
    if len(userCPF) == 11 and userCPF.isnumeric():
        for itemCPF in userCPF:
            validationCPF += int(itemCPF)
        if validationCPF == 44 or validationCPF == 55 or validationCPF == 66:
            shaCPF = str(sha256(userCPF.encode('utf-8')).hexdigest())
            user.append(shaCPF)
    db_commands(f'INSERT INTO users(NOME, CPF) VALUES("{user[0]}", "{user[1]}");')
    return f'<h1>{user[0]} cadastrado com sucesso</h1>'

# Retornar - 1 usuário
@app.get('/user/{_id}', response_class = HTMLResponse, status_code = 200)
async def return_user(_id: int):
    return f'<h1>{db_select(f"SELECT * FROM users where ID = {_id};")}</h1>'

# Retornar - Todos os usuários
@app.get('/user', response_class = HTMLResponse, status_code = 200)
async def return_users():
    return f'<h1>{db_select("SELECT * FROM users;")}</h1>'

# Deletar 1 usuário
@app.delete('/user/delete/{_id}', response_class = HTMLResponse, status_code = 200)
async def delete(_id: int):
    name = db_select(f"SELECT NOME FROM users where ID = {_id};")[0]
    db_commands(f"DELETE FROM users where ID = {_id}")
    return f'<h1>{name} excluído com sucesso</h1>'

if __name__ == '__main__':
	uvicorn.run(app = 'main:app', reload = True)