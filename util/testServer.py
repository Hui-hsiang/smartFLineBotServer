from flask import Flask, request, abort, render_template
from urllib.request import urlopen


posts = []
names = []

app = Flask(__name__)
@app.route("/jerrycomments", methods=['GET','POST'])
def jerrycomments():
    if request.method == 'POST':

        posts.append(request.form.get('url'))
        names.append(request.form.get('name'))

        return render_template("comments.html",title = 'apple', names = names, posts = posts)
    else:
        return render_template("comments.html",title = 'apple', names = names, posts = posts)

    

 

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)