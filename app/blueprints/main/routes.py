from calendar import c
from hashlib import new
from flask import render_template, request, redirect, url_for, flash
import requests
from flask_login import login_user, login_required, logout_user, current_user
from app.blueprints.auth.forms import EditProfileForm, LoginForm, RegisterForm
from . import bp as main
from .forms import PokemonForm, PropertyForm
from ...models import Pokemon, Property
import time
import json

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/property', methods=['GET', 'POST'])
@login_required
def property_search():
    form = PropertyForm()
    if request.method == 'POST': 
        print('code is here')
        address = request.form.get('address')
        # time.sleep(2)
        print('address below')
        print(address)
        url = "https://zillow56.p.rapidapi.com/search"

        querystring = {"location":f"{address}"}

        headers = {
            "X-RapidAPI-Key": "c95c3d4444msh7459b33ab45edc5p1b6fc1jsn10ec7672af71",
            "X-RapidAPI-Host": "zillow56.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        property_data = {
            'home_address': data['address']['streetAddress'],
            'city': data['address']['city'],
            'state': data['address']['state'],
            'price': data['price'],
            'market_status': data['homeStatus'],
            'agent_name': data['attributionInfo']['agentName'],
            'agent_phone': data['attributionInfo']['agentPhoneNumber'],
            'agent_email': data['attributionInfo']['agentEmail'],
            'days_on_zillow': data['daysOnZillow'],
            'photo': data['hiResImageLink']
        }
        
        new_property = Property()
        new_property.from_dict(property_data)
        new_property.save_propety()

        current_user.property.append(new_property)
        current_user.save()
        new_property.save_propety()
        flash('Added to watchlist!', 'success')

        return render_template('property.html.j2', property=property_data)
    else:
        return render_template('property.html.j2')


@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST': 
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}/'
        response = requests.get(url)
        if not response.ok:
            error_string = "Invalid selection, try again."
            return render_template('pokemon.html.j2', error=error_string, form=form)
        
        data = response.json()
        poke_dict={
            "name": data['name'].title(),
            "ability":data['abilities'][0]["ability"]["name"].title(),
            "base_experience":data['base_experience'],
            "attack_base_stat": data['stats'][1]['base_stat'],
            "hp_base_stat":data['stats'][0]['base_stat'],
            "defense_stat":data['stats'][2]["base_stat"],
            "photo":data['sprites']['other']['home']["front_default"]
        }
        
        return render_template('pokemon.html.j2', pokemon=poke_dict)
        
    else:
        error = 'error'
        return render_template('pokemon.html.j2', poke=error)

@main.route('/catch_pokemon', methods=['GET', 'POST'])
@login_required
def catch_pokemon():
    form = PokemonForm()
    if request.method == 'POST':
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}/'
        response = requests.get(url)
        if not response.ok:
            error_string = "Invalid selection, try again."
            return render_template('pokemon.html.j2', error=error_string)
        
        data = response.json()
        poke_dict={
            "name": data['name'].lower(),
            "ability":data['abilities'][0]["ability"]["name"].lower(),
            "base_experience":data['base_experience'],
            "attack_base_stat": data['stats'][1]['base_stat'],
            "hp_base_stat":data['stats'][0]['base_stat'],
            "defense_stat":data['stats'][2]["base_stat"],
            "photo":data['sprites']['other']['home']["front_default"],
            "user_id": current_user.id
        }
        
        new_pokemon = Pokemon()
        new_pokemon.from_dict(poke_dict)
        new_pokemon.save_poke()

        poke2 = Pokemon.query.filter_by(name=name.lower()).first()
        if len(current_user.pokemon.all()) == 5:
            print('You already have 5 Pokemon. Release one before cathing more!')
            flash('You already have 5 Pokemon. Release one before cathing more!', 'warning')
            return render_template('search.html.j2', pokemon=poke_dict)
        else:
            current_user.pokemon.append(poke2)
            current_user.save()
            poke2.save_poke()
            flash(f'You caught {poke2.name.title()}!', 'success')
        
        return render_template('search.html.j2', pokemon=poke_dict)

    else:
        error = 'error'
        return render_template('search.html.j2', poke=error)


@main.route("/view_props")
@login_required
def view_props():
    
    if len(current_user.property.all()) == 0:
        flash("You don't have any properties in your watchlist!", "danger")
        error = 'error'
        return render_template('property.html.j2', error=error)
    else:
        for property in current_user.property.all():
            print(property.home_address)
        property_counter = 0
        flash("Here are all the properties on your watchlist!", "success")
        return render_template('view_pokemon.html.j2', current_user=current_user, property_counter=property_counter)
        
@main.route("/release")
@login_required
def release():
    name = current_user.query.get('property.id')
    if current_user.property.delete(name):
        print('success')
    return render_template('release.html.j2')



# method sqlalchemy.orm.Query.delet
# https://docs.sqlalchemy.org/en/14/orm/query.html
