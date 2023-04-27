import requests
from django.shortcuts import render

def solar_plant_form(request):
    if request.method == 'POST':
        # Get form inputs
        rooftop_area = float(request.POST.get('rooftop_area'))
        zipcode = int(request.POST.get('zipcode'))
        monthly_consumption = float(request.POST.get('monthly_consumption'))

        # Get average solar irradiance data from openweathermap API
        url = f'http://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&appid=7193fb1d13782f01dd012f3454f7f6a1razil), 
        response = requests.get(url)
        data = response.json()
        solar_irradiance = data['main']['temp']  # assuming the API returns solar irradiance in temperature field

        # Calculate required panel efficiency
        rooftop_area_m2 = rooftop_area / 10.764  # convert square feet to square meters
        required_efficiency = monthly_consumption / (solar_irradiance * rooftop_area_m2 * 30 * 24)

        # Determine suggested solar panel
        if required_efficiency > 0.20:
            panel = 'no panel possible'
        elif required_efficiency > 0.15:
            panel = 'Monocrystalline silicon solar panels'
        elif required_efficiency > 0.13:
            panel = 'Polycrystalline silicon solar panels'
        else:
            panel = 'Thin-film solar panels'

        # Render response template with suggested panel
        context = {'panel': panel}
        return render(request, 'suggestion/solar_panel.html', context)

    else:
        # Render empty form template
        return render(request, 'suggestion/solar_form.html')
