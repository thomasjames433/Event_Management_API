# Event Management API
This is a project that allows Organisers to create events and  registered users to register for events. Made using Django, Django-Rest-Framework and Django-Rest-Framework-SimpleJWT
## Features:

- Does not allow organisers to perform bookings that clash with slots already taken
- Users are allowed to register and unregister for events
- User authorization using JWT
- Makes sure the number of users registered for an event does not exceed its capacity 

## Important!

Organisers are oly allowed to be created by admins

While giving an input to book a venue, follow the instructions below

'OAT', 'Auditorium', 'Aryabhatta_Hall', 'Bhaskara_Hall', 'Chanakya_Hall', 'SOMS', are the venues available

"date": "2024-12-18",  // Date in 'YYYY-MM-DD' format

"start_time": "21:30:00",  // Time in 'HH:MM:SS' format

"end_time": "22:00:00"  // Time in 'HH:MM:SS' format

The order is not important, but maintain the formats 

## Functionality/URLS

#### userregister
 POST- Creates the user, input fields are roll_no, name and password

#### login
 POST- Login user, input fields are name and password (if organiser), roll_no and password(if user), username and password if superuser
 
#### createorganiser

 POST- FOR ADMINS ONLY, input fields - name,password
  
#### api/events/create

 POST- FOR Organisers and ADMINS, input fields - title, description, date, start_time, end_time, venue, capacity, organiser, tags

#### api/events/all

 GET-For Everyone, Shows details of all events there
 
 
#### api/events/<int:id>

FOR ADMINS and the Organiser who made the booking ONLY

id - is the id of the Event 

GET- The details of the booking made

 PATCH-  input fields -  title, description, date, start_time, end_time, venue, capacity, organiser, tags

 DELETE- Delete the booking/request
 
#### api/events/register/<int:id>

POST - For Users, id= Id of Event


#### api/events/unregister/<int:id>

DELETE - For Users, id= Id of Event


## To run the library system:

#### 1. Clone the repository:
   `git clone "https://github.com/thomasjames433/Hall_Booking_System_Backend.git"`
#### 2. Navigate into the project directory:
   `cd Hall_Booking_System`
#### 3. Install dependencies:
   - `pip install django`
   - `pip install djangorestframework`
   - `pip install djangorestframework-simplejwt`
   - `python manage.py makemigrations`
   - `python manage.py migrate`  
   - `To createsuperuser: python manage.py createsuperuser`
#### 4. Run the system:
   `python manage.py runserver`

## Technologies Used
- Django
- Django-Rest-Framework
- Django-Rest-Framework-simplejwt


