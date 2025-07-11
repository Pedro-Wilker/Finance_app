# Adicionar ao final da classe Database
def insert_investimento(self, valor, tipo, descricao, data, usuario_id):
    query = """
        INSERT INTO investimentos (valor, tipo, descricao, data, usuario_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    self.cursor.execute(query, (valor, tipo, descricao, data, usuario_id))
    self.conn.commit()

def get_investimentos(self, usuario_id):
    query = """
        SELECT i.id, i.valor, i.tipo, i.descricao, i.data
        FROM investimentos i
        WHERE i.usuario_id = %s
        ORDER BY i.data DESC
    """
    self.cursor.execute(query, (usuario_id,))
    return self.cursor.fetchall()

def delete_investimento(self, investimento_id):
    query = "DELETE FROM investimentos WHERE id = %s"
    self.cursor.execute(query, (investimento_id,))
    self.conn.commit()

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