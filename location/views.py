from django.shortcuts import render
from .models import IDtoUser, NumberofEvents
from django.core.mail import send_mail
import requests

# Create your views here.
def index(request):
	
    Employee = IDtoUser.objects.all()
    url = 'https://api.radar.io/v1/users/{}'

    privatekey = {
    'Authorization': 'prj_live_sk_5bff60481af1adf8a3793ce4b3a12f48e3f424de',
    }
    event_details = requests.get('https://api.radar.io/v1/events', headers=privatekey).json()
    lengthofEvents = len(event_details['events'])
    ID_DICT = {IDtoUser.objects.get(id=1).ID_Device:IDtoUser.objects.get(id=1).name , 
        IDtoUser.objects.get(id=2).ID_Device:IDtoUser.objects.get(id=2).name,
        IDtoUser.objects.get(id=3).ID_Device:IDtoUser.objects.get(id=3).name,
        IDtoUser.objects.get(id=4).ID_Device:IDtoUser.objects.get(id=4).name,
        IDtoUser.objects.get(id=5).ID_Device:IDtoUser.objects.get(id=5).name,
        IDtoUser.objects.get(id=6).ID_Device:IDtoUser.objects.get(id=6).name,}
    ExitandEnter = {'user.exited_geofence': 'exited', 'user.entered_geofence': 'entered'}

    if (lengthofEvents > NumberofEvents.objects.get(id=1).number):

    	t = NumberofEvents.objects.get(id=1)
    	difference = lengthofEvents - t.number
    	t.number = lengthofEvents
    	t.save()
    	for i in range(difference):
    		send_mail(ID_DICT.get(event_details['events'][i]['user']['_id']), ID_DICT.get(event_details['events'][i]['user']['_id'])+ ' ' + ExitandEnter.get(event_details['events'][i]['type']) + ' ' + event_details['events'][i]['geofence']['description'],'anupriyamranjit8@gmail.com',['nafap19986@topmail1.net'],fail_silently=False)
    else:
    	pass

    employeelocation = []
    for person in Employee:
        employee_location = requests.get(url.format(person.ID_Device), headers=privatekey).json()
        try:
            Location_Value = (employee_location['user']['geofences'])[0]['description']
        except IndexError:
            Location_Value = 'Unknown'

        employee = {
            'Name': person.name,
            'Employee_Location': Location_Value,
            'Accuracy': employee_location['user']['locationAccuracy'],
            'Last_Update': employee_location['user']['actualUpdatedAt'],
            'Coordinate' : [round(employee_location['user']['location']['coordinates'][0], 5),round(employee_location['user']['location']['coordinates'][1], 5)],
            'TypeofPhone' : employee_location['user']['deviceType'],
            }
        employeelocation.append(employee)
    context = {'employeelocation' : employeelocation }
    
    return render(request, 'location/index.html', context)