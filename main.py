#Aluna: Maria Jaqueline dos Santos Silva
from flask import Flask, render_template, request, redirect, session,flash
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL
from models import Jogo, Usuario

app =  Flask(__name__)

app.secret_key='LP2'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'jogoteca'
app.config['MYSQL_PORT'] = 3307
db =MySQL(app)
jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo="Lista de Jogos X", jogos=lista)

@app.route('/novo')
def novo():
    '''verifica se o usuário não está na sessão e se (True) redireciona para tela de login.'''
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=novo')
    return render_template('novo.html', titulo="Cadastrando Novo Jogo")
#request.form captura a ação do submit dos forms.
@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogo)
    return redirect('/')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima = ''
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['usuario'])
    '''primeiro if verifica de usuario buscado acima não está vazio ele verifica a senha'''
    if usuario:
        if usuario._senha == request.form['senha']:
            '''se usuário logado for igual ao do envio no form, exibe-se a
            mensagem de sucesso no login e o mesmo é redirecionado para tela principal,
            senão ele exibe a mensagem de inconsistência e retorna a tela de login.
            '''
            session ['usuario_logado'] = request.form['usuario']
            #mensagem rápida
            flash(request.form['usuario'] + ' logou com sucesso!')
            ''' já enacaminha o usuário ao logar para a página em que ele clicou antes  logar.
            variável proxima_página recebe o input do form'''
            proxima_pagina = request.form['proxima']
            print(proxima_pagina)
        #trata a possibilidade de não haver próxima página e redireciona o usuário para tela de login.
            if proxima_pagina == '':
                return redirect('/')
            else:
                 return redirect('/{}'.format(proxima_pagina))

    flash('Não logado, insira os dados novamente!')
    return redirect('/login')

@app.route('/logout')
def logout():
    #session for igual a vazia
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect('/login')
#no aquivo editar ele pega o parâmetro id da lista e passa para a função editar
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=editar')
    jogo = jogo_dao.busca_por_id(id)
    return render_template('editar.html', titulo="Editando o Jogo", jogo=jogo)

@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    id = request.form['id']
    jogo = Jogo(nome, categoria, console, id)
    jogo_dao.salvar(jogo)
    return redirect('/')

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


