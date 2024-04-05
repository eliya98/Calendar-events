import csv
from icalendar import Calendar, Event
from datetime import datetime

# Dictionary mapping month names to their numeric representation
month_mapping = {
    'january ': '01', 'february': '02', 'march': '03',
    'april': '04', 'may ': '05', 'june': '06',
    'july': '07', 'august': '08', 'september': '09',
    'october': '10', 'november': '11', 'december ': '12'
}

def csv_to_ics(csv_file, ics_file):
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        cal = Calendar()

        for row in csvreader:
            event = Event()

            # Convert spelled-out month to its numeric representation
            month = row['MONTH'].lower()
            month_number = month_mapping.get(month)
            if month_number is None:
                raise ValueError(f"Invalid month name: {row['MONTH']}")

            # Combine month number, day, and year to form the event date
            event_date = f"{month_number} {row['Day ']}, {row['Year ']}"
            event_start = datetime.strptime(event_date, '%m %d, %Y')

            # Set event start date
            event.add('dtstart', event_start)
            
            # Set event end date (Assuming the event lasts for one day)
            event.add('dtend', event_start)
            
            # Set event summary (EVENTTYPE + First Name + Last Name)
            summary = f"{row['First_name ']} {row['Last_name ']}'s {row['EVENT_type']}"
            event.add('summary', summary)
            
            # Add RRULE for yearly recurrence
            event.add('rrule', {'freq': YEARLY})
            cal.add_component(event)
            
            # Set event location (if available)
            if 'Column2' in row:
                event.add('location', row['Column2'])
            cal.add_component(event)

    with open(ics_file, 'wb') as f:
        f.write(cal.to_ical())

csv_to_ics('events.csv', 'calendar.ics')

