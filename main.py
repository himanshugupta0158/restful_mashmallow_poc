from flask import Flask , jsonify , request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    firstname = db.Column(db.String(50) , nullable=False)
    lastname = db.Column(db.String(50) , nullable=False)
    email = db.Column(db.String(50) , nullable=False)
    password = db.Column(db.String(50) , nullable=False)
    
    

"""
by using marshmallow ,we serialize data from db 
"""
# creating Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id' , 'firstname' , 'lastname' , 'email' , 'password')



@app.route('/users' , methods=['GET' , 'POST'])
def users():
    if request.method == 'GET':
        user1 = User.query.all()
        user_schema = UserSchema(many=True)
        #below is going to convert user1 object into something like mixture of python dict and list
        output = user_schema.dump(user1) # user1 will become something which can be serialized.
        # now output is serialized one 
        return jsonify(output)
    if request.method == 'POST':
        email = request.json['email']
        result = User.query.filter_by(email=email).first()
        print(result)
        if not result :
            user = User(firstname = request.json['firstname'] , lastname =request.json['lastname'] , email=request.json['email'], password=request.json['password'])
            db.session.add(user)
            db.session.commit()
            return jsonify({'result' : 'successfully created new user.'})
        else:
            return jsonify({'result' : 'user already exist.'})
    else:
        return jsonify({'result' : 'new user not created.'})


@app.route("/user/<int:id>" , methods=['GET' , 'DELETE' , 'PUT', 'PATCH'])
def user(id):
    if request.method == 'GET':
        u = User.query.get_or_404(id)
        schema = UserSchema()
        result = schema.dump(u)
        return schema.jsonify(result)
    if request.method == 'DELETE':
        u = User.query.get_or_404(id)
        db.session.delete(u)
        db.session.commit()
        return jsonify({'result' : 'user deleted successfully.'})
    if request.method == 'PUT':
        try:
            u = User.query.get_or_404(id)
            result = User.query.filter_by(email=request.json['email']).first()
            if not result :
                u.firstname = request.json['firstname']
                u.lastname = request.json['lastname']
                u.email = request.json['email']
                u.password = request.json['password']
                db.session.commit()
                return jsonify({'result' : 'user updated successfully.'})
            else:
                return jsonify({'result' : 'user email already exist.'})
        except:
            return jsonify({'result' : 'some problem occured.'})
            
    if request.method == 'PATCH':
        u = User.query.get_or_404(id)
        try:
            if request.json['firstname'] :
                u.firstname = request.json['firstname']
        except:
            pass
        
        try:
            if request.json['lastname'] :
                u.lastname = request.json['lastname']
        except:
            pass
        
        try:    
            if request.json['email'] :
                u.email = request.json['email']
        except:
            pass
        
        try:
            if request.json['password'] :
                u.password = request.json['password']
        except:
            pass
        db.session.commit()
        return jsonify({'result' : 'users partial update is successful.'})
            

if __name__ == "__main__":
    app.run(debug=True)