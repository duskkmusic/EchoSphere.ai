# 🤖 AI Multi-Agent Debate System

Sistema avançado de análise de documentos com múltiplos agentes de IA que debatem entre si, oferecendo perspectivas diversas sobre o mesmo conteúdo.

## 🎯 O Que Este Projeto Aborda

### **Conceitos Avançados**
- ✅ **OAuth2 completo** com refresh tokens e roles
- ✅ **SQLAlchemy 2.0 async** com relacionamentos complexos
- ✅ **Arquitetura multi-agente** com processamento paralelo
- ✅ **Context window management** para LLMs
- ✅ **RAG (Retrieval Augmented Generation)** com embeddings
- ✅ **WebSockets** para streaming em tempo real
- ✅ **Background tasks** com Celery
- ✅ **Rate limiting** por tier de usuário
- ✅ **Migrations** com Alembic
- ✅ **Testes assíncronos** com Pytest

## 🚀 Setup Inicial

### 1. Clonar e Configurar Ambiente

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar .env.example
cp .env.example .env

# Editar .env e adicionar sua chave Groq
# Obtenha em: https://console.groq.com/keys
```

### 3. Iniciar Serviços com Docker

```bash
# Subir PostgreSQL e Redis
docker-compose up -d postgres redis

# Verificar se estão rodando
docker ps
```

### 4. Criar Tabelas do Banco

```bash
# Inicializar Alembic (primeira vez)
alembic init alembic

# Criar migration inicial
alembic revision --autogenerate -m "Initial schema"

# Aplicar migrations
alembic upgrade head
```

### 5. Rodar a Aplicação

```bash
# Desenvolvimento
uvicorn app.main:app --reload

# Acesse: http://localhost:8000/docs
```

## 📚 Estrutura do Projeto

```
debate-ai/
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   │   ├── user.py      # User, RefreshToken, Roles
│   │   ├── document.py  # Document, DocumentChunk
│   │   ├── agent.py     # AgentPersonality
│   │   └── debate.py    # Debate, Analysis
│   ├── api/             # Endpoints FastAPI
│   │   ├── auth.py      # Login, register, refresh
│   │   ├── documents.py # Upload, list documents
│   │   └── debates.py   # Create, start debates
│   ├── services/        # Lógica de negócio
│   │   ├── llm_service.py      # Integração Groq
│   │   ├── agent_service.py    # Gerenciamento de agentes
│   │   └── debate_service.py   # Orquestração de debates
│   └── core/            # Segurança e config
│       ├── security.py  # JWT, hashing
│       └── oauth2.py    # Dependencies OAuth2
```

## 🎮 Como Usar

### 1. **Registrar Usuário**

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "securepass123"
  }'
```

### 2. **Fazer Login**

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepass123"
```

Salve o `access_token` retornado!

### 3. **Upload de Documento**

```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/document.pdf"
```

### 4. **Listar Agentes Disponíveis**

```bash
curl -X GET "http://localhost:8000/api/debates/agents" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Você verá:
- 🤔 **Cético**: Questiona tudo
- 😊 **Otimista**: Foca em possibilidades
- 🔬 **Técnico**: Análise profunda
- 🎨 **Criativo**: Conexões inesperadas
- ⚡ **Pragmático**: Aplicação prática

### 5. **Criar e Iniciar Debate**

```bash
# Criar debate
curl -X POST "http://localhost:8000/api/debates/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Análise do Contrato X",
    "document_id": 1,
    "num_rounds": 3
  }'

# Iniciar debate (passando IDs dos agentes)
curl -X POST "http://localhost:8000/api/debates/1/start" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_ids": [1, 2, 3, 4, 5]
  }'
```

### 6. **Ver Resultados do Debate**

```bash
curl -X GET "http://localhost:8000/api/debates/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔥 Desafios Técnicos para Implementar

### **Nível 1: Básico** ✅ (Já implementado)
- [x] OAuth2 com JWT
- [x] CRUD de usuários e documentos
- [x] Sistema de agentes
- [x] Debates básicos

### **Nível 2: Intermediário** 🚧 (Para você fazer!)

1. **Document Processor Service**
   - Extrair texto de PDFs (PyPDF2)
   - Chunking inteligente do conteúdo
   - Salvar chunks no banco

2. **Embedding Service**
   - Gerar embeddings com sentence-transformers
   - Armazenar no pgvector
   - Busca semântica por similaridade

3. **Rate Limiting**
   - Implementar decorator para rate limiting
   - Usar Redis para contadores
   - Diferenciar por tier (free/premium/admin)

4. **WebSocket para Streaming**
   - Endpoint WebSocket para debates ao vivo
   - Stream das respostas dos agentes em tempo real
   - Multiple clients watching

### **Nível 3: Avançado** 🔥 (Vai te fazer chorar!)

5. **Context Window Management**
   - Resumir conversas longas automaticamente
   - Manter contexto relevante (sliding window)
   - Priorizar informações importantes

6. **Caching Inteligente**
   - Cache de embeddings no Redis
   - Cache de análises similares
   - Invalidação estratégica

7. **Celery Background Tasks**
   - Processar documentos grandes em background
   - Fila de debates
   - Retry logic e error handling

8. **Testing Completo**
   - Unit tests para services
   - Integration tests para APIs
   - Mock de chamadas LLM
   - Test fixtures complexos

9. **Análise de Sentimento**
   - Detectar tom dos agentes
   - Gráficos de concordância/discordância
   - Timeline de evolução do debate

10. **Sistema de Memória**
    - Agentes "lembram" debates anteriores
    - Referências cruzadas entre documentos
    - Aprendizado de preferências do usuário

## 🎓 Conceitos Para Estudar

### **FastAPI & Async**
- `async/await` patterns
- AsyncSession vs Session
- Dependency injection system
- Background tasks vs Celery

### **SQLAlchemy 2.0**
- Async queries
- Relationships (one-to-many, many-to-many)
- Eager vs lazy loading
- Query optimization

### **OAuth2 & JWT**
- Token types (access vs refresh)
- Token rotation
- Secure password hashing
- Role-based access control

### **LLMs & RAG**
- Prompt engineering
- Context window limits
- Token counting
- Embeddings e similarity search

### **Arquitetura**
- Service layer pattern
- Repository pattern
- Domain-driven design
- SOLID principles

## 🐛 Troubleshooting

### Erro: `relation "vector" does not exist`
```bash
# Conectar no PostgreSQL
docker exec -it debate_ai_db psql -U debate_user -d debate_ai

# Criar extensão pgvector
CREATE EXTENSION IF NOT EXISTS vector;
```

### Erro: `Groq API key not found`
- Verifique se `.env` existe
- Confirme que `GROQ_API_KEY` está definida
- Reinicie a aplicação

### Debates não iniciam
- Verifique logs: `docker-compose logs -f api`
- Confirme que documento foi processado
- Teste Groq API separadamente

## 📝 Licença

MIT - Use como quiser para aprender!

---

**Dica Final**: Comece implementando um desafio por vez. Não tenha medo de errar - é assim que se aprende! 🚀
