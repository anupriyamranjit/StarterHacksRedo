from django.shortcuts import render
from .models import IDtoUser
import requests
# Create your views here.
def index(request):
    Employee = IDtoUser.objects.all()
    url = 'https://api.radar.io/v1/users/{}'

    privatekey = {
    'Authorization': 'prj_live_sk_5bff60481af1adf8a3793ce4b3a12f48e3f424de',
    }
    employeelocation = []
    for person in Employee:
        employee_location = requests.get(url.format(person), headers=privatekey).json()
        try:
            Location_Value = (employee_location['user']['geofences'])[0]['description']
        except IndexError:
            Location_Value = 'Unknown'

        employee = {
            'Name': person.name,
            'Employee_Location': Location_Value,
            'Accuracy': employee_location['user']['locationAccuracy'],
            'Last_Update': employee_location['user']['actualUpdatedAt'],
            'Coordinate' : [round(employee_location['user']['location']['coordinates'][0], 3),round(employee_location['user']['location']['coordinates'][1], 3)]
            }
        employeelocation.append(employee)
    context = {'employeelocation' : employeelocation }
    
    return render(request, 'location/index.html', context)

