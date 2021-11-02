import MySQLdb
#criando conexão com o banco
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='admin', host='127.0.0.1', port=3307, charset='utf8')

#comando CREATE em SQL armazendo na variável criar_tabelas
criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `jogoteca`  DEFAULT CHARSET=utf8;
    USE `jogoteca`;
    CREATE TABLE `jogo` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB;
    CREATE TABLE `usuario` (
      `id` varchar(8) NOT NULL,
      `nome` varchar(20) NOT NULL,
      `senha` varchar(8) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB;'''

#execute() roda o comamdo acima guardado na variável criar_tabelas.
conn.cursor().execute(criar_tabelas)


# inserindo usuarios com executemany() que permite a inserção de várias linhas.
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO jogoteca.usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
            ('diego', 'Diego Saqui', 'flask'),
            ('nico', 'Nico', '7a1'),
            ('danilo', 'Danilo', 'vegas')
      ])

cursor.execute('select * from jogoteca.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO jogoteca.jogo (nome, categoria, console) VALUES (%s, %s, %s)',
      [
            ('God of War 4', 'Ação', 'PS4'),
            ('NBA 2k18', 'Esporte', 'Xbox One'),
            ('Rayman Legends', 'Indie', 'PS4'),
            ('Super Mario RPG', 'RPG', 'SNES'),
            ('Super Mario Kart', 'Corrida', 'SNES'),
            ('Fire Emblem Echoes', 'Estratégia', '3DS'),
      ])

cursor.execute('select * from jogoteca.jogo')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()