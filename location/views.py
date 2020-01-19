from django.shortcuts import render
from .models import IDtoUser
import requests
# Create your views here.
def index(request):
	Employee = IDtoUser.objects.all()

	privatekey = {
    'Authorization': 'prj_live_sk_5bff60481af1adf8a3793ce4b3a12f48e3f424de',
}

	employee_location = requests.get('https://api.radar.io/v1/users/5e236e8ca4f676009627bec8', headers=privatekey).json()
	employeelocation = []
	for person in Employee:
		employee = {
		'Name': Employee[0].name,
		'Employee_Location': (employee_location['user']['geofences'])[0]['description'],
		'Accuracy': employee_location['user']['locationAccuracy'],
		'Last_Update': employee_location['user']['actualUpdatedAt']
		}

	return render(request, 'location/index.html', employee)

