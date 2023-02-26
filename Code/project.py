import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

"# Movie Ticketing System"


@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df


"## Read Tables"

sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
try:
    all_table_names = query_db(sql_all_table_names)["relname"].tolist()
    table_name = st.selectbox("Choose A Table.", all_table_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")
else:
    if table_name:
        f"Display the table"

        sql_table = f"SELECT * FROM {table_name};"
        try:
            df1 = query_db(sql_table)
            st.dataframe(df1)
        except:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )

"## Query Employee"

sql_employee_ids = "SELECT emp_id FROM Employee;"
try:
    employee_ids = query_db(sql_employee_ids)["emp_id"].tolist()
    employee_id = st.selectbox("Choose An Employee_id.", employee_ids)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")
else:
    if employee_id:
        sql_employee = f"""select E3.emp_id, E3.employee_name, E3.ssn, E3.executive_rank,E3.supervisor_name,ED.dependent_name 
                        from ((select E1.emp_id, E1.employee_name, E1.ssn, E1.executive_rank,E2.employee_name as supervisor_name 
                            from Employee E1 
                            left join 
                            Employee E2 on E1.supervisor_id = E2.emp_id) E3 
                                left join 
                            Employee_dependents ED on E3.emp_id = ED.emp_id ) where E3.emp_id='{employee_id}';"""
        try:
            table1 = query_db(sql_employee)
            employee_info = table1.loc[0]
            employee_name = employee_info["employee_name"]
            ssn = employee_info["ssn"]
            executive_rank = employee_info["executive_rank"]
            supervisor_name = employee_info["supervisor_name"]
            dependent_name = employee_info["dependent_name"]

            if len(table1) > 1:
                for i in range(1, len(table1)):
                    dependent_name += ", "+table1["dependent_name"][i]

            st.write(f"employee_id: {employee_id}\n")
            st.write(f"employee_name: {employee_name}\n")
            st.write(f"SSN: {ssn}\n")
            st.write(f"executive_rank: {executive_rank}\n")
            st.write(f"supervisor_name: {supervisor_name}")
            st.write(f"dependents_name: {dependent_name}")
        except:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )

"## Customers Who Watched A Particular Movie."

sql_movie_names = "SELECT movie_name FROM Movie;"
try:
    movie_names = query_db(sql_movie_names)["movie_name"].tolist()
    movie_name = st.selectbox("Choose A Movie Name", movie_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")
else:
    if movie_name:
        sql_customers = f"""select u.name, u.user_id,u.gender, u.dob
                            from ticket t join screening s on t.screening_id = s.screening_id and t.start_time = s.start_time
                            join userinfo u on t.user_id = u.user_id
                            where s.movie_name='{movie_name}';"""
        try:
            df2 = query_db(sql_customers)
            if len(df2) > 0:
                st.dataframe(df2)
            else:
                st.write(
                    f"No one has watched the movie {movie_name}."
                )
        except:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )

"## List All The Screenings Of The Day."

num_day = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
           7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
try:
    day = st.radio("Choose A Screening Day.",
                   ('Today', 'Tomorrow', 'Day after tomorrow'))
    i = 0
    if day == 'Tomorrow':
        i = 1
    elif day == 'Day after tomorrow':
        i = 2
    date_query = "select extract(Day from Now()) as day ,extract(month from Now()) as month, extract(year from Now()) as year;"
    date = query_db(date_query).loc[0]
    date_day = int(date["day"])
    date_month = int(date["month"])
    date_year = int(date["year"])

    date_day += i
    if date_day > num_day[date_month]:
        date_day = (date_day+i)-num_day[date_month]
        date_month += 1
    if date_month == 13:
        date_month = 1
        date_year += 1

except:
    st.write("Sorry! Something went wrong with your query, please try again.")
