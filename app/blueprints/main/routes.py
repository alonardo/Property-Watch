from flask import render_template, request, flash
import requests
from flask_login import login_required, current_user
from . import bp as main
from .forms import PropertyForm
from ...models import  Property


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/property', methods=['GET', 'POST'])
@login_required
def property_search():
    form = PropertyForm()
    if request.method == 'POST': 
        address = request.form.get('address')
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
        
        if new_property in current_user.property.all():
            flash('This property is already in your watchlist!', 'warning')
            return render_template('property.html.j2')

        current_user.property.append(new_property)
        current_user.save()
        new_property.save_propety()
        flash('Added to watchlist!', 'success')

        return render_template('property_added.html.j2', property=property_data)
    else:
        return render_template('property.html.j2')


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
        return render_template('property_watchlist.html.j2', current_user=current_user, property_counter=property_counter)
        
@main.route("/remove")
@login_required
def remove():
    pass

@main.route("/refresh", methods=['GET', 'POST'])
@login_required
def refresh():
    pass

    
    
