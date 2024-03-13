# Requisitions API

A Requisitions API foi desenhada para facilitar a gestão de requisições de compra, serviços e fretes. Ela permite que usuários criem, atualizem, leiam e deletem informações sobre contratos, departamentos, fretes, produtos, fornecedores, compras, serviços, transportadoras e usuários.

## ✔️ Tecnologias usadas
- Python
- Django
- Django Rest Framework
- PostgreSQL
- Simple JWT
- Swagger/Redoc
- Vercel

## 📁 Acesso ao deploy

[![Deploy with Vercel](https://vercel.com/button)](https://requisitions-api.vercel.app/)

## 🔨 Funcionalidades

- **Gestão de Contratos**: Crie, atualize, leia e delete contratos.
- **Gestão de Departamentos**: Gerencie informações dos departamentos.
- **Gestão de Fretes**: Inclui a criação de fretes e a cotação para estes.
- **Gestão de Produtos**: Adicione e gerencie produtos.
- **Gestão de Fornecedores**: Mantenha o cadastro de fornecedores atualizado.
- **Gestão de Compras**: Gerencie compras e os produtos relacionados a estas.
- **Gestão de Serviços**: Inclui a gestão de serviços e seus tipos.
- **Autenticação**: Sistema de tokens para acesso seguro à API.
- **Gestão de Transportadoras**: Cadastro e gestão de transportadoras.
- **Gestão de Usuários**: Administração de usuários que podem acessar a API.

## 📌 Uso

A Requisitions API segue os princípios REST para comunicação. Os seguintes endpoints estão disponíveis:

### /contracts/
- Listar, criar, ler detalhes, atualizar, e deletar contratos.

### /departments/
- Listar, criar, ler detalhes, atualizar, e deletar departamentos.

### /freights/
- Listar, criar fretes, ler detalhes, atualizar, deletar, e gerenciar cotações de fretes.

### /products/
- Listar, criar produtos, ler detalhes, atualizar, e deletar produtos.

### /providers/
- Listar, criar fornecedores, ler detalhes, atualizar, e deletar fornecedores.

### /purchases/
- Listar compras, criar, ler detalhes, atualizar, deletar, e gerenciar produtos associados às compras.

### /services/
- Gerenciar serviços, tipos de serviços, e realizar operações CRUD.

### /transporters/
- Listar, criar transportadoras, ler detalhes, atualizar, e deletar transportadoras.

### /users/
- Gerenciar usuários e realizar operações CRUD.

## 🔐 Autenticação

A autenticação é realizada através de JWT. Utilize a rota `/token/` para obter um token de acesso, enviando as credenciais do usuário. Utilize este token nas requisições subsequentes para autenticar.

## 🛠️ Abrindo e rodando o projeto

Para configurar a Requisitions API em seu ambiente, siga estas etapas:

1. Clone o repositório do projeto para sua máquina local.
2. Configure o ambiente virtual para Python e ative-o.
3. Instale as dependências do projeto
```bash
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente necessárias para a conexão com o banco de dados e outras configurações de sistema.
5. Execute as migrações do banco de dados
```bash
python manage.py migrate
```
6. Crie um super usuário para ter acesso a `/admin/`
```bash
python manage.py createsuperuser
```
7. Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```
