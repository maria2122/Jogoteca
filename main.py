#Aluna: Maria Jaqueline dos Santos Silva
from flask import Flask, render_template, request, redirect, session,flash
# render_template permite carregarmos arquivo no arquivo atual.
#instanciando um objeto flask e armazenando na variável app.
app =  Flask(__name__)
#chave para o session
app.secret_key='LP2'

class Jogo:
    def __init__(self, nome, categoria, console):
        self._nome = nome
        self._categoria = categoria
        self._console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self._id=id
        self._nome=nome
        self._senha=senha

usuario1 = Usuario('mj', 'Maria Jaqueline', '123')
usuario2 = Usuario('mjs', 'Maria Jaqueline Santos', '1234')

usuarios={usuario1._id:usuario1, usuario2._id:usuario2}


jogo1 = Jogo('Tetrix', 'Puzzle', 'Super Nintendo')
jogo2 = Jogo('Super Mario', 'Aventura', 'Nintendo 64')
jogo3 = Jogo('Sonic', 'Aventura', 'Mega Drive')
jogo4 = Jogo('Sonic2', 'Aventura', 'Mega Drive')
jogo5 = Jogo('Sonic3', 'Aventura', 'Mega Drive')

lista = [jogo1, jogo2, jogo3, jogo4, jogo5]

@app.route('/')
def index():
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

    lista.append(jogo)
    return redirect('/')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima = ''
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    #verifica se o usuário enviado no form está na lista de usários
    if request.form['usuario'] in usuarios:
        usuario=usuarios[request.form['usuario']]
        print(usuario._senha, usuario._id, usuario._nome)

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


if __name__ == '__main__':
    app.run(debug=True)


