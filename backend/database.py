# backend/database.py
import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="gestao_financeira",
            user="postgres",
            password="161011",  
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def insert_usuario(self, nome, idade, email, senha):
        query = """
            INSERT INTO usuarios (nome, idade, email, senha)
            VALUES (%s, %s, %s, %s) RETURNING id
        """
        self.cursor.execute(query, (nome, idade, email, senha))
        usuario_id = self.cursor.fetchone()['id']
        self.conn.commit()
        return usuario_id

    def update_usuario(self, usuario_id, numero, salario, profissao):
        query = """
            UPDATE usuarios
            SET numero = %s, salario = %s, profissao = %s
            WHERE id = %s
        """
        self.cursor.execute(query, (numero, salario, profissao, usuario_id))
        self.conn.commit()

    def autenticar_usuario(self, email, senha):
        query = """
            SELECT id, nome FROM usuarios
            WHERE email = %s AND senha = %s
        """
        self.cursor.execute(query, (email, senha))
        return self.cursor.fetchone()

    def insert_transacao(self, valor, descricao, data, categoria_id, usuario_id):
        query = """
            INSERT INTO transacoes (valor, descricao, data, categoria_id, usuario_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (valor, descricao, data, categoria_id, usuario_id))
        self.conn.commit()

    def get_transacoes(self, usuario_id):
        query = """
            SELECT t.id, t.valor, t.descricao, t.data, c.nome as categoria, c.tipo
            FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE t.usuario_id = %s
            ORDER BY t.data DESC
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchall()

    def delete_transacao(self, transacao_id):
        query = "DELETE FROM transacoes WHERE id = %s"
        self.cursor.execute(query, (transacao_id,))
        self.conn.commit()

    def insert_custo_ganho_fixo(self, valor, descricao, categoria_id, usuario_id, tipo, dia):
        query = """
            INSERT INTO custos_ganhos_fixos (valor, descricao, categoria_id, usuario_id, tipo, dia)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (valor, descricao, categoria_id, usuario_id, tipo, dia))
        self.conn.commit()

    def get_custos_ganhos_fixos(self, usuario_id):
        query = """
            SELECT f.id, f.valor, f.descricao, f.dia, c.nome as categoria, f.tipo
            FROM custos_ganhos_fixos f
            JOIN categorias c ON f.categoria_id = c.id
            WHERE f.usuario_id = %s
            ORDER BY f.dia
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchall()

    def insert_aposta(self, jogo, valor_apostado, resultado, data, usuario_id):
        query = """
            INSERT INTO apostas (jogo, valor_apostado, resultado, data, usuario_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (jogo, valor_apostado, resultado, data, usuario_id))
        self.conn.commit()

    def get_apostas(self, usuario_id):
        query = """
            SELECT id, jogo, valor_apostado, resultado, data
            FROM apostas
            WHERE usuario_id = %s
            ORDER BY data DESC
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchall()

    def insert_investimento(self, valor, tipo, descricao, data, usuario_id):
        query = """
            INSERT INTO investimentos (valor, tipo, descricao, data, usuario_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (valor, tipo, descricao, data, usuario_id))
        self.conn.commit()

    def get_investimentos(self, usuario_id):
        query = """
            SELECT id, valor, tipo, descricao, data
            FROM investimentos
            WHERE usuario_id = %s
            ORDER BY data DESC
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchall()

    def delete_investimento(self, investimento_id):
        query = "DELETE FROM investimentos WHERE id = %s"
        self.cursor.execute(query, (investimento_id,))
        self.conn.commit()

    def get_categorias(self):
        query = """
            SELECT id, nome, tipo
            FROM categorias
            ORDER BY nome
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_resumo_semanal(self, usuario_id):
        query = """
            SELECT tipo, SUM(valor) as total
            FROM (
                SELECT 'Receita' as tipo, valor
                FROM transacoes t
                JOIN categorias c ON t.categoria_id = c.id
                WHERE t.usuario_id = %s AND c.tipo = 'Receita'
                AND t.data >= CURRENT_DATE - INTERVAL '7 days'
                UNION ALL
                SELECT 'Despesa' as tipo, valor
                FROM transacoes t
                JOIN categorias c ON t.categoria_id = c.id
                WHERE t.usuario_id = %s AND c.tipo = 'Despesa'
                AND t.data >= CURRENT_DATE - INTERVAL '7 days'
                UNION ALL
                SELECT 'Aposta Ganhou' as tipo, valor_apostado
                FROM apostas
                WHERE usuario_id = %s AND resultado = 'Ganhou'
                AND data >= CURRENT_DATE - INTERVAL '7 days'
                UNION ALL
                SELECT 'Aposta Perdeu' as tipo, valor_apostado
                FROM apostas
                WHERE usuario_id = %s AND resultado = 'Perdeu'
                AND data >= CURRENT_DATE - INTERVAL '7 days'
            ) subquery
            GROUP BY tipo
        """
        self.cursor.execute(query, (usuario_id, usuario_id, usuario_id, usuario_id))
        return self.cursor.fetchall()