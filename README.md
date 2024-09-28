# Gerenciamento Centralizado de Logs com rsyslog e MySQL
Este projeto configura um sistema de gerenciamento centralizado de logs utilizando rsyslog para coletar logs de hosts remotos, armazená-los em um banco de dados MySQL e filtrá-los/processá-los através de um script em Python.

# Visão Geral do Projeto
O sistema permite o armazenamento e processamento centralizado de logs provenientes de diversas fontes (clientes Linux e Windows) usando rsyslog. Os logs são recebidos no servidor, analisados, filtrados e armazenados em um banco de dados MySQL, facilitando a análise e o monitoramento. Um script em Python processa os logs a cada hora, filtrando entradas desnecessárias e inserindo os dados relevantes no banco de dados.

# Principais Funcionalidades
Armazenamento Centralizado de Logs: Recebe e armazena logs de múltiplos clientes via UDP/TCP utilizando rsyslog.
Processamento Automatizado de Logs: Script em Python que analisa, filtra e organiza os logs para fácil inserção no banco de dados.
Integração com MySQL: Logs são armazenados em um banco de dados MySQL com metadados, como data, hora, usuário, tipo de log e host de origem.
Suporte a Clientes Remotos: Configurado para clientes Linux e Windows, que enviam logs para o servidor central.

# Tecnologias Utilizadas
rsyslog: Para recebimento e encaminhamento de logs.
Python: Para filtrar logs e automatizar a inserção no banco de dados.
MySQL: Banco de dados para armazenar e consultar logs.

# Configuração do Projeto
Pré-requisitos:
Servidor Linux (VM ou Docker)
Servidor MySQL
Python 3.x e bibliotecas necessárias (ex: mysql-connector-python)
rsyslog instalado e configurado no servidor e nas máquinas clientes

# Instalação
Instale e configure o rsyslog no servidor para receber logs dos clientes.
Crie o banco de dados e as tabelas necessárias no MySQL para armazenar os logs.
Configure o script Python para processar os logs e enviá-los ao banco de dados.
Configure os clientes remotos (Linux ou Windows) para encaminhar os logs ao servidor.

# Uso
O servidor coletará os logs dos clientes remotos via rsyslog.
A cada hora, o script em Python processa os logs e armazena os dados relevantes (tipo de log, usuário, prioridade, nome do host, etc.) no banco de dados MySQL.
Os logs podem ser consultados diretamente no banco de dados para análise.
