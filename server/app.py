# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        response =  {
            'id': earthquake.id,
            'location':earthquake.location,
            'magnitude': earthquake.magnitude,
            'year':earthquake.year
    } 
        status_code = 200
    else:
        response = {'message': f'Earthquake {id} not found.'}
        status_code = 404

    return make_response(response, status_code)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)
    
    if earthquakes:
            response = {
                'count': count,
                'quakes': [
                    {
                        'id': earthquake.id,
                        'location':earthquake.location,
                        'magnitude':earthquake.magnitude,
                        'year':earthquake.year,
                    }
                  for earthquake in earthquakes]
            }
            
    else:
        response = {
            'count': count,
            'quakes': []
        }

    status_code = 200



    return make_response(response, status_code)


    


if __name__ == '__main__':
    app.run(port=5555, debug=True)