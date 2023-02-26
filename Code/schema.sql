drop table if exists Employee cascade;
drop table if exists Employee_dependents cascade;
drop table if exists Casting cascade;
drop table if exists Movie cascade;
drop table if exists Movie_has cascade;
drop table if exists Screen cascade;
drop table if exists Screening cascade;
drop table if exists Employee_manages cascade;
drop table if exists UserInfo cascade;
drop table if exists Ticket cascade;

create table Employee(
    emp_id char(12) primary key,
    employee_name varchar(32) not null,
    SSN char(9) unique not null,
    executive_rank integer,
    supervisor_id char(12),
    foreign key(supervisor_id) references Employee(emp_id)
);

create table Employee_dependents(
    dependent_name varchar(32) not null,
    emp_id char(12),
    primary key(dependent_name,emp_id),
    foreign key(emp_id) references Employee(emp_id) on delete cascade
);

create table Casting(
    actor_name varchar(32) primary key,
    dob date,
    age integer
);

create table Movie(
    movie_name varchar(32) primary key,
    release_year integer,
    language varchar(32),
    duration integer,
    genre varchar(64)
);

create table Movie_has(
    movie_name varchar(32),
    actor_name varchar(32),
    primary key(movie_name,actor_name),
    foreign key(movie_name) references Movie(movie_name),
    foreign key(actor_name) references Casting(actor_name)
);

create table Screen(
    screen_no integer primary key,
    capacity integer,
    media_technology varchar(32)
);

create table Screening(
    screening_id char(10),
    price decimal not null,
    start_time timestamp,
    movie_name varchar(32) not null,
    screen_no integer not null,
    primary key(screening_id,start_time),
    unique(start_time,screen_no),
    foreign key(movie_name) references Movie(movie_name),
    foreign key(screen_no) references screen(screen_no)
);

create table Employee_manages(
    screening_id char(10),
    start_time timestamp,
    emp_id char(12),
    primary key(screening_id,start_time,emp_id),
    foreign key(screening_id,start_time) references Screening(screening_id,start_time),
    foreign key(emp_id) references Employee(emp_id)
);

create table UserInfo(
    user_id varchar(32) primary key,
    name varchar(32) not null,
    membership varchar(32) not null,
    dob date,
    gender char(1),
    check(gender in ('M','F')) 
);

create table Ticket(
    ticket_id char(10) primary key,
    screening_id char(10) not null,
    start_time timestamp not null,
    user_id  varchar(32) not null,
    seat_no char(6) not null,
    screen_no integer not null,
    unique(screening_id,start_time,seat_no,screen_no),
    foreign key(screening_id,start_time) references Screening(screening_id,start_time),
    foreign key(user_id) references UserInfo(user_id),
    foreign key(screen_no) references Screen(screen_no) 
)

