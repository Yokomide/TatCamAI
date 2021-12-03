from flask import Flask, render_template, request, Response
from flask_mysqldb import MySQL
import yaml
import numpy as np
import cv2
import tensorflow as tf


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
    """
    if request.method == 'POST':
        userDetails = request.form
        position = userDetails['position']
        trashfull = userDetails['trashfull']
        folder_id = userDetails['folder_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tatcamerstats(position, trashfull, folder_id) VALUES(%s, %s, %s)",(position, trashfull, folder_id))
        mysql.connection.commit()
        cur.close()
        """
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

#Тестовый, простенький ИИ по отслеживанию движения с видео и выводом на сайт.

def gen():

    cap = cv2.VideoCapture("1.avi")

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret: 
            frame = cv2.VideoCapture("1.avi")
            continue
        if ret: 
            image = cv2.resize(frame, (0, 0), None, 1, 1) 
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
            fgmask = sub.apply(gray)  
            
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) 
            closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
            opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
            dilation = cv2.dilate(opening, kernel)
            retvalbin, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)  
            contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            minarea = 400
            maxarea = 50000
            for i in range(len(contours)):  
                if hierarchy[0, i, 3] == -1: 
                    area = cv2.contourArea(contours[i])  
                    if minarea < area < maxarea:
                        cnt = contours[i]
                        M = cv2.moments(cnt)
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(image, str(cx) + "," + str(cy), (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX,.3, (0, 0, 255), 1)
                        cv2.drawMarker(image, (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, markerSize=8, thickness=3,line_type=cv2.LINE_8)

        frame = cv2.imencode('.jpg', image)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20)
        if key == 27:
           break
   
        

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)