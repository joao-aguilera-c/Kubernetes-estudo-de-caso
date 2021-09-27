# Kubernetes, Estudo de Caso
Esta é uma versão demo, apenas para teste, de um programa chamado Lista de Tarefas, construido on top de uma arquitetura do Kubernetes.

## App: Lista de Tarefas
O app é uma limples lista de tarefas, com as funcionalidades de adicionar, excluir e editar tarefas. Escrito em python, html e com DB sqlite

<p align="center">
  <img src="https://user-images.githubusercontent.com/68448759/134955365-1ec005ff-f84c-4fb6-a577-e6ff1bdd1db7.PNG" />
</p>

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