else:
    if date_day:
        screening_query = f"""SELECT X.movie_name, X.screen_no, TO_CHAR(X.start_time, 'HH24:MI') AS start_time, S.media_technology 
                                FROM screening AS X 
                                JOIN screen AS S ON X.screen_no = S.screen_no 
                                WHERE EXTRACT(DAY FROM X.start_time) = {date_day} 
                                AND EXTRACT(MONTH FROM X.start_time) = {date_month} 
                                AND EXTRACT(YEAR FROM X.start_time) = {date_year};"""

        try:
            st.write('Date: ', str(date_month), str(date_day), str(date_year))
            df3 = query_db(screening_query)
            if len(df3) > 0:
                st.dataframe(df3)
            else:
                st.write(
                    "There is no screening held for the selected day."
                )
        except:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )


"## Total Tickets Sold For A Movie."

try:
    mov_names = query_db(sql_movie_names)["movie_name"].tolist()
    mov_name = st.selectbox("Choose A Movie Name.", mov_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")
else:
    if mov_name:
        sql_no_tickets = f"""SELECT m.movie_name, COUNT(t.ticket_id) as ticket_count,m.language,m.genre FROM Movie m INNER JOIN Screening s ON m.movie_name = s.movie_name INNER JOIN Ticket t ON t.screening_id = s.screening_id AND t.start_time=s.start_time where m.movie_name='{mov_name}' GROUP BY m.movie_name;"""
        try:
            df4 = query_db(sql_no_tickets)
            if len(df4) > 0:
                st.dataframe(df4)
            else:
                st.write(
                    f"There are no tickets sold for the movie '{mov_name}'."
                )
        except:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )


"## Average Age Of the Users Intrested In A Particular Genre."
try:
    age = st.slider("Minimum AVG Age Of Customers Per Genre.", 0, 60, 10)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")
else:
    if age:
        avg_age_sql = f"""SELECT * from (
                        SELECT m.genre,AVG(EXTRACT(YEAR FROM current_date) - EXTRACT(YEAR FROM u.dob))::decimal(10,0) as avg_age
                        FROM UserInfo u
                        JOIN Ticket t ON u.user_id = t.user_id
                        JOIN Screening s ON t.screening_id = s.screening_id AND t.start_time = s.start_time
                        JOIN Movie m ON s.movie_name = m.movie_name
                        group by m.genre
                        ) temp where temp.avg_age>={age};"""
        try:
            df5 = query_db(avg_age_sql)
            if len(df5) > 0:
                st.dataframe(df5)
            else:
               st.write(
                f"No Genre has avg viewer age greater than {age}."
                ) 
        except:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )


"## Languages Known by Actor/Actress."

sql_actor_names = "select * from Casting;"
try:
    actor_names = query_db(sql_actor_names)["actor_name"].tolist()
    actor_name = st.selectbox("Choose An Actor/Actress Name.", actor_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")
else:
    if actor_name:
        sql_num_langueages = f"""select actor_name, count(*) as count from
                                (select distinct C.actor_name,M.language from 
                                Casting C join Movie_has MH on C.actor_name=MH.actor_name
                                join Movie M on MH.movie_name=M.movie_name) temp
                                where actor_name = '{actor_name}'
                                group by actor_name;"""
        try:
            df6 = query_db(sql_num_langueages)
            if len(df6) > 0:
                st.write(f"{df6.loc[0]['actor_name']} knows {df6.loc[0]['count']} language/s.")
            else:
                st.write(f"Language data unavailable for {df6.loc[0]['actor_name']}.")

        except:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )


"## Number Of Screening Managed By AN Employee."
try:
    screening_num = st.slider("Minimum Screening Count.", 1, 5)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")
else:
    if screening_num:
        sql_employee_no_screening = f"""select * from (
                            select e.emp_id,e.employee_name,count(*) from
                            employee_manages em join employee e on em.emp_id =e.emp_id
                            group by e.emp_id,e.employee_name
                        ) temp 
                        where count >= {screening_num};"""
        try:
            df7 = query_db(sql_employee_no_screening)
            if len(df7) > 0:
                st.dataframe(df7)
            else:
                 st.write(f"No employee manages more than {screening_num} screenings.")
        except:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
