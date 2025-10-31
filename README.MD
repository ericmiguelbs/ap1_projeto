Sistema de Gerenciamento EscolarAPI RESTful para gerenciamento de alunos, professores, turmas, atividades, notas e reservas em uma instituição de ensino.📖 ÍndiceFuncionalidadesTecnologias UtilizadasPré-requisitosInstalação e ExecuçãoLocalmenteCom DockerDocumentação da APIBaseModelos de DadosEndpointsAlunoControllerProfessorControllerTurmaControllerAtividadeControllerNotasControllerReservaControllerComo ContribuirAutoresLicença💡 Funcionalidades[X] CRUD completo para Alunos[X] CRUD completo para Professores[X] CRUD completo para Turmas[X] CRUD completo para Atividades (com validação externa)[X] CRUD completo para Notas (com validação externa)[X] CRUD completo para Reservas (com validação externa)💻 Tecnologias UtilizadasEste projeto foi construído utilizando as seguintes tecnologias:Backend: PythonFramework: FlaskContainerização: Docker e Docker ComposeComunicação: API REST com validações entre microsserviços.🔧 Pré-requisitosAntes de começar, você precisará ter as seguintes ferramentas instaladas em sua máquina:Python 3.9+pipGitDocker (Opcional, para execução com container)🚀 Instalação e ExecuçãoSiga os passos abaixo para executar o projeto.LocalmenteClone o repositório:git clone https://seu-repositorio-aqui.git
cd nome-do-projeto
Crie e ative um ambiente virtual (recomendado):# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Para Windows
python -m venv venv
.\venv\Scripts\activate
Instale as dependências:pip install -r requirements.txt
(Opcional) Configure as variáveis de ambiente. Crie um arquivo .env na raiz do projeto, se necessário.Execute a aplicação:# (Comando pode variar dependendo de como seu app está configurado)
flask run
# ou
python app.py
Com DockerCertifique-se de que o Docker e o Docker Compose estejam instalados.Construa e suba os containers:docker-compose up --build
A aplicação estará disponível em http://localhost:<PORTA> (verifique a porta no seu docker-compose.yml).API_DOC 📖 Documentação da APIURL BaseA URL base para todos os endpoints da API é:http://localhost:5000/api (Altere se for diferente)Modelos de DadosAlunoCampoTipoDescriçãoidIntegerIdentificador único do aluno.nomeStringNome completo do aluno.idadeIntegerIdade do aluno.turma_idIntegerFK para a turma do aluno.data_nascimentoString (Date)Data de nascimento (YYYY-MM-DD).nota_primeiro_semestreFloatNota do primeiro semestre.nota_segundo_semestreFloatNota do segundo semestre.media_finalFloatMédia final (calculada).ProfessorCampoTipoDescriçãoidIntegerIdentificador único do professor.nomeStringNome completo do professor.idadeIntegerIdade do professor.materiaStringMatéria que o professor leciona.observacoesStringObservações adicionais.TurmaCampoTipoDescriçãoidIntegerIdentificador único da turma.descricaoStringDescrição/Nome da turma (ex: "Turma de T.I.").professor_idIntegerFK para o professor responsável.ativoBooleanIndica se a turma está ativa.AtividadeCampoTipoDescriçãoidIntegerIdentificador único da atividade.nome_atividadeStringNome da atividade.descricaoStringDescrição detalhada da atividade.peso_porcentoFloatO peso (percentual) da atividade na nota.data_entregaString (Date)Data limite para entrega (YYYY-MM-DD).id_turmaIntegerFK para a turma associada.id_professorIntegerFK para o professor associado.NotasCampoTipoDescriçãoidIntegerIdentificador único da nota.notaFloatO valor da nota.id_alunoIntegerFK para o aluno vinculado.id_atividadeIntegerFK para a atividade vinculada.ReservaCampoTipoDescriçãoidIntegerIdentificador único da reserva.num_salaStringNúmero da sala ou laboratório.labStringNome do laboratório (ex: "Laboratório de Redes").dataString (Date)Data da reserva (YYYY-MM-DD).id_turmaIntegerFK para a turma que fará a reserva.EndpointsAlunoControllerControlador responsável pelo gerenciamento dos alunos.listar()Método HTTP: GETEndpoint: /lista_alunoDescrição: Retorna todos os alunos cadastrados.Resposta 200 (OK):[
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
criar()Método HTTP: POSTEndpoint: /criar_alunoDescrição: Cria um novo aluno.Body (JSON):{
  "nome": "João Silva",
  "idade": 18,
  "turma_id": 1,
  "data_nascimento": "2007-05-15",
  "nota_primeiro_semestre": 8.5,
  "nota_segundo_semestre": 9.0,
  "media_final": 8.75
}
Resposta 201 (Created):{ "mensagem": "Aluno adicionado com sucesso!" }
Resposta 400 (Bad Request):{ "erro": "Dados inválidos ou faltando." }
atualizar(id)Método HTTP: PUTEndpoint: /atualiza_aluno/<int:id>Descrição: Atualiza um aluno existente.Body (JSON):{ "nome": "Maria Souza", "nota_primeiro_semestre": 9.0 }
Resposta 200 (OK):{ "mensagem": "Aluno atualizado com sucesso!" }
Resposta 404 (Not Found):{ "erro": "Aluno não encontrado." }
deletar(id)Método HTTP: DELETEEndpoint: /deleta_aluno/<int:id>Descrição: Remove um aluno.Resposta 200 (OK):{ "mensagem": "Aluno removido com sucesso!" }
Resposta 404 (Not Found):{ "erro": "Aluno não encontrado." }
ProfessorControllerControlador responsável pelo gerenciamento dos professores.listar()Método HTTP: GETEndpoint: /lista_professoresDescrição: Retorna todos os professores cadastrados.Resposta 200 (OK):[
  {
    "id": 1,
    "nome": "Ana Martins",
    "idade": 45,
    "materia": "Matemática",
    "observacoes": "Professora experiente"
  }
]
criar()Método HTTP: POSTEndpoint: /criar_professorDescrição: Cria um novo professor.Body (JSON):{
  "nome": "Ana Martins",
  "idade": 45,
  "materia": "Matemática",
  "observacoes": "Professora experiente"
}
Resposta 201 (Created):{ "mensagem": "Professor criado com sucesso!" }
atualizar(id)Método HTTP: PUTEndpoint: /atualiza_professor/<int:id>Descrição: Atualiza um professor existente.Body (JSON):{ "materia": "Física" }
Resposta 200 (OK):{ "mensagem": "Professor atualizado com sucesso!" }
Resposta 404 (Not Found):{ "erro": "Professor não encontrado." }
deletar(id)Método HTTP: DELETEEndpoint: /deleta_professor/<int:id>Descrição: Remove um professor.Resposta 200 (OK):{ "mensagem": "Professor deletado com sucesso!" }
Resposta 404 (Not Found):{ "erro": "Professor não encontrado." }
TurmaControllerControlador responsável pelo gerenciamento das turmas.listar()Método HTTP: GETEndpoint: /lista_turmasDescrição: Retorna todas as turmas cadastradas.Resposta 200 (OK):[
  {
    "id": 1,
    "descricao": "Turma de T.I.",
    "professor_id": 1,
    "ativo": true
  }
]
criar()Método HTTP: POSTEndpoint: /cria_turmasDescrição: Cria uma nova turma.Body (JSON):{
  "descricao": "Turma de T.I.",
  "professor_id": 1,
  "ativo": true
}
Resposta 201 (Created):{ "mensagem": "Turma criada com sucesso!" }
atualizar(id)Método HTTP: PUTEndpoint: /atualiza_turmas/<int:id>Descrição: Atualiza uma turma existente.Body (JSON):{ "descricao": "Turma de Robótica", "ativo": false }
Resposta 200 (OK):{ "mensagem": "Turma atualizada com sucesso!" }
Resposta 404 (Not Found):{ "erro": "Turma não encontrada." }
deletar(id)Método HTTP: DELETEEndpoint: /deleta_turmas/<int:id>Descrição: Remove uma turma.Resposta 200 (OK):{ "mensagem": "Turma deletada com sucesso!" }
Resposta 404 (Not Found):{ "erro": "Turma não encontrada." }
AtividadeControllerControlador responsável pelo gerenciamento das atividades.listar()Método HTTP: GETEndpoint: /lista_atividades (Assumido)Descrição: Lista todas as atividades cadastradas.Resposta 200 (OK):[
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
criar()Método HTTP: POSTEndpoint: /criar_atividade (Assumido)Descrição: Cria uma nova atividade. Valida se id_professor e id_turma existem consultando serviços externos.Body (JSON):{
  "nome_atividade": "Prova 1",
  "descricao": "Prova sobre Banco de Dados",
  "peso_porcento": 25.5,
  "data_entrega": "2025-10-01",
  "id_turma": 1,
  "id_professor": 1
}
Resposta 201 (Created):{ "mensagem": "Atividade adicionada com sucesso!" }
Resposta 400 (Bad Request):{ "erro": "Dados inválidos ou faltando (verifique o formato da data AAAA-MM-DD)." }
Resposta 404 (Not Found):{ "erro": "O 'id_professor' ou 'id_turma' não foi encontrado nos serviços externos." }
Resposta 500 (Internal Server Error):{ "erro": "Falha ao consultar os serviços externos de professores ou turmas." }
atualizar(id)Método HTTP: PUTEndpoint: /atualiza_atividade/<int:id> (Assumido)Descrição: Atualiza uma atividade existente. Valida id_professor ou id_turma se eles forem enviados.Body (JSON):{ "descricao": "Descrição atualizada", "peso_porcento": 30.0 }
Resposta 200 (OK):{ "mensagem": "Atividade atualizada com sucesso!" }
Resposta 400 (Bad Request):{ "erro": "Dados inválidos ou faltando (verifique o formato da data AAAA-MM-DD)." }
Resposta 404 (Not Found):{ "erro": "A atividade (ID) não foi encontrada, ou o novo 'id_professor'/'id_turma' não existe." }
Resposta 500 (Internal Server Error):{ "erro": "Falha ao consultar os serviços externos." }
deletar(id)Método HTTP: DELETEEndpoint: /deleta_atividade/<int:id> (Assumido)Descrição: Deleta uma atividade pelo seu ID.Resposta 200 (OK):{ "mensagem": "Atividade deletada com sucesso!" }
Resposta 404 (Not Found):{ "erro": "A atividade com o 'id' fornecido não foi encontrada." }
NotasControllerControlador responsável pelo gerenciamento das notas dos alunos.listar()Método HTTP: GETEndpoint: /lista_notas (Assumido)Descrição: Lista todas as notas cadastradas.Resposta 200 (OK):[
  {
    "id": 1,
    "nota": 8.5,
    "id_aluno": 1,
    "id_atividade": 1
  }
]
criar()Método HTTP: POSTEndpoint: /criar_nota (Assumido)Descrição: Cria uma nova nota para um aluno. Valida se o id_aluno existe consultando um serviço externo.Body (JSON):{
  "nota": 8.5,
  "id_aluno": 1,
  "id_atividade": 1
}
Resposta 201 (Created):{ "mensagem": "nota adicionada com sucesso!" }
Resposta 400 (Bad Request):{ "erro": "Dados inválidos ou faltando (nota, id_aluno, id_atividade)." }
Resposta 404 (Not Found):{ "erro": "O 'id_aluno' enviado não foi encontrado no serviço externo." }
Resposta 500 (Internal Server Error):{ "erro": "Falha ao consultar o serviço externo de alunos." }
atualizar(id)Método HTTP: PUTEndpoint: /atualiza_nota/<int:id> (Assumido)Descrição: Atualiza uma nota existente. Valida id_aluno se for enviado.Body (JSON):{ "nota": 9.0 }
Resposta 200 (OK):{ "mensagem": "Nota atualizada com sucesso!" }
Resposta 400 (Bad Request):{ "erro": "Dados inválidos no JSON enviado." }
Resposta 404 (Not Found):{ "erro": "A nota (pelo ID) não foi encontrada, ou o novo 'id_aluno' não foi encontrado no serviço externo." }
Resposta 500 (Internal Server Error):{ "erro": "Falha ao consultar o serviço externo de alunos." }
deletar(id)Método HTTP: DELETEEndpoint: /deleta_nota/<int:id> (Assumido)Descrição: Deleta uma nota pelo seu ID.Resposta 200 (OK):{ "mensagem": "Nota deletada com sucesso!" }
Resposta 404 (Not Found):{ "erro": "A nota com o 'id' fornecido não foi encontrada." }
ReservaControllerControlador responsável pelo gerenciamento de reservas de salas/laboratórios.listar()Método HTTP: GETEndpoint: /lista_reservas (Assumido)Descrição: Lista todas as reservas de salas/laboratórios.Resposta 200 (OK):[
  {
    "id": 1,
    "num_sala": "101A",
    "lab": "Laboratório de Redes",
    "data": "2025-10-30",
    "id_turma": 1
  }
]
Resposta 500 (Internal Server Error):{ "erro": "Falha ao listar reservas: Erro interno do servidor local." }
criar()Método HTTP: POSTEndpoint: /criar_reserva (Assumido)Descrição: Cria uma nova reserva para uma turma. Valida a existência da turma em um serviço externo.Body (JSON):{
  "num_sala": "101A",
  "lab": "Laboratório de Redes",
  "data": "2025-10-30",
  "id_turma": 1
}
Resposta 201 (Created):{ "mensagem": "reserva adicionada com sucesso!" }
Resposta 400 (Bad Request):{ "erro": "Dados inválidos ou faltando (verifique o formato da data AAAA-MM-DD)." }
Resposta 404 (Not Found):{ "erro": "A turma id_turma não foi encontrada no serviço externo." }
Resposta 500 (Internal Server Error):{ "erro": "Erro interno do servidor (falha de conexão com serviço externo, etc.)." }
atualizar(id)Método HTTP: PUTEndpoint: /atualiza_reserva/<int:id> (Assumido)Descrição: Atualiza uma reserva existente. Valida a turma e a reserva em serviços externos.Body (JSON):{ "num_sala": "102B", "lab": "Laboratório de Hardware" }
Resposta 200 (OK):{ "mensagem": "Reserva atualizada com sucesso!" }
Resposta 400 (Bad Request):{ "erro": "Dados inválidos (ex: formato de data)." }
Resposta 404 (Not Found):{ "erro": "Reserva, Turma ou ID externo não encontrado." }
Resposta 500 (Internal Server Error):{ "erro": "Erro interno ou falha de comunicação com serviços externos." }
deletar(id)Método HTTP: DELETEEndpoint: /deleta_reserva/<int:id> (Assumido)Descrição: Deleta uma reserva pelo seu ID.Resposta 200 (OK):{ "mensagem": "Reserva deletada com sucesso!" }
Resposta 404 (Not Found):{ "erro": "Reserva não encontrada no banco de dados local." }
Resposta 500 (Internal Server Error):{ "erro": "Falha ao deletar a reserva." }
🤔 Como ContribuirContribuições são bem-vindas! Siga estes passos:Faça um Fork do projeto.Crie uma nova Branch: git checkout -b feature/sua-featureFaça Commit das suas mudanças: git commit -m 'Adiciona nova feature'Faça Push para a Branch: git push origin feature/sua-featureAbra um Pull Request.👥 AutoresNomeRANicolas Lopes Miranda2403929Eric Miguel2402345📄 LicençaEste projeto é licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
