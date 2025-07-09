import psycopg2
from psycopg2 import Error
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        try:
            self.connection = psycopg2.connect(
                user="postgres",
                password="161011",
                host="localhost",
                port="5432",
                database="gestao_financeira"
            )
            self.cursor = self.connection.cursor()
            self.create_tables()
        except (Exception, Error) as error:
            print("Erro ao conectar ao PostgreSQL:", error)

    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                idade INTEGER,
                email VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(100) NOT NULL,
                numero VARCHAR(20),
                salario DECIMAL(10, 2),
                profissao VARCHAR(100)
            )
            """,
            """
            ALTER TABLE usuarios
            ADD COLUMN IF NOT EXISTS idade INTEGER,
            ADD COLUMN IF NOT EXISTS email VARCHAR(100) UNIQUE,
            ADD COLUMN IF NOT EXISTS senha VARCHAR(100),
            ADD COLUMN IF NOT EXISTS numero VARCHAR(20),
            ADD COLUMN IF NOT EXISTS salario DECIMAL(10, 2),
            ADD COLUMN IF NOT EXISTS profissao VARCHAR(100)
            """,
            """
            CREATE TABLE IF NOT EXISTS categorias (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                tipo VARCHAR(20) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS transacoes (
                id SERIAL PRIMARY KEY,
                valor DECIMAL(10, 2) NOT NULL,
                descricao TEXT,
                data DATE NOT NULL,
                categoria_id INTEGER REFERENCES categorias(id),
                usuario_id INTEGER REFERENCES usuarios(id)
            )
            """
        )
        try:
            for command in commands:
                self.cursor.execute(command)
            self.connection.commit()
        except (Exception, Error) as error:
            print("Erro ao criar tabelas:", error)

    def insert_usuario(self, nome, idade, email, senha, numero=None, salario=None, profissao=None):
        sql = """INSERT INTO usuarios (nome, idade, email, senha, numero, salario, profissao)
                 VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id"""
        self.cursor.execute(sql, (nome, idade, email, senha, numero, salario, profissao))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def update_usuario(self, usuario_id, numero, salario, profissao):
        sql = """UPDATE usuarios SET numero = %s, salario = %s, profissao = %s
                 WHERE id = %s"""
        self.cursor.execute(sql, (numero, salario, profissao, usuario_id))
        self.connection.commit()

    def autenticar_usuario(self, email, senha):
        sql = "SELECT id, nome FROM usuarios WHERE email = %s AND senha = %s"
        self.cursor.execute(sql, (email, senha))
        return self.cursor.fetchone()

    def insert_categoria(self, nome, tipo):
        sql = "INSERT INTO categorias (nome, tipo) VALUES (%s, %s) RETURNING id"
        self.cursor.execute(sql, (nome, tipo))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def insert_transacao(self, valor, descricao, data, categoria_id, usuario_id):
        sql = """INSERT INTO transacoes (valor, descricao, data, categoria_id, usuario_id)
                 VALUES (%s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (valor, descricao, data, categoria_id, usuario_id))
        self.connection.commit()

    def delete_transacao(self, transacao_id):
        sql = "DELETE FROM transacoes WHERE id = %s"
        self.cursor.execute(sql, (transacao_id,))
        self.connection.commit()

    def get_transacoes(self, usuario_id):
        sql = """SELECT t.id, t.valor, t.descricao, t.data, c.nome, c.tipo
                 FROM transacoes t
                 JOIN categorias c ON t.categoria_id = c.id
                 WHERE t.usuario_id = %s"""
        self.cursor.execute(sql, (usuario_id,))
        return self.cursor.fetchall()

    def get_categorias(self, tipo=None):
        if tipo:
            sql = "SELECT id, nome FROM categorias WHERE tipo = %s"
            self.cursor.execute(sql, (tipo,))
        else:
            sql = "SELECT id, nome, tipo FROM categorias"
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_relatorio_mensal(self, usuario_id, ano, mes):
        sql = """SELECT c.nome, c.tipo, SUM(t.valor) as total
                 FROM transacoes t
                 JOIN categorias c ON t.categoria_id = c.id
                 WHERE t.usuario_id = %s AND EXTRACT(YEAR FROM t.data) = %s AND EXTRACT(MONTH FROM t.data) = %s
                 GROUP BY c.nome, c.tipo"""
        self.cursor.execute(sql, (usuario_id, ano, mes))
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()