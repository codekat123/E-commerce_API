import pycountry

def get_country_choices():
    return [(country.alpha_2, country.name) for country in pycountry.countries]