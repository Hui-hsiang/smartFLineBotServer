from flask import Flask, request, abort, render_template
from urllib.request import urlopen


app = Flask(__name__)
@app.route("/taipei", methods=['GET'])
def lineFriends():
    return render_template("lineFriends.html")

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)