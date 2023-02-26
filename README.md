# Movie-Ticketing-System
This project aims to develop an online booking system for movie tickets. The system will provide users with real-time information on the availability of movies and their timings. This will enable them to easily book tickets and plan their movie-watching experience. It will also provide employees with the tools they need to manage the cinema screen and ensure that the movie-watching experience is seamless for users.

## Features
- Real-time information on movie availability and timings
- Easy booking of tickets
- Tools for employees to manage cinema screens
- Information on movies, cast, and screening

## Entity Sets
- Employee
- User
- Movie
- Screen
- Dependents (Weak Entity)
- Screening
- Tickets
- Cast

## Relationship Sets
- Reports
- Plays
- Has
- Features
- Employee_manages
- At
- For
- Contains
- Reserved_by

## Attributes
- Movie (movie_name (primary key), release_year, language, duration, genre)
- Cast (actor_name (primary_key), dob, age)
- Tickets (Ticket_id (primary_key))
- Screening (screening_id (primary_key), start_time (primary_key), price)
- Employee (emp_id (primary_key), name, SSN, executive_rank)
- Dependents (name) – It will be a weak entity, dependent on Employee.
- Screen (screen_no (primary_key), capacity, media_technology)
- User (user_id (primary_key), name, membership, dob, gender)

## Business Rules
- Users are uniquely identified by their user_id and has name, membership type, dob, gender.
- Screen is uniquely identified by Screen_no and has capacity, media technology.
- Movie contains list of all the movies in the database. They are uniquely identified by the Movie_name and has release_year, duration, languages, genre. Each movie has some cast of at least one.
- Cast is uniquely identified by actor_name and has age, dob.
- Employees are uniquely identified by their emp_id and has name, SSN, executive_rank.
- Employee reports to at most one supervisor.
- Employee has dependents (weak entity). Dependents only exists with occurrence of identified employee.
- Screening entity It is uniquely identified by screening_id and start_timestamp and has price. Each screening plays exactly one movie, but same movie can be played in multiple screening.
- Each screening of movie is managed by at least one employee.
- Tickets are uniquely identified by the ticket_id and has a seat number. For same screening, tickets for same seat can’t be sold to multiple user.
- A user can reserve any number of tickets, but each ticket is reserved by exactly one user. The seat_no on each ticket should be recorded.
