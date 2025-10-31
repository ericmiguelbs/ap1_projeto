Perfeito 👍
Aqui está **o código completo em Markdown**, com **todas as formatações, ícones e blocos de código preservados**, exatamente como na sua documentação original:

````markdown
# 🏫 Sistema de Gerenciamento Escolar

API RESTful para gerenciamento de alunos, professores, turmas, atividades, notas e reservas em uma instituição de ensino.

---

## 📖 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
  - [Localmente](#localmente)
  - [Com Docker](#com-docker)
- [Documentação da API](#api_doc--documentação-da-api)
- [Modelos de Dados](#modelos-de-dados)
- [Endpoints](#endpoints)
  - [AlunoController](#alunocontroller)
  - [ProfessorController](#professorcontroller)
  - [TurmaController](#turmacontroller)
  - [AtividadeController](#atividadecontroller)
  - [NotasController](#notascontroller)
  - [ReservaController](#reservacontroller)
- [Como Contribuir](#como-contribuir)
- [Autores](#-autores)
- [Licença](#-licença)

---

## 💡 Funcionalidades

- [x] CRUD completo para Alunos  
- [x] CRUD completo para Professores  
- [x] CRUD completo para Turmas  
- [x] CRUD completo para Atividades (com validação externa)  
- [x] CRUD completo para Notas (com validação externa)  
- [x] CRUD completo para Reservas (com validação externa)

---

## 💻 Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias:

- **Backend:** Python  
- **Framework:** Flask  
- **Containerização:** Docker e Docker Compose  
- **Comunicação:** API REST com validações entre microsserviços.

---

## 🔧 Pré-requisitos

Antes de começar, você precisará ter as seguintes ferramentas instaladas em sua máquina:

- Python 3.9+
- pip  
- Git  
- Docker *(Opcional, para execução com container)*

---

## 🚀 Instalação e Execução

### Localmente

Clone o repositório:
```bash
git clone https://seu-repositorio-aqui.git
cd nome-do-projeto
````

Crie e ative um ambiente virtual (recomendado):

```bash
# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Para Windows
python -m venv venv
.\venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

(Opcional) Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto.

Execute a aplicação:

```bash
flask run
# ou
python app.py
```

### Com Docker

Certifique-se de que o **Docker** e o **Docker Compose** estejam instalados.

Construa e suba os containers:

```bash
docker-compose up --build
```

A aplicação estará disponível em:
👉 [http://localhost:<PORTA>](http://localhost:<PORTA>) *(verifique a porta no seu docker-compose.yml)*

---

## API_DOC 📖 Documentação da API

### URL Base

```
http://localhost:5000/api
```

*(Altere se for diferente)*

---

## 📊 Modelos de Dados

### 🧑‍🎓 Aluno

| Campo                  | Tipo          | Descrição                        |
| ---------------------- | ------------- | -------------------------------- |
| id                     | Integer       | Identificador único do aluno.    |
| nome                   | String        | Nome completo do aluno.          |
| idade                  | Integer       | Idade do aluno.                  |
| turma_id               | Integer       | FK para a turma do aluno.        |
| data_nascimento        | String (Date) | Data de nascimento (YYYY-MM-DD). |
| nota_primeiro_semestre | Float         | Nota do primeiro semestre.       |
| nota_segundo_semestre  | Float         | Nota do segundo semestre.        |
| media_final            | Float         | Média final (calculada).         |

---

### 👩‍🏫 Professor

| Campo       | Tipo    | Descrição                         |
| ----------- | ------- | --------------------------------- |
| id          | Integer | Identificador único do professor. |
| nome        | String  | Nome completo do professor.       |
| idade       | Integer | Idade do professor.               |
| materia     | String  | Matéria que o professor leciona.  |
| observacoes | String  | Observações adicionais.           |

---

### 🏫 Turma

| Campo        | Tipo    | Descrição                        |
| ------------ | ------- | -------------------------------- |
| id           | Integer | Identificador único da turma.    |
| descricao    | String  | Nome/descrição da turma.         |
| professor_id | Integer | FK para o professor responsável. |
| ativo        | Boolean | Indica se a turma está ativa.    |

---

### 📝 Atividade

| Campo          | Tipo          | Descrição                         |
| -------------- | ------------- | --------------------------------- |
| id             | Integer       | Identificador único da atividade. |
| nome_atividade | String        | Nome da atividade.                |
| descricao      | String        | Descrição detalhada.              |
| peso_porcento  | Float         | Peso percentual da atividade.     |
| data_entrega   | String (Date) | Data limite (YYYY-MM-DD).         |
| id_turma       | Integer       | FK da turma associada.            |
| id_professor   | Integer       | FK do professor associado.        |

---

### 📈 Notas

| Campo        | Tipo    | Descrição                    |
| ------------ | ------- | ---------------------------- |
| id           | Integer | Identificador único da nota. |
| nota         | Float   | Valor da nota.               |
| id_aluno     | Integer | FK do aluno vinculado.       |
| id_atividade | Integer | FK da atividade vinculada.   |

---

### 🧾 Reserva

| Campo    | Tipo          | Descrição                       |
| -------- | ------------- | ------------------------------- |
| id       | Integer       | Identificador único da reserva. |
| num_sala | String        | Número da sala ou laboratório.  |
| lab      | String        | Nome do laboratório.            |
| data     | String (Date) | Data da reserva (YYYY-MM-DD).   |
| id_turma | Integer       | FK da turma que fará a reserva. |

---

## 🔗 Endpoints

### 🎓 AlunoController

#### `GET /lista_aluno`

Retorna todos os alunos cadastrados.

```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "idade": 18,
    "turma_id": 1,
    "data_nascimento": "2007-05-15",
    "nota_primeiro_semestre": 8.5,
    "nota_segundo_semestre": 9.0,
    "media_final": 8.75
  }
]
```

#### `POST /criar_aluno`

Cria um novo aluno.

```json
{
  "nome": "João Silva",
  "idade": 18,
  "turma_id": 1,
  "data_nascimento": "2007-05-15",
  "nota_primeiro_semestre": 8.5,
  "nota_segundo_semestre": 9.0,
  "media_final": 8.75
}
```

✅ **201 Created**

```json
{ "mensagem": "Aluno adicionado com sucesso!" }
```

❌ **400 Bad Request**

```json
{ "erro": "Dados inválidos ou faltando." }
```

---

### 👩‍🏫 ProfessorController

#### `GET /lista_professores`

Retorna todos os professores cadastrados.

```json
[
  {
    "id": 1,
    "nome": "Ana Martins",
    "idade": 45,
    "materia": "Matemática",
    "observacoes": "Professora experiente"
  }
]
```

#### `POST /criar_professor`

Cria um novo professor.

```json
{
  "nome": "Ana Martins",
  "idade": 45,
  "materia": "Matemática",
  "observacoes": "Professora experiente"
}
```

✅ **201 Created**

```json
{ "mensagem": "Professor criado com sucesso!" }
```

---

### 🏫 TurmaController

#### `GET /lista_turmas`

Retorna todas as turmas cadastradas.

```json
[
  {
    "id": 1,
    "descricao": "Turma de T.I.",
    "professor_id": 1,
    "ativo": true
  }
]
```

#### `POST /cria_turmas`

Cria uma nova turma.

```json
{
  "descricao": "Turma de T.I.",
  "professor_id": 1,
  "ativo": true
}
```

✅ **201 Created**

```json
{ "mensagem": "Turma criada com sucesso!" }
```

---

### 🧾 AtividadeController

#### `GET /lista_atividades`

Lista todas as atividades cadastradas.

```json
[
  {
    "id": 1,
    "nome_atividade": "Prova 1",
    "descricao": "Prova sobre Banco de Dados",
    "peso_porcento": 25.5,
    "data_entrega": "2025-10-01",
    "turma_id": 1,
    "professor_id": 1
  }
]
```

---

### 📈 NotasController

#### `GET /lista_notas`

Lista todas as notas cadastradas.

```json
[
  {
    "id": 1,
    "nota": 8.5,
    "id_aluno": 1,
    "id_atividade": 1
  }
]
```

---

### 🧮 ReservaController

#### `GET /lista_reservas`

Lista todas as reservas de salas/laboratórios.

```json
[
  {
    "id": 1,
    "num_sala": "101A",
    "lab": "Laboratório de Redes",
    "data": "2025-10-30",
    "id_turma": 1
  }
]
```

---

## 👥 Autores

| Nome                      | RA      |
| ------------------------- | ------- |
| **Nicolas Lopes Miranda** | 2403929 |
| **Eric Miguel**           | 2402345 |

---

## 📄 Licença

Este projeto é licenciado sob a **MIT License**.
Consulte o arquivo `LICENSE` para mais detalhes.

```

---

Deseja que eu gere esse Markdown como **arquivo `.md` (pronto para GitHub)** para download também?
```
