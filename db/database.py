import psycopg2
from psycopg2 import Error

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
                nome VARCHAR(100) NOT NULL
            )
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

    def insert_usuario(self, nome):
        sql = "INSERT INTO usuarios (nome) VALUES (%s) RETURNING id"
        self.cursor.execute(sql, (nome,))
        self.connection.commit()
        return self.cursor.fetchone()[0]

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

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()