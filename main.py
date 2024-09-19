# %%
from datetime import datetime

import requests
from ics import Calendar, Event

# Fetch JSON data from the URL
# url = "https://corsi.unibo.it/2cycle/ParticlePhysics/timetable/@@orario_reale_json?anno=2&curricula=&start=2024-09-23&end=2024-09-30"
# url = "https://corsi.unibo.it/2cycle/ParticlePhysics/timetable/@@orario_reale_json?anno=2"
url = "https://corsi.unibo.it/2cycle/ParticlePhysics/timetable/@@orario_reale_json?anno=2&curricula=&start=2024-08-01&end=2025-04-01"
response = requests.get(url)
data = response.json()
data

# %%
len(data)

# %%
[d['start'] for d in data]

# %%
# Create a new calendar
cal = Calendar()


# Define a function to convert date strings to datetime objects
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")


# Extract event details and create events
for item in data:
    event = Event()
    event.name = item.get('title', 'No Title')
    event.begin = parse_date(item['start'])
    event.end = parse_date(item['end'])
    event.location = item['aule'][0]['des_ubicazione'] if item['aule'] else 'No Location'
    event.description = f"Professor: {item.get('docente', 'No Professor')}\nNotes: {item.get('note', 'No Notes')}"
    cal.events.add(event)

# Save the calendar to an ICS file
with open('timetable.ics', 'w') as f:
    f.writelines(cal)

print("ICS file generated successfully.")
