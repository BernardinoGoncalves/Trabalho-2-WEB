import requests
from flask import Flask, render_template, request, redirect


dicUsers = {}
dicUsers['bernardo@hotmail.com'] = ('Bernardino', '123', 'bernardo@hotmail.com')
listFav = ['https://myanimelist.net/anime/20/Naruto']

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():  # put application's code here
    user = request.form['user']
    password = request.form['password']
    res = dicUsers.get(user, ('null', '-1'))
    if len(res) < 2:
        return redirect('/')
    if res[2] == user and res[1] == password:
        return redirect('/home2')
        #return render_template('home.html')
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
    if len(res) > 2: #ja existe esse usuário
        return redirect('/registration')
    if password1 != password2 or name == '': #senhas não são iguais ou nome vazio
        return redirect('/registration')

    dicUsers[email] = (name, password1, email)
    return redirect('/home2')


@app.route('/home2')
def home():  # put application's code here

    try:
        text = request.args.get('search')
        text = text.lower().replace(' ', '%20')
        url = 'https://api.jikan.moe/v3/search/anime?q=' + text
        search_anime = requests.get(url).json()['results']
    except:
        search_anime = []
    return render_template('home.html', result=search_anime, fav=listFav)


if __name__ == '__main__':
    app.run()
