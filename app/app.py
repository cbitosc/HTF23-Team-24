from flask import Flask,render_template,request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
import newspaper
from newspaper import Article

app = Flask(__name__)

#------------------------------To render HTML pages-----------------------------------

@app.route('/',methods=['GET','POST'])
def hello_world():
    return render_template('index.html')

@app.route('/link',methods=['GET','POST'])
def link():
    return render_template('link.html')

@app.route('/linkfind',methods=['GET','POST'])
def linkfind():
    if request.method=="POST":
        l=(request.form['link'])
        t=get_article_content(l)
        credibility_score = calculate_credibility_score(t)
    return render_template('Find.html',cs=credibility_score,te=t)

@app.route('/textfind',methods=['GET','POST'])
def textfind():
    if request.method=="POST":
        t=(request.form['textnews'])
        credibility_score = calculate_credibility_score(t)
    return render_template('Find.html',cs=credibility_score,te=t)

@app.route('/text',methods=['GET','POST'])
def text():
    return render_template('text.html')

@app.route('/notext',methods=['GET','POST'])
def notext():
    return render_template('notext.html')

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route('/help',methods=['GET','POST'])
def help():
    return render_template('help.html')

#-----------------------------------METHODS----------------------------------
def get_article_content(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def calculate_credibility_score(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    # Assuming a linear mapping from polarity to credibility score in the range [0, 1]
    credibility_score = (polarity + 1) / 2

    return credibility_score


if __name__== "__main__":
    app.run(debug=True,port="8000")