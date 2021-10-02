# Kubernetes, Estudo de Caso
Esta é uma versão demo, apenas para teste, de um programa chamado Lista de Tarefas, construído sobre uma arquitetura Kubernetes.

## App: Lista de Tarefas
O app é uma simples lista de tarefas, com as funcionalidades de adicionar, excluir e editar tarefas. Escrito em python, html e com DB sqlite

<p align="center">
  <img src="https://user-images.githubusercontent.com/68448759/135730727-e8dee513-061d-4221-a366-21cc525eed38.PNG" />
</p>

### Versão Online
O App está também disponível em cloud, rodando sobre a estrutura do Google Cloud Services e pode ser acessado via: https://tarefaspostgres-r2aix6p4na-uw.a.run.app
O mesmo salva e acessa os dados da lista utilizando uma instância PostgreSQL também hospedada no GCS.
Para mais informações sobre esta versão, acesse a pasta [G Cloud version](https://github.com/joao-aguilera-c/Kubernetes-estudo-de-caso/tree/master/G%20Cloud%20Version) neste repositório.

## Arquitetura
Uma Docker container image foi criada a partir [deste repositório](https://hub.docker.com/repository/docker/aguilerajoao/python).
A partir desta imagem fiz um deploy localmente utilizando o plugin de kubernetes para docker e sua ferramenta para command-line kubectl, utilizando os seguintes comandos:

`docker pull aguilerajoao/python:1.0.0 # recebe a imagem no docker repo`

`kubectl apply -f .\kubernetes\deployments\deployment.yaml # executa o deploy`

---------

Como visto em `deployment.yaml` e `service.yaml` abaixo apresento a arquitetura do cluster criado:

<p align="center">
  <img src="https://user-images.githubusercontent.com/68448759/134965244-d70df5ea-03e4-4a19-81e6-d6e6ccbcfe34.png" />
</p>


