from flask import Flask, render_template, request, Response
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

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", data=[{'id': '1'}])

@app.route('/get-text', methods=['GET', 'POST'])
def foo():
    i = 0
    tableCount = request.form.get('cams')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM tatcamerstats")
    
    if resultValue > 0:
        for i in range(int(tableCount)):
            camDetails = cur.fetchmany()
    return render_template("index.html", userDetails=camDetails,tableCount=tableCount)

@app.route('/get-all', methods=['GET', 'POST'])
def foo2():
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

def gen():
 

    img = cv2.imread("pic.png")
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
    frame = cv2.imencode('.png', img)[1].tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
   
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)