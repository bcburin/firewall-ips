# Firewall-Rules-Predictions

## Ferramentas necessárias:

- **Python (^v3.10.12):** para executar o lado servidor
- **Node (^v20.15.1):** para servir o cliente de navegador

## Dependências

- As dependências do lado servidor estão no arquivo `requirements.txt`, que podem ser instaladas via CLI com o comando `pip install -r requirements.txt`, preferencialmente em um virtual environment do Python.
- As dependências do cliente de navegador estão especificadas em `client/package.json`, para instalá-las basta utilizar `npm install`.

## Configuração do dataset

Caso haja alterações na base de dados utilizada, o arquivo `dataset.json` deve ser atualizado com as informações da nova base. Essas informações são: nome, tipo e a flag mustInclude (que determina se a variável deve estar obrigatoriamente nas regras criadas)

## Configurações do modelo

Caso sejam adicionados novos modelos, deve-se alterar o arquivo `models.json`, especificando os valores dos hiperparâmetros.

## Configurações de servidor

***Configuração Geral:***
  - host: define o endereço IP do servidor, recomenda-se utilizar 127.0.0.1 (localhost).
  - port: a porta que o servidor escutará para receber requisições (exemplo: 8000).
***Banco de Dados***
  - name: Nome do banco de dados (padrão: fw-rules).
  - host: Endereço IP do banco de dados.
  - port: Porta do servidor do banco de dados (padrão: 5432 para PostgreSQL).
  - dbms: Sistema de Gerenciamento de Banco de Dados (SGBD) relacional utlizado, recomenda-se o PostgresSQL.
  - user e password: Credenciais de autenticação do banco de dados.
  - verbose: se true, exibe detalhes das operações de banco de dados.
***Módulo de IA***
  - cronString: cron string para determinar a recorrencia da tarefa de retreinamento. 
  - runOnStart: determina se o treinamento deve ser iniciado no startup do sistema (false).
  - directory: diretório onde os modelos treinados são salvos.
  - maxSavedModels: número máximo de modelos a serem mantidos.
  - loadLatestOnStart: se true, carrega o último modelo salvo na inicialização.
  - enable: Se true, habilita a compressão dos modelos.
  - tool: Ferramenta de compressão usada (padrão: zip).
***Notificações***
  - enable: Habilita o envio de notificações.
  - maxQueueSize: Limita o número máximo de notificações na fila.
  - cronString: Configura a frequência das notificações (a cada minuto).
  - Métodos de Notificação (Email)
  - subject: Assunto do email, contendo o número de regras criadas.
  - templatePath: Caminho para o template do email (arquivo Jinja2).
  - server: Servidor SMTP (localhost).
  - port: Porta do servidor SMTP (1025).
  - sender: Detalhes do remetente.
  - mailingList: Lista de destinatários do email.
***Autenticação***
  - Token JWT
  - key: Chave secreta para geração de tokens JWT.
  - algorithm: Algoritmo de criptografia (HS256).
  - expirationTimeInMinutes: Tempo de expiração do token (30 minutos).
  - method: Método de autenticação (JWT).
  - maxLoginTries: Número máximo de tentativas de login.
  - notifyOnMaxTries: Notifica se o número máximo de tentativas for atingido.
  - devMode: Ativa ou desativa o modo de desenvolvimento (true).
  - Informações do Firewall
  - chain: Define a cadeia de regras do firewall.
  - table: Define a tabela de regras do firewall.
***Credenciais do Executor***
  - ssh_host: Host para conexão SSH.
  - ssh_user: Usuário SSH.
  - ssh_key_path: Caminho para a chave SSH.

## Como executar os serviços

- Cliente de navegador:
```bash
npm run build
npm install -g serve
serve -s build
```

- Servidor:
```bash
python -m src.main
```