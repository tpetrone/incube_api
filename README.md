#Python Rest API

A API está disponível on-line no endereço:
http://191.180.144.139:5000/incube_api/

Propõe-se uma aplicação que possa armazenar e disponibilizar a posição geográfica de uma frota de veículos.
A disponibilização dos dados é feita através do método GET.
A inclusão de novos veículos na frota é feita através do método POST.
O método PUT atualiza a posição de um veículo já existente.
O método DELETE remove o veículo da frota.
A aplicação está protegida por senha; usuário:incube; senha:incube


Essa aplicação foi desenvolvida usando a base de dados Sqlite3, o Flask web framework e o módulo SQLAlchemy.
Abaixo se encontram as instruções para instalação e configuração do servidor (Linux) bem como para a execução e operação da API.

Instalação e configuração:

	mkdir incube_api

	cd incube_api

<b>Base de dados:

Instalação:

	sudo apt-get install sqlite3

Criação da base de dados:

	sqlite3 incube.db

Criação da tabela:

	CREATE TABLE pos_carros(
	ID INTEGER PRIMARY KEY   AUTOINCREMENT,
	PLACA TEXT NOT NULL,
	LAT FLOAT(10,6),
	LNG FLOAT(10,6),
	HORA DATETIME NOT NULL);

Obs.: O arquivo já está disponível (incube.db) com a tabela criada e alguns itens de exemplo.

<b>Flask:

Instalação (através de 'ambiente virtual'):

	sudo apt-get install python-virtualenv
	virtualenv venv
	. venv/bin/activate
	pip install flask
	pip install flask-sqlalchemy
	pip install mysql-python


<b>Execução:
	
	python incube_api.py
	

<b>Operação:
	
Para enviar os comandos para a aplicação pode-se utilizar o programa Curl.

	sudo apt-get install curl	

Método POST:
		
Esse método adiciona um veículo à frota. É necessário prover apenas a placa do veículo a ser adicionado. 
Comando Curl:

	curl -i -H "Content-Type: application/json" -X POST -d '{"placa" : "ABC2348"}' http://localhost:500/incube_api/ -u incube:incube

A aplicação retorna uma uri que deverá ser usada para identificar aquele veículo para futuras consultas e atualizações.


Método GET:

É possível recuperar informações do servidor de duas formas: de todos os veículos através do endereço da API ou de um único através da uri gerada ao adicionar o veículo. 

Endereço da API: http://191.180.144.139:5000/incube_api/
Comando curl:

	curl -i http://191.180.144.139:5000/incube_api/ -u incube:incube

Uri do primeiro carro adicionado à base de dados: http://191.180.144.139:5000/incube_api/1

Comando curl:

	curl -i http://191.180.144.139:5000/incube_api/1 -u incube:incube

Método PUT:

Esse método atualiza a posição do veículo baseado na uri fornecida no método POST.
Para atualizar o veículo é necessário fornecer latitude e longitude em formato json dessa forma:
{"lat" : "-23.76589", "lng" : "-46.87650"}

Comando Curl que atualizaria o primeiro veículo adicionado:

	curl -i -H "Content-Type: application/json" -X PUT -d '{"lat" : "-23.88756", "lng" : "-46.67483"}' http://191.180.144.139:5000/incube_api/1 -u incube:incube

Método DELETE:

Finalmente para remover um veículo da frota deverá ser usado o método DELETE na uri fornecida pelo método POST. Não é necessário nenhum parâmetro adicional.

Comando Curl:

	curl -i -X DELETE http://191.180.144.139:5000/incube_api/1 -u incube:incube







