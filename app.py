from flask import Flask,  render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/data.db"
db = SQLAlchemy(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

data = {
    'iot': [
        {
            'avatar': 'girls1.jpg',
            'name': 'Maria',
            'interacao': '100',
            'email': 'maria@gmail.com'
        },
        {
            'avatar': 'girl11.jpg',
            'name': 'Joana',
            'interacao': '120',
            'email': 'joana@gmail.com'
        },
        {
            'avatar': 'girl10.jpg',
            'name': 'Julia',
            'interacao': '120',
            'email': 'juli@gmail.com'
        },
        {
            'avatar': 'girl14.png',
            'name': 'Patricia',
            'interacao': '100',
            'email': 'pa@gmail.com'
        },
        {
            'avatar': 'girl15.png',
            'name': 'Ana',
            'interacao': '120',
            'email': 'ana@gmail.com'
        },
        {
            'avatar': 'girl16.jpg',
            'name': 'Paula',
            'interacao': '120',
            'email': 'pa@gmail.com'
        },
    ],
    'web': [
        {
            'avatar': 'girls4.jpg',
            'name': 'Roberta',
            'interacao': '300',
            'email': 'roberta@gmail.com'
        },
        {
            'avatar': 'girl5.jpg',
            'name': 'Vanessa',
            'interacao': '315',
            'email': 'vanessa@gmail.com'
        },
        {
            'avatar': 'girl12.jpg',
            'name': 'Fernanda',
            'interacao': '315',
            'email': 'nanda@gmail.com'
        },
        {
            'avatar': 'girl17.png',
            'name': 'Rubia',
            'interacao': '300',
            'email': 'ru@gmail.com'
        },
        {
            'avatar': 'girl18.jpg',
            'name': 'Valeria',
            'interacao': '315',
            'email': 'va@gmail.com'
        },
        {
            'avatar': 'girl25.png',
            'name': 'Fatima',
            'interacao': '315',
            'email': 'fa@gmail.com'
        },

    ],
    'datascience': [
        {
            'avatar': 'girl7.jpg',
            'name': 'Nina',
            'interacao': '215',
            'email': 'nina@gmail.com'
        },
        {
            'avatar': 'girl8.jpg',
            'name': 'Marcia',
            'interacao': '400',
            'email': 'vanessa@gmail.com'
        },
        {
            'avatar': 'girl9.jpg',
            'name': 'Camila',
            'interacao': '400',
            'email': 'cami@gmail.com'
        },
        {
            'avatar': 'girl20.jpg',
            'name': 'Manu',
            'interacao': '37',
            'email': 'manu@gmail.com'
        },
        {
            'avatar': 'girl22.jpg',
            'name': 'Leticia',
            'interacao': '250',
            'email': 'le@gmail.com'
        },
        {
            'avatar': 'girl23.jpg',
            'name': 'Sandra',
            'interacao': '400',
            'email': 'san@gmail.com'
        },
    ]
}


class Girl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    id_tele = db.Column(db.String)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "id_tele": self.id_tele,
        }


class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pergunta = db.Column(db.String)
    tech = db.Column(db.String)
    status = db.Column(db.Boolean)
    id_girl = db.Column(db.Integer, ForeignKey('girl.id'))
    girl = relationship('Girl')

    def json(self):
        return {
            "id": self.id,
            "pergunta": self.pergunta,
            "tech": self.tech,
            "status": self.status,
            "id_girl": self.id_girl
        }


class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    id_tele = db.Column(db.String)
    tech = db.Column(db.String)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "id_tele": self.id_tele,
            "tech": self.tech
        }


class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String)
    id_mentor = db.Column(db.String)

    def json(self):
        return {
            "id": self.id,
            "texto": self.texto,
            "id_mentor": self.id_mentor
        }


class Pergunta_Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_pergunta = db.Column(db.Integer, ForeignKey('pergunta.id'))
    resposta_mentor = db.Column(db.Integer, ForeignKey('resposta.texto'))
    pergunta = relationship('Pergunta')
    resposta = relationship('Resposta')

    def json(self):
        return {
            "id": self.id,
            "id_pergunta": self.id_pergunta,
            "resposta_mentor": self.resposta_mentor
        }


@ app.route('/')
def home():
    return render_template('index.html')


@ app.route('/recrutar')
def recrutar(tech):
    return render_template('girls-list.html')


@ app.route('/recrutar/<tech>')
def recrutar_tech(tech):
    girls = []
    if (tech == 'todas'):
        for tech in data:
            girls.extend(data[tech])
        print(girls)
    else:
        girls = data[tech]
    return render_template('girls-list.html', girls=girls)


@ app.route('/profissional')
def profissional():
    return render_template('telegram-redirect.html')


@ app.route('/mentor')
def mentor():
    return render_template('mentor.html')


@ cross_origin()
@ app.route('/girl', methods=['POST'])
def girl():
    req = request.get_json()
    print(req)
    girl = Girl(name=req['name'], email=req['email'], id_tele=req['id_tele'])
    db.session.add(girl)
    db.session.commit()
    return "OK", 201


@ app.route('/pergunta', methods=['POST'])
def pergunta():
    req = request.get_json()
    print(req)
    pergunta = Pergunta(
        pergunta=req['pergunta'], tech=req['tech'], id_girl=req['id_girl'], status=True)
    db.session.add(pergunta)
    db.session.commit()
    return jsonify(pergunta.json()), 201


@ app.route('/mentor', methods=['POST'])
def mentor_tech():
    req = request.get_json()
    print(req)
    mentor = Mentor(name=req['name'],
                    email=req['email'], id_tele=req['id_tele'], tech=req['tech'])
    db.session.add(mentor)
    db.session.commit()
    return "OK", 201


@ app.route('/resposta', methods=['POST'])
def resposta():
    req = request.get_json()
    print(req)
    resposta = Resposta(texto=req['texto'], id_mentor=req['id_mentor'])

    db.session.add(resposta)
    db.session.commit()
    return "OK", 201


@ app.route('/find_mentors', methods=['POST'])
def find_mentors():

    req = request.get_json()

    foundedTupleMentorsIds = db.session.query(
        Mentor).filter(Mentor.tech == req['tech']).all()

    foundedListMentorsIds = list(
        map(lambda x: x.id_tele, foundedTupleMentorsIds))

    return jsonify({"foundedMentorsIds": foundedListMentorsIds})


@ app.route('/pergresp', methods=['POST'])
def pergresp():
    req = request.get_json()
    print(req)
    pergresp = Pergunta_Resposta()
    db.session.add(pergresp)
    db.session.commit()
    return "OK", 201


@ app.route('/pergresp')
def get_pergresp():
    req = request.get_json()
    print(req)
    tasks = [u.json() for u in db.session.query(Pergunta_Resposta).all()]
    return jsonify(tasks)
    return "OK", 201


if __name__ == "__main__":
    app.run()
