import base64
from datetime import datetime

import requests
from ics import Calendar, Event


def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")


def lambda_handler(event, context):
    url = "https://corsi.unibo.it/2cycle/ParticlePhysics/timetable/@@orario_reale_json?anno=2&curricula=&start=2024-09-23&end=2024-09-30"
    response = requests.get(url)
    data = response.json()

    cal = Calendar()

    for item in data:
        event = Event()
        event.name = item.get('title', 'No Title')
        event.begin = parse_date(item['start'])
        event.end = parse_date(item['end'])
        event.location = item['aule'][0]['des_ubicazione'] if item['aule'] else 'No Location'
        event.description = f"Professor: {item.get('docente', 'No Professor')}\nNotes: {item.get('note', 'No Notes')}"
        cal.events.add(event)

    # Create the ICS file content
    ics_content = cal.serialize()

    # Base64 encode the ICS content
    encoded_ics_content = base64.b64encode(ics_content.encode('utf-8')).decode('utf-8')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/calendar',
            'Content-Disposition': 'attachment; filename="timetable.ics"'
        },
        'body': encoded_ics_content,
        'isBase64Encoded': True
    }
