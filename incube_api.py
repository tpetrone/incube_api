from flask import Flask, url_for, request, jsonify, render_template, abort, make_response
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'incube.db')
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
                                         
                                         
class Carro(db.Model):
	__tablename__ = 'pos_carros'
	id = db.Column(db.Integer, primary_key = True)
	placa = db.Column(db.String)
	lat = db.Column(db.Float(6))
	lng = db.Column(db.Float(6))
	hora = db.Column(db.DateTime)
	def __init__(self, placa, lat, lng, hora = None):
		self.placa = placa
		self.lat = lat
		self.lng = lng
		if hora is None:
			hora = datetime.utcnow()
			self.hora = hora
@auth.get_password
def get_password(username):
    if username == 'incube':
        return 'incube'
    return None
    
@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
    
#GET ALL
@app.route('/incube_api/', methods=['GET'])
def get_carros():
	if request.method == 'GET':
		lim = request.args.get('limit', 100)
		off = request.args.get('offset', 0)
		results = Carro.query.all()
		json_results = []
		for result in results:
			d = {
			'placa':result.placa,
			'uri': url_for('get_carro', cod = result.id, _external=True),
			'lat': result.lat,
			'lng': result.lng,
			'hora': result.hora}
			json_results.append(d)
		return jsonify(carros=json_results)
 
#GET ONE
@app.route('/incube_api/<int:cod>', methods=['GET'])
def get_carro(cod):
	if request.method == 'GET':
		result = Carro.query.filter_by(id=cod).first()
		if result:
			d = {
			'placa': result.placa,
			'uri': url_for('get_carro', cod = cod, _external=True),
			'lat': result.lat,
			'lng': result.lng}
			return jsonify(carros=d)
		else:
			abort(403)
#ADD
@app.route('/incube_api/', methods=['POST'])
@auth.login_required
def post_carro():
	if request.method == 'POST':
		json = request.get_json()
		placa = json['placa']
		result = Carro.query.filter_by(placa=placa).first()
		if not result:	
			carro = Carro(json['placa'], None, None)
			db.session.add(carro)
			db.session.commit()
			result = Carro.query.filter_by(placa=placa).first()
			d = {
			'placa': result.placa,
			'uri': url_for('get_carro', cod = result.id, _external=True),
			'lat': result.lat,
			'lng': result.lng}
			return jsonify({'adicionado' : d}), 200
		else:
			abort(403)
#UPDATE	
@app.route('/incube_api/<int:cod>', methods=['PUT'])
@auth.login_required
def put_carro(cod):
	if request.method == 'PUT':
		result = Carro.query.filter_by(id=cod).first()
		if result:
			json = request.get_json()
			d = {
			'placa': result.placa,
			'uri': url_for('get_carro', cod = cod, _external=True),
			'lat': json['lat'],
			'lng': json['lng']}
			result.lat = json['lat']
			result.lng = json['lng']
			db.session.commit()
			return jsonify({'atualizado' : d}), 200
		else:
			abort(403)
#REMOVE	
@app.route('/incube_api/<int:cod>', methods=['DELETE'])
@auth.login_required
def delete_carro(cod):
	if request.method == 'DELETE':
		result = Carro.query.filter_by(id=cod).first()
		if result:
			d = {
			'placa': result.placa,
			'uri': url_for('get_carro', cod = result.id, _external=True)}
			db.session.delete(result)
			db.session.commit()	
			return jsonify({'Removido' : d}), 200
		else:
			abort(403)
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int("5000"), debug=True)

