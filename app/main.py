#!/usr/bin/python3

from flask import render_template,request
import connexion
import sys
sys.path.append('library')
sys.path.append('controller')
sys.path.append('model')

app = connexion.App(__name__,specification_dir='./')
app.add_api('swagger.yml')

@app.route('/')
def home():
    return render_template('../templates/main.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)


