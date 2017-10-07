import re
import os
from flask import *
import pdfkit
from flask_sqlalchemy import *
from flask_restless import *
from flask_cors import CORS
from config import Config

app=Flask(__name__)
CORS(app, resources={
    r"/api/*": {
            "origins": "*",
            "methods": "GET, HEAD, POST, OPTIONS, PUT, PATCH, DELETE",
            "allow_headers": "*"
        }
    })
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    firstname = db.Column("firstname",db.String(50))
    lastname = db.Column("lastname",db.String(50))
    gender = db.Column("gender",db.String(50))
    email = db.Column("email",db.String(120), unique=True, nullable=False)
    age = db.Column("age",db.String(50))
    contact = db.Column("contact",db.String(50))
    region = db.Column("region",db.String(50))
    city = db.Column("city",db.String(50))
    donorweight = db.Column("donorweight",db.String(50))
    haemoglobin = db.Column("haemoglobin",db.String(50))
    blood = db.Column("blood",db.String(50))
    decision = db.Column("decision",db.String(50))

    def __init__(self, firstname, lastname, gender,
                 email,age,contact,region,city,donorweight,
                 haemoglobin,blood,decision):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.email = email
        self.age = age
        self.contact = contact
        self.region = region
        self.city = city
        self.donorweight = donorweight
        self.haemoglobin = haemoglobin
        self.blood = blood
        self.decision = decision
    
