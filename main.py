from flask import Flask, render_template, request, Response, redirect
from flask_mysqldb import MySQL
import yaml
import cv2


app = Flask(__name__)

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor

pic = 2
n = 1
@app.route('/', methods=['GET', 'POST'])
def index():
    global n
    n = 1
    return render_template("index.html", data=[{'id': '1'}])

@app.route('/get-text', methods=['GET', 'POST'])
def foo():
    i = 0
    global n
    n = 1
    tableCount = request.form.get('cams')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM tatcamerstats")
    
    if resultValue > 0:
        for i in range(int(tableCount)):
            camDetails = cur.fetchmany()
    global pic
    pic = tableCount
    return render_template("index.html", userDetails=camDetails,tableCount=tableCount)

def gen(pic):
 
    img = cv2.imread("src/test"+str(pic)+".jpg")  # 1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    trash = cv2.CascadeClassifier('cascade/trash.xml')

    results = trash.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=17)

    for (x, y, w, h) in results:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
    frame = cv2.imencode('.jpg', img)[1].tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')

def gen2():
 
    img = cv2.imread("src/man.jpg")  # 1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    man = cv2.CascadeClassifier('cascade/body.xml')

    results = man.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    for (x, y, w, h) in results:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
    frame = cv2.imencode('.jpg', img)[1].tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')


@app.route('/get-all', methods=['GET', 'POST'])
def foo2():
    global n
    n = 1
    tableCount = request.form.get('allcams')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM tatcamerstats")
    
    if resultValue > 0:
            camDetails = cur.fetchall()
    return render_template("index.html", userDetails=camDetails,tableCount=tableCount)


@app.route('/get-rating', methods=['GET', 'POST'])
def foo3():
    tableCount = request.form.get('ratings')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT rating.service, rating.area, A.Count FROM rating LEFT JOIN (SELECT *, COUNT(trashfull) AS Count FROM tatcamerstats WHERE trashfull = 'YES' GROUP BY street) AS A ON A.street = rating.area ORDER BY A.Count ASC;")
    if resultValue > 0:
            statDetails = cur.fetchall()
    return render_template("index.html",ratingDetails=statDetails,tableCount=tableCount)

@app.route('/get-man', methods=['GET', 'POST'])
def nfunc():
    global n
    n += 1
    return  render_template("index.html")
        
@app.route('/video_feed')
    
def video_feed():
    global n
    if n==1:
        return Response(gen(pic),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    elif n==2:
         return Response(gen2(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug=True)