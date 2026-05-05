
# 🛒 MercadoSaaS — Gestão Inteligente para Supermercado de Bairro

Sistema SaaS completo para gestão de supermercado de bairro, com interface moderna dark-theme e backend Python.

---

## 🚀 Como Rodar

### 1. Pré-requisitos
- Python 3.8+
- pip

### 2. Instalar dependências
```bash
cd mercado_saas
pip install -r requirements.txt
```

### 3. Iniciar o servidor
```bash
python app.py
```

### 4. Acessar no navegador
```
http://localhost:5000
```

---

## 📦 Estrutura do Projeto

```
mercado_saas/
├── app.py              # Backend Flask (API REST)
├── requirements.txt    # Dependências Python
├── mercado.db          # Banco SQLite (gerado automaticamente)
└── static/
    └── index.html      # Frontend completo (HTML + CSS + JS)
```

---

## ✨ Funcionalidades

### 📊 Dashboard
- Métricas em tempo real: vendas do dia, do mês, total de produtos, alertas de estoque
- Gráfico de barras — vendas dos últimos 7 dias
- Alertas visuais para produtos com estoque baixo
- Distribuição de produtos por categoria

### 💳 PDV — Ponto de Venda (Caixa)
- Interface de caixa com grid de produtos
- Busca e filtro por categoria
- Carrinho de compras interativo
- Controle de quantidade
- Suporte a: Dinheiro, PIX, Cartão Débito, Cartão Crédito
- Atualização automática do estoque após venda

### 📦 Gestão de Produtos
- Cadastro completo: nome, código, categoria, preço, estoque, unidade
- Edição e exclusão de produtos
- Filtro por categoria e busca por nome/código
- Indicador visual de estoque baixo

### 🧾 Histórico de Vendas
- Listagem das últimas 50 vendas
- Data, hora, quantidade de itens, forma de pagamento, total

### 👥 Clientes
- Cadastro de clientes com nome, telefone, email
- Sistema de pontos de fidelidade

### ⚠️ Controle de Estoque
- Listagem de todos os produtos com estoque abaixo do mínimo
- Indicadores: 🔴 Crítico / 🟡 Alerta
- Badge no menu lateral com contagem de alertas

---

## 🛠️ Tecnologias

| Camada     | Tecnologia              |
|------------|-------------------------|
| Backend    | Python + Flask          |
| Banco      | SQLite (via sqlite3)    |
| API        | REST JSON               |
| Frontend   | HTML5 + CSS3 + JS puro  |
| Fontes     | Syne + DM Sans (Google) |

---

## 🔌 API Endpoints

| Método | Rota                    | Descrição                    |
|--------|-------------------------|------------------------------|
| GET    | /api/dashboard          | Métricas e dados do painel   |
| GET    | /api/produtos           | Listar produtos (c/ filtros) |
| POST   | /api/produtos           | Criar produto                |
| PUT    | /api/produtos/:id       | Atualizar produto            |
| DELETE | /api/produtos/:id       | Deletar produto              |
| GET    | /api/vendas             | Listar vendas                |
| POST   | /api/vendas             | Registrar venda              |
| GET    | /api/clientes           | Listar clientes              |
| POST   | /api/clientes           | Cadastrar cliente            |
| GET    | /api/categorias         | Listar categorias            |

---

## 📝 Dados Iniciais (Seed)
Ao iniciar pela primeira vez, o sistema cria automaticamente:
- **20 produtos** de exemplo em diversas categorias
- **60 vendas** simuladas nos últimos 30 dias
- **5 clientes** de exemplo

---

## 🔮 Próximas Funcionalidades (Roadmap)
- [ ] Autenticação de usuários (login/logout)
- [ ] Relatórios exportáveis em PDF/Excel
- [ ] Módulo de fornecedores
- [ ] Controle de contas a pagar/receber
- [ ] App mobile (PWA)
- [ ] Multi-loja

