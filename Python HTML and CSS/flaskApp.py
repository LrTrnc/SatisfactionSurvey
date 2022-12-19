from flask import Flask, render_template
#import os

app = Flask(__name__, template_folder='templates')


@app.route('/' )
def home():
   return render_template('index.html')

@app.route("/All/Yearly")
def Display_IMG1():
    return render_template("All365DaysPie.html", user_image="All365DaysPie.png")

@app.route("/SH-A2.09/Yearly")
def Display_IMG2():
  return render_template("SH-A2.09-365DaysPie.html", user_image="SH-A2.09-365DaysPie.png")

@app.route("/All/Daily/Days:30")
def Display_IMG3():
  return render_template("AllLine30Days.html", user_image="AllLine30Days.png")

@app.route("/SH-A2.09/Daily/Days:30")
def Display_IMG4():
  return render_template("SH-A2.09-Line30Days.html", user_image="SH-A2.09-Line30Days.png")

@app.route('/about')
def about():
  return render_template("about.html", user_image="lara.png")


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True,use_reloader=True)
