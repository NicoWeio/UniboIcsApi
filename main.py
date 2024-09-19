from datetime import datetime

import arrow
import requests
from ics import Calendar, Event, Organizer

URL = "https://corsi.unibo.it/2cycle/ParticlePhysics/timetable/@@orario_reale_json?anno=2"


def parse_date(date_str) -> arrow.Arrow:
    # return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    #
    # unaware_datetime = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    # rome_tz = ZoneInfo('Europe/Rome')
    # aware_datetime = unaware_datetime.replace(tzinfo=rome_tz)
    # return aware_datetime
    #
    # NOTE: We use Arrow so that our ICS library actually cares about the timezone
    arrow_date = arrow.get(date_str, tzinfo='Europe/Rome')
    return arrow_date.to('Europe/Rome')
    # return arrow.get(date_str).to('Europe/Rome').datetime


def get_cal():
    response = requests.get(URL)
    data = response.json()

    cal = Calendar(creator="Nicolai Weitkemper, with Unibo data")

    for item in data:
        event = Event()
        event.created = datetime.now()  # best thing I can do with a stateless function
        # event.last_modified = datetime.now()  # best thing I can do with a stateless function
        event.name = item.get('title', 'No Title')
        event.begin = parse_date(item['start'])
        event.end = parse_date(item['end'])
        aula = item['aule'][0]  # assuming there is always at least one aula
        # event.location = item['aule'][0]['des_ubicazione'] if item['aule'] else 'No Location'
        event.location = aula['des_risorsa'] + ", " + aula['des_indirizzo']
        event.description = f"Professor: {item.get('docente', 'No Professor')}\nNotes: {item.get('note', 'No Notes')}"
        if 'docente' in item:
            assert isinstance(item['docente'], str)
            email_guess = item['docente'].replace(' ', '.').lower() + '@unibo.it'  # TODO: risky
            event.organizer = Organizer(
                email=email_guess,
                common_name=item.get('docente')
            )
        if item.get('teams'):
            assert isinstance(item['teams'], str)
            event.url = item['teams']
        cal.events.add(event)

    return cal


if __name__ == '__main__':
    cal = get_cal()

    # Create the ICS file content
    ics_content = cal.serialize()

    # Save the calendar to an ICS file
    with open('timetable.ics', 'w') as f:
        f.writelines(ics_content)

    print("ICS file generated successfully.")
