# Projeto API Escolar

API para gerenciamento de alunos, professores e turmas.

## Índice

- [Configuração](#configuração)
- [Endpoints](#endpoints)
  - [Alunos](#alunos)
  - [Professores](#professores)
  - [Turmas](#turmas)
- [Como Usar](#como-usar)
- [Contribuição](#contribuição)

---

## Configuração

- O arquivo `Config` define as configurações do Flask e do banco de dados SQLite.
- O projeto utiliza Docker para facilitar a execução e isolamento do ambiente.
- As dependências estão listadas em `requirements.txt`.

---

## Endpoints

### Alunos

- **`GET /lista_aluno`**  
  Lista todos os alunos cadastrados.
  - **Retorno:** JSON com a lista de alunos.

- **`POST /criar_aluno`**  
  Cria um novo aluno.
  - **Body:** JSON com os dados do aluno.
  - **Retorno:** JSON com o aluno criado.

- **`PUT /atualiza_aluno/<int:id>`**  
  Atualiza os dados de um aluno pelo ID.
  - **Parâmetros:**  
    - `id` (int): ID do aluno a ser atualizado.
  - **Body:** JSON com os dados atualizados.
  - **Retorno:** JSON com o aluno atualizado.

- **`DELETE /deleta_aluno/<int:id>`**  
  Remove um aluno pelo ID.
  - **Parâmetros:**  
    - `id` (int): ID do aluno a ser removido.
  - **Retorno:** Mensagem de sucesso ou erro.

---

### Professores

- **`GET /lista_professor`**  
  Lista todos os professores cadastrados.
  - **Retorno:** JSON com a lista de professores.

- **`POST /adiciona_professor`**  
  Adiciona um novo professor.
  - **Body:** JSON com os dados do professor.
  - **Retorno:** JSON com o professor criado.

- **`PUT /atualiza_professor/<int:id>`**  
  Atualiza os dados de um professor pelo ID.
  - **Parâmetros:**  
    - `id` (int): ID do professor a ser atualizado.
  - **Body:** JSON com os dados atualizados.
  - **Retorno:** JSON com o professor atualizado.

- **`DELETE /deleta_professor/<int:id>`**  
  Remove um professor pelo ID.
  - **Parâmetros:**  
    - `id` (int): ID do professor a ser removido.
  - **Retorno:** Mensagem de sucesso ou erro.

---

### Turmas

- **`GET /lista_turmas`**  
  Lista todas as turmas cadastradas.
  - **Retorno:** JSON com a lista de turmas.

- **`POST /cria_turmas`**  
  Cria uma nova turma.
  - **Body:** JSON com os dados da turma.
  - **Retorno:** JSON com a turma criada.

- **`PUT /atualiza_turmas/<int:id>`**  
  Atualiza os dados de uma turma pelo ID.
  - **Parâmetros:**  
    - `id` (int): ID da turma a ser atualizada.
  - **Body:** JSON com os dados atualizados.
  - **Retorno:** JSON com a turma atualizada.

- **`DELETE /deleta_turmas/<int:id>`**  
  Remove uma turma pelo ID.
  - **Parâmetros:**  
    - `id` (int): ID da turma a ser removida.
  - **Retorno:** Mensagem de sucesso ou erro.

---

## Como Usar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt