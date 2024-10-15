# Manual de Usuário

Este manual fornece instruções detalhadas para analistas de segurança da informação utilizarem o sistema. Ele cobre casos de uso relacionados ao login, gerenciamento de usuários e gerenciamento de regras críticas.

## 1. Login

### Descrição
Este caso descreve o processo de autenticação no sistema, permitindo que o usuário acesse as funcionalidades disponíveis com base em suas permissões.

### Pré-condições
- O usuário deve estar registrado no sistema.

### Fluxo principal
1. Acessar a página de login do sistema.
2. A página exibirá os campos "Usuário" e "Senha" e os botões "Entrar" e "Esqueci minha senha".
3. Insira o nome de usuário ou e-mail e a senha.
4. Clique no botão "Entrar".
5. Se as credenciais estiverem corretas, o sistema redirecionará para a página inicial.

### Fluxos alternativos
- Se as credenciais estiverem incorretas:
  - O usuário poderá tentar novamente, até que o número máximo de tentativas seja atingido.
  - Após o número máximo de tentativas, o sistema bloqueará o usuário e enviará notificações por e-mail para o usuário e administradores.

### Pós-condições
- O usuário autenticado terá acesso aos recursos disponíveis com base em suas permissões.

---

## 2. Gerenciamento de Usuários

### Descrição
Este caso descreve o processo de cadastro, atualização e remoção de usuários no sistema.

### Pré-condições
- O administrador deve estar autenticado para realizar ações de gerenciamento de usuários.

### Fluxo principal
1. O sistema exibirá uma interface com um botão "Criar" e uma tabela listando os usuários cadastrados.
2. Para criar um novo usuário, clique no botão "Criar", preencha os campos no modal exibido e clique em "Criar".
3. Para atualizar um usuário existente, clique no botão "Atualizar" ao lado do usuário desejado, faça as modificações no modal exibido e clique em "Atualizar".
4. Para remover um usuário, clique no botão "Remover" e confirme a remoção no modal exibido.

### Fluxos alternativos
- Se a remoção de um usuário não for confirmada, o cadastro permanecerá inalterado.

### Pós-condições
- Um usuário será criado, atualizado ou removido conforme as ações do administrador.

---

## 3. Gerenciamento de Regras Críticas

### Descrição
Este caso descreve o processo de visualização, cadastro, atualização e remoção de regras críticas.

### Pré-condições
- O usuário deve estar autenticado para gerenciar regras críticas.

### Fluxo principal
1. O sistema exibirá uma interface com um botão "Criar" e uma tabela listando as regras críticas.
2. Para criar uma nova regra, clique no botão "Criar", preencha os campos da regra (como portas, endereços, tempos de início e fim, e prioridade) e clique em "Criar".
3. Para atualizar uma regra, clique no botão "Atualizar", modifique as informações no modal exibido e clique em "Atualizar".
4. Para remover uma regra, clique no botão "Remover" e confirme a remoção no modal exibido.

### Fluxos alternativos
- Se as datas de início e fim forem inválidas (por exemplo, a data de início maior que a de fim), o sistema solicitará a correção das informações.
- Se a remoção não for confirmada, a regra permanecerá inalterada.

### Pós-condições
- Uma regra crítica será cadastrada, atualizada ou removida conforme a solicitação do usuário.
