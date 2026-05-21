# 🛒 Django Produtos API

> 🔗 **API em produção:** https://django-produtos-api.onrender.com/api

> API REST completa de produtos com autenticação JWT, rate limiting, containerização Docker e deploy em produção no Render.

---

## 📌 Sobre o projeto

Projeto construído para consolidar uma stack sólida de mercado com Django REST Framework — indo além do CRUD básico, aplicando autenticação stateless, proteção contra abuso, boas práticas de segurança e deploy em ambiente real.

---

## 🛠️ Stack

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.x | Linguagem principal |
| Django | 6.x | Framework web |
| Django REST Framework | latest | Construção da API REST |
| djangorestframework-simplejwt | latest | Autenticação JWT |
| PostgreSQL | latest | Banco de dados |
| Gunicorn | latest | Servidor WSGI em produção |
| Docker | latest | Containerização |
| python-dotenv | latest | Variáveis de ambiente |
| django-cors-headers | latest | Configuração de CORS |

---

## 📦 Instalação local

```bash
# Clone o repositório
git clone https://github.com/Wellington-Roveder/django-produtos-api.git
cd django-produtos-api

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```

---

## ⚙️ Variáveis de ambiente

Crie um `.env` na raiz baseado no `.env.example`:

```env
SECRET_KEY=
DEBUG=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

---

## 🔐 Autenticação

A API usa **JWT (JSON Web Token)** via `djangorestframework-simplejwt`. Todos os endpoints de produtos exigem autenticação.

**Por que JWT e não sessão ou API Key?**
JWT é stateless — o servidor não precisa manter estado de sessão, o que favorece escalabilidade horizontal. A troca foi aceita conscientemente: tokens JWT não podem ser revogados antes de expirar, então o tempo de expiração curto é a principal mitigação.

### Obter token

```http
POST /api/token/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

Resposta:

```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

### Renovar token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

### Usar o token nas requisições

```http
Authorization: Bearer <access_token>
```

---

## 🔗 Endpoints

Base URL: `http://localhost:8000/api/`

