# Sistema de Gerenciamento Escolar

API RESTful para gerenciamento de **alunos**, **professores** e **turmas**.

---

## Índice

- [Controllers](#controllers)
  - [AlunoController](#alunocontroller)
  - [ProfessorController](#professorcontroller)
  - [TurmaController](#turmacontroller)
- [Como Usar](#como-usar)
- [Contribuição](#contribuição)

---

## Controllers

### AlunoController

Controlador responsável pelo gerenciamento dos alunos.

#### `listar()`
- **Método HTTP:** GET  
- **Endpoint:** `/lista_aluno`  
- **Descrição:** Retorna todos os alunos cadastrados.  
- **Resposta 200:**  
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

#### `criar()`
- **Método HTTP:** POST  
- **Endpoint:** `/criar_aluno`  
- **Descrição:** Cria um novo aluno.  
- **Body (JSON):**
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
- **Resposta 201:**  
  ```json
  { "mensagem": "Aluno adicionado com sucesso!" }
  ```
- **Resposta 400:**  
  ```json
  { "erro": "Dados inválidos ou faltando." }
  ```

#### `atualizar(id)`
- **Método HTTP:** PUT  
- **Endpoint:** `/atualiza_aluno/<int:id>`  
- **Descrição:** Atualiza um aluno existente.  
- **Body (JSON):**
  ```json
  { "nome": "Maria Souza", "nota_primeiro_semestre": 9.0 }
  ```
- **Resposta 200:**  
  ```json
  { "mensagem": "Aluno atualizado com sucesso!" }
  ```
- **Resposta 404:**  
  ```json
  { "erro": "Aluno não encontrado." }
  ```

#### `deletar(id)`
- **Método HTTP:** DELETE  
- **Endpoint:** `/deleta_aluno/<int:id>`  
- **Descrição:** Remove um aluno.  
- **Resposta 200:**  
  ```json
  { "mensagem": "Aluno removido com sucesso!" }
  ```
- **Resposta 404:**  
  ```json
  { "erro": "Aluno não encontrado." }
  ```

---

### ProfessorController

Controlador responsável pelo gerenciamento dos professores.

#### `listar()`
- **Método HTTP:** GET  
- **Endpoint:** `/lista_professores`  
- **Descrição:** Retorna todos os professores cadastrados.  
- **Resposta 200:**  
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

#### `criar()`
- **Método HTTP:** POST  
- **Endpoint:** `/criar_professor`  
- **Descrição:** Cria um novo professor.  
- **Body (JSON):**
  ```json
  {
    "nome": "Ana Martins",
    "idade": 45,
    "materia": "Matemática",
    "observacoes": "Professora experiente"
  }
  ```
- **Resposta 201:**  
  ```json
  { "mensagem": "Professor criado com sucesso!" }
  ```

#### `atualizar(id)`
- **Método HTTP:** PUT  
- **Endpoint:** `/atualiza_professor/<int:id>`  
- **Descrição:** Atualiza um professor existente.  
- **Body (JSON):**
  ```json
  { "materia": "Física" }
  ```
- **Resposta 200:**  
  ```json
  { "mensagem": "Professor atualizado com sucesso!" }
  ```
- **Resposta 404:**  
  ```json
  { "erro": "Professor não encontrado." }
  ```

#### `deletar(id)`
- **Método HTTP:** DELETE  
- **Endpoint:** `/deleta_professor/<int:id>`  
- **Descrição:** Remove um professor.  
- **Resposta 200:**  
  ```json
  { "mensagem": "Professor deletado com sucesso!" }
  ```
- **Resposta 404:**  
  ```json
  { "erro": "Professor não encontrado." }
  ```

---

### TurmaController

Controlador responsável pelo gerenciamento das turmas.

#### `listar()`
- **Método HTTP:** GET  
- **Endpoint:** `/lista_turmas`  
- **Descrição:** Retorna todas as turmas cadastradas.  
- **Resposta 200:**  
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

#### `criar()`
- **Método HTTP:** POST  
- **Endpoint:** `/cria_turmas`  
- **Descrição:** Cria uma nova turma.  
- **Body (JSON):**
  ```json
  {
    "descricao": "Turma de T.I.",
    "professor_id": 1,
    "ativo": true
  }
  ```
- **Resposta 200:**  
  ```json
  { "mensagem": "Turma criada com sucesso!" }
  ```

#### `atualizar(id)`
- **Método HTTP:** PUT  
- **Endpoint:** `/atualiza_turmas/<int:id>`  
- **Descrição:** Atualiza uma turma existente.  
- **Body (JSON):**
  ```json
  { "descricao": "Turma de Robótica", "ativo": false }
  ```
- **Resposta 200:**  
  ```json
  { "mensagem": "Turma atualizada com sucesso!" }
  ```
- **Resposta 404:**  
  ```json
  { "erro": "Turma não encontrada." }
  ```

#### `deletar(id)`
- **Método HTTP:** DELETE  
- **Endpoint:** `/deleta_turmas/<int:id>`  
- **Descrição:** Remove uma turma.  
- **Resposta 200:**  
  ```json
  { "mensagem": "Turma deletada com sucesso!" }
  ```
- **Resposta 404:**  
  ```json
  { "erro": "Turma não encontrada." }
  ```

---

## Como Usar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Construa a imagem de acordo com o `dockerfile`:
   ```bash
   docker-compose up --build
   ```


nomes: Nicolas Lopes Miranda, Eric Miguel
RA: 2403929, 2402345
