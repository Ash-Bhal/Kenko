from flask import Flask, render_template, request, jsonify, redirect, url_for
#import pyrebase
from textblob import TextBlob
scorelist = []
scorelistfinal = []
ratinglist = []
import nltk
count = 0 
from newspaper import Article

import uuid
import requests
import datetime
from werkzeug.utils import secure_filename
import os
# from optical import Transcriber
import pytesseract
from PIL import Image

app = Flask(__name__)

entrieslist = []
timelist = []
#APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#UPLOAD_FOLD = 'uploads'
#UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER







@app.route('/')
def patient_splash():

    return render_template("patient.html")

@app.route('/write', methods=['POST'])
def submit_journal_entry():
    if request.method == 'POST' and 'entry' in request.form:
        
        entry = request.form['entry']
        obj = TextBlob(entry)
        rating = obj.sentiment.polarity
        rating = str(round(rating,2))
        ratinglist.append(float(rating))
        time =str(datetime.datetime.now())
        timelist.append(time)
        entrieslist.append(entry)
        print(entrieslist)
        
        

            
            #date = str(datetime.datetime.now())
        data = {
                "date": str(datetime.datetime.now()), 
                "content": entry, 
        #        "score": rating
                    }
            #DB_REF.push(data)
    return redirect((url_for('my_journal', entrieslist = entrieslist, timelist=timelist, ratinglist=ratinglist)))
    return redirect((url_for('doctor_splash', entrieslist = entrieslist, timelist=timelist, ratinglist = ratinglist)))
    
    
    


@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files['file']
        #path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        #f.save(path)
        # pil_images = Transcriber.pdftopil(path)
        # text = Transcriber.image_to_text(pil_images)
        #text = pytesseract.image_to_string(Image.open(path))
        #rating = score(text)
        #rating = 10
        obj = TextBlob(f)
        rating = obj.sentiment.polarity
        data = {
                "date": str(datetime.datetime.now()), 
                "content": text, 
                "score": rating
                }
        #DB_REF.push(data)    
    return redirect((url_for('patient_splash')))

@app.route('/journal')
def my_journal():
    #entries = DB_REF.get().val()
    #if entries is not None:
    entries = ['test']

        
    #    entries = [entry_tuple[1] for entry_tuple in entries.items()][::-1]
    # more sauce
    for entrynum in range(len(entrieslist)):
        journalwrite = entrieslist[entrynum]
        length = len(entrieslist)

    return render_template("journal.html", timelist=timelist, length = length, journalwrite = journalwrite, entrieslist = entrieslist, entries = entries)
    #return render_template("patient.html", entrieslist = entrieslist)

@app.route('/patients')
def patients():
    return render_template("patients.html")

@app.route('/patients/1')
def doctor_splash(): 
    entries = ["Test"]
    scoreddd = 10
    if scoreddd == 10:
        score_type_dist = [{"type":"Concern","count":0}, {"type":"Moderate","count":0}, {"type":"Good","count":0}]
        score_avg = 5
            #score_type_dist = [-8,-7,7]
        scores_rev = [1,-0.4,3]
        time =str(datetime.datetime.now())
        timelist.append(time)
        length = len(entrieslist)

        score_avg = (sum(ratinglist))//(len(ratinglist))
        #scores_rev = ratinglist[::-1]
        scores_rev = ratinglist
        for score in ratinglist:
            if score < -0.2:
                score_type_dist[0]["count"] += 1
            elif score < 0.2:
                score_type_dist[1]["count"] += 1
            else:
                score_type_dist[2]["count"] += 1
    
    
    return render_template("doctor.html", ratinglist = ratinglist, timelist = timelist, length=length, entries=entries, score_avg=score_avg, score_type_dist=score_type_dist, scores_rev=scores_rev)
    
    #return render_template("doctor.html")



if __name__ == "__main__":
    app.run(debug=True)