class Admin(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    email = db.Column("email",db.String(120), unique=True, nullable=False)
    password = db.Column("password",db.String(50))

    def __init__(self, email, password):
        self.email = email
        self.password = password
    

db.create_all()
manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Admin, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route("/posa", methods=['POST'])
def posa():
    try:
        auser=request.form['auser']
        apwd=request.form['apwd']
        admin=Admin(auser,apwd)
        db.session.add(admin)
        db.session.commit()
        return redirect('/adminp')
    except:
        print('error')

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/questions")
def questions():
    return render_template("questionnaire.html")

@app.route("/q", methods=['POST', 'GET'])
def q():
        
    try:
        a1      =   request.form['1']
        a2      =   request.form['2']
        a3      =   request.form['3']
        print(a1,a2,a3)
        
        if a1 == 'yes':
                
                return redirect('/questions')
        elif a2 == 'yes':
                
                return redirect('/questions')
        elif a3 == 'yes':
                
                return redirect('/questions')
     
        else:
                return redirect('/r1')
        
    except:
        return redirect('/questions')


@app.route("/r1")
def r1():
    return render_template('q1.html')

@app.route("/q1", methods=['POST', 'GET'])
def q1():
        
  try:     
        a4      =   request.form['4']
        a5      =   request.form['5']
        a6      =   request.form['6']


        if a4 == "no":
                return redirect('/r1')
        elif a5 == "yes":
                return redirect('/r1')
        elif a6 == "yes":
                return redirect('/r1')
     
        else:
                return redirect('/r2')
  except:
      return redirect('/r1')

    
@app.route("/r2")
def r2():
    return render_template('q2.html')

@app.route("/q2", methods=['POST', 'GET'])
def q2():

    try:
        a7      =   request.form['7']
        a8      =   request.form['8']
        a9      =   request.form['9']

        if request.method == 'POST':

            if a7 == "yes":
                
                return redirect('/r2')
            elif a8 == "yes":
                return redirect('/r2')
     
            else:
                return redirect('/r3')

    except:
       
       return redirect('/r2')

    

@app.route("/r3")
def r3():
    return render_template('q3.html')


@app.route("/q3", methods=['POST', 'GET'])
def q3():

    
    try:   
        fname   =   session['fn']
        lname    =   session['ln']
        gender  =   session['gender']
        email   =   session['email']
        age     =   session['age']
        cn      =   session['cn']
        region  =   session['region']
        city    =   session['cities']
         
        add = User(fname,lname,gender,email,age,cn,region,city, "", "", "","")
        db.session.add(add)
        db.session.commit()
        print('You were successfully registered')
        return redirect('/')
    except:
        return redirect('/r3')
    


@app.route("/answers", methods=['POST', 'GET'])
def answers():
    session['fn'] = request.form.get('fn')
    session['ln'] = request.form.get('ln')
    session['gender'] = request.form.get('gender')
    session['email'] = request.form.get('email')
    session['age'] = request.form.get('age')                            
    session['cn'] = request.form.get('cn')
    session['region'] = request.form.get('region')
    session['cities'] = request.form.get('cities')
    
    return redirect('/questions')


@app.route("/adminp")
def adminp():


    data = User.query.all()
    idds=[]
    for x in data:
        idds.append(x.id)
    

    ids=[]
    for x in data:
        ids.append(x.id)

    fns=[]
    for x in data:
        fns.append(x.firstname)
        
    lns=[]
    for x in data:
        lns.append(x.lastname)

    gens=[]
    for x in data:
        gens.append(x.gender)

    ages=[]
    for x in data:
        ages.append(x.age)

    bloods=[]
    for x in data:
        bloods.append(x.blood)

    decs=[]
    for x in data:
        decs.append(x.decision)

    return render_template("admin.html", posts=zip(idds,ids,fns,lns,gens,ages,bloods,decs))


@app.route("/admin", methods=['POST'])
def admin():
        error=None
        if request.method == 'POST' :
            auser = request.form.get('auser')
        
            apwd  = request.form.get('apwd')

            all = Admin.query.all()
            email=[]
            for x in all:
                email.append(x.email)
            if(auser in email):
                data=Admin.query.filter_by(email=auser).first()

                print(auser,apwd)
                if (data.password == apwd):
                    flash('You were successfully logged in')
                    return redirect('adminp')
                else:
                    error = 'Invalid password'
                    return render_template('home.html', error=error)
            else:
                error = "No account for that email/username"
                return render_template('home.html',error=error)


@app.route("/decision", methods=["POST"])
def decision():
    
        session['x'] = request.form['x']
        print(session['x'])
        ex = User.query.filter_by(id=session['x']).first()
        fns=[]
        fns.append(ex.firstname)
        
        return render_template("questionnaire 1.html", posts=fns)


@app.route("/decisions", methods=['POST', 'GET'])
def decisions():

        
        ids = session['x']
        weight = request.form.get('dw')
        blood = request.form.get('blood')
        type = request.form.get('bloodgroup')
        deci = request.form.get('decision')

        ex = User.query.filter_by(id=ids).first()
        ex.donorweight = weight
        ex.haemoglobin = blood
        ex.blood= type
        ex.decision=deci
        
        db.session.commit()

        deci = User.query.filter_by(id=ids).first()
        decs=[]
        decs.append(deci.decision)

        if (decs[0] == 'accepted'):

             return redirect('/cert/{}'.format(ids))
            
        else:

            return redirect("/adminp")


@app.route("/delete", methods=["POST"])
def delete():
    ids = request.form['x']

    delete = User.query.filter_by(id=ids).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect('/adminp')





@app.route("/certi")
def certi():
    
    return render_template('cert.html')


@app.route("/cert/<ids>")
def cert(ids):


    data = User.query.filter_by(id=ids).first()
    fns=[]
    fns.append(data.firstname)
        
    lns=[]

    lns.append(data.lastname)
    
    rendered = render_template('cert.html',posts=zip(fns,lns))
    config= pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    options = {
    'page-size': 'Letter',
    'orientation': 'landscape',
    'encoding': 'UTF-8',
    'margin-left': '0.1cm',
    'margin-right': '0.1cm',
    'margin-top': '0.1cm',
    'margin-bottom': '0.1cm',
    }
    pdf = pdfkit.from_string(rendered, False,configuration=config, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response



if __name__ == "__main__":
    app.run(port=5495)












































