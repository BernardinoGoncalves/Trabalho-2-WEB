import json

import requests
from flask import Flask, render_template, request, redirect

dicUsers = {}
dicUsers['bernardo@hotmail.com'] = ('Bernardino', '123', 'bernardo@hotmail.com')
listFav = {}

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():  # put application's code here
    user = request.form['user']
    password = request.form['password']
    res = dicUsers.get(user, ('null', '-1'))
    if len(res) <= 2:
        return redirect('/')
    if res[2] == user and res[1] == password:
        return redirect('/home')
    return redirect('/')


@app.route('/registration')
def registration():  # put application's code here
    return render_template('cadastro.html')


@app.route('/registration', methods=['POST'])
def register():  # put application's code here
    email = request.form['email']
    name = request.form['name']
    password1 = request.form['password1']
    password2 = request.form['password2']

    res = dicUsers.get(email, ('null', '-1'))
    if len(res) > 2:  # ja existe esse usuário
        return redirect('/registration')
    if password1 != password2 or name == '':  # senhas não são iguais ou nome vazio
        return redirect('/registration')

    dicUsers[email] = (name, password1, email)
    return redirect('/home')


@app.route('/home')
def home():  # put application's code here
    search_anime = []
    try:
        text = request.args.get('search')
        text = text.lower().replace(' ', '%20')
        url = 'https://api.jikan.moe/v3/search/anime?q=' + text
        search = requests.get(url).json()['results']
        for s in search:
            if s['type'] == 'TV' or s['type'] == 'anime':
                search_anime.append(s)
    except:
        search_anime = []
    return render_template('home.html', result=search_anime, favorito=listFav)


@app.route('/anime')
def anime():  # put application's code here
    ep = request.args.get('anime')
    url = 'https://api.jikan.moe/v3/anime/' + ep
    anime = requests.get(url).json()
    image = anime['image_url']
    title = anime['title']
    synopsis = anime['synopsis']
    url = url + '/episodes'
    eps = requests.get(url).json()['episodes']
    print(anime)
    return render_template('animes.html', image=image, title=title, synopsis=synopsis, eps=eps)


@app.route('/fav', methods=['POST'])
def fav():
    j = request.data
    favorite = json.loads(j)
    if not listFav.__contains__(int(favorite['id'])):
        listFav[int(favorite['id'])] = favorite
    else:
        listFav.pop(int(favorite['id']))
    return '200'


if __name__ == '__main__':
    app.run()
