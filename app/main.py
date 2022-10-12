# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import uvicorn
from uuid import uuid4

app = FastAPI()

users = {0: 'Ingnave'}
# Cadastrar
@app.get('/user/register/{user_register}', response_class = HTMLResponse)
async def register(user_register: str):
    if user_register:
        id = str(uuid4())
        users[id] = user_register
        return f'<h1>{user_register} cadastrado com sucesso!!!</h1>{users}'
    else:
        return 'Status Code = ?????????'


# Deletar
@app.get('/user/delete/{user_delete}', response_class = HTMLResponse)
async def delete(user_delete: str):
    if user_delete:
        return f'<h1>{users.get(user_delete)} excluido com sucesso!!!</h1>'
        users.pop(user_delete)

# Consultar um User
@app.get('/user/{token_user}', response_class = HTMLResponse)
async def return_user(token_user: str):
    return f'<h1>{users.get(token_user)}</h1>'

# Consultar todos
@app.get('/user', response_class = HTMLResponse)
async def return_users():
    # users = users.json()
    return f'<h1>{users}</h1>'

if __name__ == '__main__':
	uvicorn.run(app = 'main:app', reload = True)


# TASKS
# implementar um banco de dados
# registrar,deletar e consultar no banco
# mostrar o user ou os users em formato json
# tratar os erros e pesquisar sobre os status_code

