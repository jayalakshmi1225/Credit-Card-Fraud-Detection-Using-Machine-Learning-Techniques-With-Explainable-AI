from flask import Flask,url_for,render_template,request
import joblib
import mysql.connector,os ,re , joblib

app = Flask(__name__)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='db'
)
mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data
@app.route("/")
def index():
    return render_template('index.html') 

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        c_password = request.form['c_password']
        if password == c_password:
            query = "SELECT UPPER(email) FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])
            if email.upper() not in email_data_list:
                query = "INSERT INTO users (name,email, password) VALUES ( %s, %s, %s)"
                values = (name,email, password)
                executionquery(query, values)
                return render_template('login.html', message="Successfully Registered!")
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')

@app.route('/login',methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email.upper() in email_data_list:
            query = "SELECT UPPER(password) FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password.upper() == password__data[0][0]:
                global user_email
                user_email = email

                return render_template('home.html')
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')







@app.route('/Home')
def Home():
     return render_template('Home.html')

@app.route('/Prediction', methods = ['GET',"POST"])
def Prediction():
     if request.method == 'POST':
        category = int(request.form['category'])
        amt = (request.form['amt'])
        top_5_city = int(request.form['top_5_city'])
        gender = int(request.form['gender'])
        top_5_job = int(request.form['top_5_job'])
        top_5_in_merchant = float(request.form['top_5_in_merchant'])
        age = float(request.form['age'])
    
        lee = [[category, amt, top_5_city,gender, top_5_job, top_5_in_merchant,age]]
        print(lee)
        print(lee)
        model = joblib.load("randomforest.joblib")
        predictions = model.predict(lee)
        print(predictions)
        if predictions == 0:
            result = 'No Fraud'
            return render_template('prediction.html', result = result)
        elif predictions == 1:
            result = 'Fraud'
            return render_template('prediction.html', result = result)
     return render_template('prediction.html')
     






@app.route('/model',methods = ['GET',"POST"])
def model():
     msg = None
     accuracy = None
     if request.method == 'POST':
        algorithams = request.form["algorithm"]
        if algorithams == "1":
            accuracy = 99
            msg = 'Accuracy  for Stacking Classifier is ' + str(accuracy) + str('%')
        elif algorithams == "2":
            accuracy = 99
            msg = 'Accuracy  for RandomForestClassifier is ' + str(accuracy) + str('%')
        elif algorithams == "3":
            accuracy = 88
            msg = 'Accuracy  for Convolutional Neural Network(CNN) is ' + str(accuracy) + str('%')
        elif algorithams == "4":
            accuracy = 92
            msg = 'Accuracy  for Long Short-Term Memory(LSTM) is ' + str(accuracy) + str('%')
        return render_template('model.html',msg=msg,accuracy = accuracy)
     return render_template('model.html')

if __name__ == "__main__":
     app.run(debug=True)