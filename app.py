from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__, static_folder='static')
CORS(app)

DB_PATH = 'mercado.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL,
        estoque_minimo INTEGER DEFAULT 10,
        codigo TEXT UNIQUE,
        unidade TEXT DEFAULT 'un',
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL NOT NULL,
        itens TEXT NOT NULL,
        forma_pagamento TEXT DEFAULT 'dinheiro',
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT,
        pontos INTEGER DEFAULT 0,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # Seed inicial se vazio
    c.execute('SELECT COUNT(*) FROM produtos')
    if c.fetchone()[0] == 0:
        produtos = [
            ('Arroz Tipo 1 5kg', 'Grãos', 22.90, 85, 20, 'P001', 'pct'),
            ('Feijão Carioca 1kg', 'Grãos', 9.50, 60, 15, 'P002', 'pct'),
            ('Açúcar Cristal 1kg', 'Mercearia', 4.99, 120, 30, 'P003', 'pct'),
            ('Óleo de Soja 900ml', 'Mercearia', 8.90, 50, 15, 'P004', 'un'),
            ('Macarrão Espaguete 500g', 'Massas', 3.49, 90, 20, 'P005', 'pct'),
            ('Leite Integral 1L', 'Laticínios', 5.29, 48, 20, 'P006', 'cx'),
            ('Pão de Forma 500g', 'Padaria', 7.90, 30, 10, 'P007', 'un'),
            ('Manteiga 200g', 'Laticínios', 11.50, 25, 8, 'P008', 'un'),
            ('Café Moído 500g', 'Bebidas', 18.90, 40, 10, 'P009', 'pct'),
            ('Refrigerante 2L', 'Bebidas', 8.49, 36, 12, 'P010', 'un'),
            ('Sabão em Pó 1kg', 'Limpeza', 12.90, 45, 15, 'P011', 'cx'),
            ('Detergente 500ml', 'Limpeza', 2.49, 80, 20, 'P012', 'un'),
            ('Shampoo 400ml', 'Higiene', 14.90, 20, 8, 'P013', 'un'),
            ('Papel Higiênico 4un', 'Higiene', 6.99, 55, 20, 'P014', 'pct'),
            ('Biscoito Recheado 130g', 'Snacks', 3.29, 70, 25, 'P015', 'un'),
            ('Tomate 1kg', 'Hortifruti', 5.90, 15, 5, 'P016', 'kg'),
            ('Banana Prata 1kg', 'Hortifruti', 4.50, 20, 5, 'P017', 'kg'),
            ('Frango Inteiro 1kg', 'Carnes', 14.90, 18, 6, 'P018', 'kg'),
            ('Ovos 12un', 'Laticínios', 13.90, 35, 12, 'P019', 'cx'),
            ('Iogurte Natural 170g', 'Laticínios', 3.99, 24, 8, 'P020', 'un'),
        ]
        c.executemany('INSERT INTO produtos (nome, categoria, preco, estoque, estoque_minimo, codigo, unidade) VALUES (?,?,?,?,?,?,?)', produtos)

        # Vendas simuladas dos últimos 30 dias
        for i in range(60):
            dias_atras = random.randint(0, 29)
            data = (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d %H:%M:%S')
            num_itens = random.randint(1, 5)
            itens = [{'produto_id': random.randint(1, 20), 'qtd': random.randint(1, 3), 'preco': round(random.uniform(3, 25), 2)} for _ in range(num_itens)]
            total = sum(i['qtd'] * i['preco'] for i in itens)
            pagamentos = ['dinheiro', 'cartao_debito', 'cartao_credito', 'pix']
            c.execute('INSERT INTO vendas (total, itens, forma_pagamento, criado_em) VALUES (?,?,?,?)',
                      (round(total, 2), json.dumps(itens), random.choice(pagamentos), data))

        clientes = [
            ('Maria Silva', '(11) 99999-1111', 'maria@email.com', 150),
            ('João Santos', '(11) 99999-2222', 'joao@email.com', 80),
            ('Ana Oliveira', '(11) 99999-3333', 'ana@email.com', 220),
            ('Carlos Lima', '(11) 99999-4444', '', 45),
            ('Fernanda Costa', '(11) 99999-5555', 'fernanda@email.com', 310),
        ]
        c.executemany('INSERT INTO clientes (nome, telefone, email, pontos) VALUES (?,?,?,?)', clientes)

    conn.commit()
    conn.close()

@app.route('/api/dashboard')
def dashboard():
    conn = get_db()
    c = conn.cursor()
    hoje = datetime.now().strftime('%Y-%m-%d')
    mes = datetime.now().strftime('%Y-%m')

    c.execute("SELECT COALESCE(SUM(total),0) FROM vendas WHERE criado_em LIKE ?", (hoje+'%',))
    vendas_hoje = c.fetchone()[0]

    c.execute("SELECT COALESCE(SUM(total),0) FROM vendas WHERE criado_em LIKE ?", (mes+'%',))
    vendas_mes = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM vendas WHERE criado_em LIKE ?", (hoje+'%',))
    num_vendas_hoje = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM produtos WHERE estoque <= estoque_minimo")
    estoque_baixo = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM produtos")
    total_produtos = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = c.fetchone()[0]

    # Vendas por dia (últimos 7 dias)
    vendas_semana = []
    for i in range(6, -1, -1):
        dia = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        c.execute("SELECT COALESCE(SUM(total),0), COUNT(*) FROM vendas WHERE criado_em LIKE ?", (dia+'%',))
        row = c.fetchone()
        vendas_semana.append({'dia': dia, 'total': round(row[0], 2), 'qtd': row[1]})

    # Categorias mais vendidas
    c.execute("SELECT categoria, COUNT(*) as qtd FROM produtos GROUP BY categoria ORDER BY qtd DESC LIMIT 6")
    categorias = [{'categoria': r[0], 'qtd': r[1]} for r in c.fetchall()]

    # Produtos com estoque baixo
    c.execute("SELECT nome, estoque, estoque_minimo FROM produtos WHERE estoque <= estoque_minimo ORDER BY estoque ASC LIMIT 5")
    alertas = [{'nome': r[0], 'estoque': r[1], 'minimo': r[2]} for r in c.fetchall()]

    conn.close()
    return jsonify({
        'vendas_hoje': round(vendas_hoje, 2),
        'vendas_mes': round(vendas_mes, 2),
        'num_vendas_hoje': num_vendas_hoje,
        'estoque_baixo': estoque_baixo,
        'total_produtos': total_produtos,
        'total_clientes': total_clientes,
        'vendas_semana': vendas_semana,
        'categorias': categorias,
        'alertas_estoque': alertas
    })

# ---- PRODUTOS ----
@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    conn = get_db()
    c = conn.cursor()
    busca = request.args.get('busca', '')
    categoria = request.args.get('categoria', '')
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []
    if busca:
        query += " AND (nome LIKE ? OR codigo LIKE ?)"
        params += [f'%{busca}%', f'%{busca}%']
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    query += " ORDER BY nome ASC"
    c.execute(query, params)
    produtos = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(produtos)

@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO produtos (nome, categoria, preco, estoque, estoque_minimo, codigo, unidade)
                 VALUES (?,?,?,?,?,?,?)''',
              (data['nome'], data['categoria'], data['preco'], data['estoque'],
               data.get('estoque_minimo', 10), data.get('codigo', ''), data.get('unidade', 'un')))
    conn.commit()
    produto_id = c.lastrowid
    conn.close()
    return jsonify({'id': produto_id, 'mensagem': 'Produto criado com sucesso!'})

@app.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('''UPDATE produtos SET nome=?, categoria=?, preco=?, estoque=?, estoque_minimo=?, unidade=?
                 WHERE id=?''',
              (data['nome'], data['categoria'], data['preco'], data['estoque'],
               data.get('estoque_minimo', 10), data.get('unidade', 'un'), id))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Produto atualizado!'})

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM produtos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Produto removido!'})

# ---- VENDAS ----
@app.route('/api/vendas', methods=['GET'])
def listar_vendas():
    conn = get_db()
    c = conn.cursor()
    limit = int(request.args.get('limit', 20))
    c.execute('SELECT * FROM vendas ORDER BY criado_em DESC LIMIT ?', (limit,))
    vendas = []
    for r in c.fetchall():
        v = dict(r)
        v['itens'] = json.loads(v['itens'])
        vendas.append(v)
    conn.close()
    return jsonify(vendas)

@app.route('/api/vendas', methods=['POST'])
def registrar_venda():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    itens = data['itens']
    total = sum(i['qtd'] * i['preco'] for i in itens)
    c.execute('INSERT INTO vendas (total, itens, forma_pagamento) VALUES (?,?,?)',
              (round(total, 2), json.dumps(itens), data.get('forma_pagamento', 'dinheiro')))
    # Atualiza estoque
    for item in itens:
        c.execute('UPDATE produtos SET estoque = estoque - ? WHERE id = ?', (item['qtd'], item['produto_id']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Venda registrada!', 'total': round(total, 2)})

# ---- CLIENTES ----
@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes ORDER BY nome ASC')
    clientes = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(clientes)

@app.route('/api/clientes', methods=['POST'])
def criar_cliente():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO clientes (nome, telefone, email) VALUES (?,?,?)',
              (data['nome'], data.get('telefone', ''), data.get('email', '')))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Cliente cadastrado!'})


