#!/usr/bin/env python

from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
        loader = FileSystemLoader('templates'),
        autoescape = select_autoescape(['html', 'css'])
        )

app = Flask(__name__)

@app.route('/')
def auth():
    return render_template('auth.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