Todos os endpoints abaixo exigem o header `Authorization: Bearer <token>`.

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/produtos/` | Lista todos os produtos |
| POST | `/produtos/` | Cria um novo produto |
| GET | `/produtos/{id}/` | Detalha um produto |
| PUT | `/produtos/{id}/` | Atualiza um produto completo |
| PATCH | `/produtos/{id}/` | Atualiza campos específicos |
| DELETE | `/produtos/{id}/` | Remove um produto |

### Exemplo de payload

```json
{
  "nome": "Notebook Gamer",
  "descricao": "Notebook para desenvolvimento",
  "valor": "2999.99",
  "quantidade": 10
}
```

### Exemplo de resposta

```json
{
  "id": 1,
  "nome": "Notebook Gamer",
  "descricao": "Notebook para desenvolvimento",
  "valor": "2999.99",
  "quantidade": 10,
  "data_criacao": "15/05/2025 14:30:00"
}
```

---

## 🛡️ Segurança

### Rate Limiting

Proteção contra abuso e força bruta via throttling do DRF:

| Perfil | Limite | Raciocínio |
|---|---|---|
| Anônimo | 10 req/min | Barreira contra brute force — 10/min ainda é alto para um ataque real, mas equilibra usabilidade |
| Autenticado | 1000 req/dia | Usuários legítimos tendem a disparar mais requisições; o limite é generoso sem abrir para abuso |

### CORS

Configurado via `django-cors-headers` para controlar quais origens podem consumir a API.

### HTTPS

`SECURE_SSL_REDIRECT = not DEBUG` em produção — requisições HTTP são redirecionadas automaticamente para HTTPS.Se DEBUG=True localmente, o redirect está desativado corretamente.Ativado automaticamente quando DEBUG=False  

---

## 🗄️ Banco de dados

**Por que PostgreSQL e não SQLite?**

SQLite não suporta bem múltiplas escritas concorrentes — em cenários com duas requisições simultâneas, uma pode bloquear a outra ou gerar corrupção. PostgreSQL lida com concorrência corretamente via MVCC, é o padrão de mercado para aplicações em produção e foi a escolha para já praticar com a stack real desde o início.

- **Desenvolvimento:** PostgreSQL local
- **Produção:** PostgreSQL provisionado pelo Render

---

## 🐳 Docker e Deploy

### Por que Docker?

O Dockerfile foi escrito manualmente para ter controle total sobre a build — garantindo que o ambiente de produção seja exatamente o que foi programado, sem surpresas de dependência ou versão.

### Por que Gunicorn e não `runserver`?

O `runserver` do Django é single-threaded e não foi feito para produção. O Gunicorn sobe múltiplos workers (instâncias do código), permitindo atender requisições simultâneas com segurança.

### Por que Render?

Custo previsível e deploy direto a partir do repositório GitHub — sem configuração manual de infraestrutura. A cada push na branch main, o Render faz o build e o deploy automaticamente.

### Rodar com Docker localmente

```bash
docker build -t django-produtos-api .
docker run -p 8000:8000 --env-file .env django-produtos-api
```

---

## 🧪 Testes

```bash
python manage.py test
```

| Teste | O que valida |
|---|---|
| `test_listar_produtos` | GET `/produtos/` retorna 200 com lista |
| `test_criar_produto` | POST cria e persiste no banco |
| `test_deletar_produto` | DELETE remove e confirma exclusão |
| `test_put_produto` | PUT atualiza produto completo |
| `test_atualizar_produto` | PATCH atualiza campos parciais |

Cada teste usa `setUp` para criar um produto base em banco isolado — o banco de testes é recriado a cada execução.

### Próximos passos em testes

A cobertura atual cobre o **caminho feliz** de cada operação. Os edge cases planejados são:

- Requisição sem token deve retornar `401 Unauthorized`
- Requisição com token expirado deve retornar `401`
- POST com payload inválido deve retornar `400 Bad Request`
- GET em produto inexistente deve retornar `404 Not Found`

---

## 🗂️ Estrutura do projeto

```
django-produtos-api/
├── config/
│   ├── settings.py        # Configurações do projeto
│   ├── urls.py            # Roteamento principal
│   └── wsgi.py
├── produtos/
│   ├── models.py          # Model Produto
│   ├── serializers.py     # Serializer com formatação de data
│   ├── views.py           # ViewSet CRUD
│   ├── admin.py           # Registro no admin
│   └── tests.py           # Testes unitários dos endpoints
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── manage.py
```

---

## 📁 Decisões técnicas

**ModelViewSet**
Abstrai as 5 operações CRUD e gera as URLs automaticamente via `router.register`. A escolha foi pela praticidade — entender o que o framework oferece antes de customizar. Para endpoints com lógica muito específica, a alternativa seria descer para `APIView` e ter controle total do comportamento.

**Serializer customizado**
`data_criacao` é formatada como `dd/mm/yyyy HH:MM:SS` no serializer, mantendo a lógica de apresentação separada do model.

**Variáveis de ambiente**
`SECURE_SSL_REDIRECT = not DEBUG` — requisições HTTP são redirecionadas automaticamente para HTTPS. Se `DEBUG=True` localmente, o redirect está desativado. Ativado automaticamente quando `DEBUG=False`.

---

## 🚀 Status

✅ Funcional em produção — todos os testes passando.

**Melhorias planejadas:**
- [ ] Testes de autenticação e edge cases HTTP
- [ ] Paginação nos resultados de listagem
- [ ] Filtros e busca por nome/categoria

---

## 👨‍💻 Autor

**Wellington Roveder** — Estudante de Ciência da Computação

[LinkedIn](https://www.linkedin.com/in/wellington-roveder-04637b37b/) · [GitHub](https://github.com/Wellington-Roveder)
