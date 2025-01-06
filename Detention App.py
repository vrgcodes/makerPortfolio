from datetime import date, datetime
import mysql.connector as mysql
import random

def detention_list():

    HOST = "localhost"
    DATABASE = "detention"
    USER = "root"
    PASSWORD = "T79N7g&$n"

    conn = mysql.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD)
    cursor2 = conn.cursor(buffered=True)
    valid = False

    while not valid:
        try:
            menu = int(input("""
What service would you like today? 
1. Add a uniform violation
2. Remove a uniform violation
3. Add a detention
4. Remove a detention
5. Add a Saturday detention
6. Remove a Saturday detention
7. View uniform violations
8. View lunch time detentions yet to be attended
9. View all lunch time detentions
10. View Saturday detentions yet to be attended
11. View all Saturday detentions
12. Attendance for detention
13. Attendance for Saturday detention
"""))
            if menu < 1 or menu > 11:
                print("Invalid input, please try again!")
                continue
            else:
                valid = True
        except ValueError:
            print("Invalid input, please try again!")
            continue

    today = date.today()
    end = 1
    name = "name"

    def counted_list(table, count_table, count_field):
        sql_count = f"SELECT Name, Class, COUNT(*) AS count FROM {table} GROUP BY Name"
        cursor2.execute(sql_count)
        final_list = cursor2.fetchall()
        cursor2.execute(f"TRUNCATE TABLE {count_table}")
        for i in range(len(final_list)):
            sql_count = f"""INSERT INTO {count_table}(Name, Class, {count_field}) VALUES (%s, %s, %s)"""
            data_count = (final_list[i][0], final_list[i][1], final_list[i][2])
            cursor2.execute(sql_count, data_count)

    def add_violation():
        name = str(input("Enter the name of the student (e.g., Veer Gudhka): "))
        cLass = str(input("Enter the class (e.g., 12A): "))
        reason = str(input("Enter the reason for this detention: "))
        authority = str(input("Enter the name of prefect/teacher giving detention: "))
                
        return name, cLass, reason, authority

    if menu == 1:
        while end != 0:
            name = str(input("Enter the name of the student (e.g., Veer Gudhka): "))
            cLass = str(input("Enter the class (e.g., 12A): "))
            authority = str(input("Enter the name of prefect/teacher giving detention: "))

            sql_uniform = """INSERT INTO uniform(Date, Name, Class, Prefect_Teacher) VALUES (%s, %s, %s, %s)"""
            data_uniform = (str(today), name, cLass, authority)
            cursor2.execute(sql_uniform, data_uniform)

            sql_count_query = "SELECT Name FROM uniform_counter"
            cursor2.execute(sql_count_query)
            result = cursor2.fetchall()
            if len(result) == 0:
                counted_list("uniform", "uniform_counter", "No_of_Violations")
            for i in range(len(result)):
                if name == result[i][0]:
                    sql_increment = f"UPDATE uniform_counter SET No_of_Violations = No_of_Violations + 1 where Name = '{result[i][0]}'"
                    cursor2.execute(sql_increment)
                else:
                    counted_list("uniform", "uniform_counter", "No_of_Violations")

            while True:
                try:
                    end = int(input("Enter 0 to end the program or 1 to continue the program: "))
                    if end !=0 and end !=1:
                        continue
                    else:
                        break
                except ValueError:
                    continue

    if menu == 3:
        while end != 0:
            lunch_time_dt = add_violation()
            sql_detention = """INSERT INTO lunch_detention(Date, Name, Class, Reason, Prefect_Teacher) VALUES (%s, %s, %s, %s, %s)"""
            data_detention = (str(today), lunch_time_dt[0], lunch_time_dt[1], lunch_time_dt[2], lunch_time_dt[3])
            cursor2.execute(sql_detention, data_detention)

            sql_count_query = "SELECT Name FROM dt_counter"
            cursor2.execute(sql_count_query)
            result = cursor2.fetchall()
            if len(result) == 0:
                counted_list("lunch_detention", "dt_counter", "No_of_Detentions")
            for i in range(len(result)):
                if name == result[i][0]:
                    sql_increment = f"UPDATE dt_counter SET No_of_Detentions = No_of_Detentions + 1 where Name = '{result[i][0]}'"
                    cursor2.execute(sql_increment)
                else:
                    counted_list("lunch_detention", "dt_counter", "No_of_Detentions")

            while True:
                try:
                    end = int(input("Enter 0 to end the program or 1 to continue the program: "))
                    if end !=0 and end !=1:
                        continue
                    else:
                        break
                except ValueError:
                    continue
    if menu == 5:
        while end != 0:
            saturday_dt = add_violation()
            sql_sdetention = """INSERT INTO lunch_detention(Date, Name, Class, Reason, Prefect_Teacher) VALUES (%s, %s, %s, %s, %s)"""
            data_sdetention = (str(today), saturday_dt[0], saturday_dt[1], saturday_dt[2], saturday_dt[3])
            cursor2.execute(sql_sdetention, data_sdetention)

            sql_count_query = "SELECT Name FROM saturday_dt_counter"
            cursor2.execute(sql_count_query)
            result = cursor2.fetchall()
            if len(result) == 0:
                counted_list("saturday_detention", "saturday_dt_counter", "No_of_Saturday_Detentions")
            for i in range(len(result)):
                if name == result[i][0]:
                    sql_increment = f"UPDATE saturday_dt_counter SET No_of_Saturday_Detentions = No_of_Saturday_Detentions + 1 where Name = '{result[i][0]}'"
                    cursor2.execute(sql_increment)
                else:
                    counted_list("saturday_detention", "saturday_dt_counter", "No_of_Saturday_Detentions")

            while True:
                try:
                    end = int(input("Enter 0 to end the program or 1 to continue the program: "))
                    if end !=0 and end !=1:
                        continue
                    else:
                        break
                except ValueError:
                    continue

    def remove_violation(table, table2, count_field):

        name_remove = str(input("Enter the name of the student (e.g., Veer Gudhka): "))
        detention_reason = str(input("Enter the reason of detention: "))

        sql_remove_query = f"SELECT Name, Reason FROM {table}"
        cursor2.execute(sql_remove_query)
        result = cursor2.fetchall()

        if len(result) == 0:
            print(f"{name_remove} does not have any detentions!")
        for i in range(len(result)):
            if (name_remove == result[i][0]) and (detention_reason == result[i][1]):
                sql_remove = f"DELETE FROM {table} WHERE Name = '{name_remove}' AND Reason = '{detention_reason}'"
                cursor2.execute(sql_remove)
                sql_count = f"SELECT {count_field} from {table2} WHERE Name = '{name_remove}'"
                cursor2.execute(sql_count)
                result2 = cursor2.fetchall()
                if result2[0][0] == 1:
                    sql_remove_count = f"DELETE FROM {table2} WHERE Name = '{name_remove}'"
                    cursor2.execute(sql_remove_count)
                else:
                    sql_decrement = f"UPDATE {table2} SET {count_field} = {count_field} - 1 where Name = '{name_remove}'"
                    cursor2.execute(sql_decrement)

            else:
                print(f"{name_remove} does not have any detentions!")

    if menu == 2:
        while end != 0:
            name_remove = str(input("Enter the name of the student (e.g., Veer Gudhka): "))
            violation_date = str(input("Enter the date of the violation(YYYY-MM-DD): "))
            
            sql_remove_query = f"SELECT Name, Date FROM uniform"
            cursor2.execute(sql_remove_query)
            result = cursor2.fetchall()

            if len(result) == 0:
                print(f"{name_remove} does not have any violations!")
            for i in range(len(result)):
                if (name_remove == result[i][0]) and (datetime.strptime(violation_date, '%Y-%m-%d').date() == result[i][1]):
                    sql_remove = f"DELETE FROM uniform WHERE Name = '{name_remove}' AND Date = '{violation_date}'"
                    cursor2.execute(sql_remove)
                    sql_count = f"SELECT No_of_Violations from uniform_counter WHERE Name = '{name_remove}'"
                    cursor2.execute(sql_count)
                    result2 = cursor2.fetchall()
                    if result2[0][0] == 1:
                        sql_remove_count = f"DELETE FROM uniform_counter WHERE Name = '{name_remove}'"
                        cursor2.execute(sql_remove_count)
                    else:
                        sql_decrement = f"UPDATE uniform_counter SET No_of_Violations = No_of_Violations - 1 where Name = '{name_remove}'"
                        cursor2.execute(sql_decrement)
                else:
                    print(f"{name_remove} does not have any detentions!")

            while True:
                try:
                    end = int(input("Enter 0 to end the program or 1 to continue the program: "))
                    if end !=0 and end !=1:
                        continue
                    else:
                        break
                except ValueError:
                    continue
                    
    if menu == 4:
        while end != 0:
            remove_violation("lunch_detention", "dt_counter", "No_of_Detentions")
            while True:
                try:
                    end = int(input("Enter 0 to end the program or 1 to continue the program: "))
                    if end !=0 and end !=1:
                        continue
                    else:
                        break
                except ValueError:
                    continue

    if menu == 6:
        while end != 0:
            remove_violation("saturday_detentions", "saturday_dt_counter", "No_of_Saturday_Detentions")
            while True:
                try:
                    end = int(input("Enter 0 to end the program or 1 to continue the program: "))
                    if end !=0 and end !=1:
                        continue
                    else:
                        break
                except ValueError:
                    continue

    def split_list(list):
        length = len(list)
        middle = length//2
        first_half = list[:middle]
        second_half = list[middle:]
        return first_half, second_half
    
    def full_list(table):
        print("Below are the violations:")
        sql_show = f"SELECT * from {table}"
        cursor2.execute(sql_show)
        result = cursor2.fetchall()
        for item in result:
            print(f"{item[0]} - {item[1]} - {item[2]} - {item[3]} - {item[4]}")
 
    if menu == 7:
        print("Below are the violations:")
        sql_show = f"SELECT * from uniform"
        cursor2.execute(sql_show)
        result = cursor2.fetchall()
        for item in result:
            print(f"{item[0]} - {item[1]} - {item[2]} - {item[3]}")

    if menu == 8:
        print("Below are the violations:")
        sql_show = f"SELECT * from lunch_detention WHERE Attendance = 0"
        cursor2.execute(sql_show)
        result = cursor2.fetchall()
        random.shuffle(result)
        tuesday, thursday = split_list(result)[0],split_list(result)[1]
        print("1st Day")
        for item in tuesday:
            print(f"{item[0]} - {item[1]} - {item[2]} - {item[3]} - {item[4]}")
        print("2st Day")
        for item in thursday:
            print(f"{item[0]} - {item[1]} - {item[2]} - {item[3]} - {item[4]}")
    
    if menu == 9:
        full_list("lunch_detention")

    if menu == 10:
        print("Below are the violations:")
        sql_show = f"SELECT * from saturday_detention WHERE Attendance = 0"
        cursor2.execute(sql_show)
        result = cursor2.fetchall()
        for item in result:
            print(f"{item[0]} - {item[1]} - {item[2]} - {item[3]} - {item[4]}")

    if menu == 11:
        full_list("saturday_detention")

    def attendance(table, table2, count_field):
        name_of_student = str(input("Enter the name of the student (e.g., Veer Gudhka): "))
        cLass = str(input("Enter the class of the student (e.g., 12A): "))
        reason = str(input("Enter the reason for this detention: "))
        attended = str(input(f"Did {name_of_student} attend detention? (Y/N/Valid Reason)"))

        if attended == "Y":
            sql_attendance = f"UPDATE {table} SET Attendance = 1 WHERE Name = '{name_of_student}' AND Reason = '{reason}'"
            cursor2.execute(sql_attendance)
        if attended == "N":
            sql_nAttend = f"INSERT INTO {table}(Date, Name, Class, Reason) VALUES (%s, %s, %s, %s)"
            data_nAttend = (str(today), name_of_student, cLass, "Did not attend detention")
            cursor2.execute(sql_nAttend, data_nAttend)
            sql_increment = f"UPDATE {table2} SET {count_field} = {count_field} + 1 where Name = '{name_of_student}'"
            cursor2.execute(sql_increment)

    if menu == 12:
        while end != 0:
            attendance("lunch_detention", "dt_counter", "No_of_Detentions")
            while True:
                try:
                    end = int(input("Enter 0 to end the program or 1 to continue the program: "))
                    if end !=0 and end !=1:
                        continue
                    else:
                        break
                except ValueError:
                    continue
            
    if menu == 13:
        while end != 0:
            attendance("saturday_detention", "saturday_dt_counter", "No_of_Saturday_Detentions")
            while True:
                try:
                    end = int(input("Enter 0 to end the program or 1 to continue the program: "))
                    if end !=0 and end !=1:
                        continue
                    else:
                        break
                except ValueError:
                    continue

    def alerts(count_field, count_field2, table, table2, table3):
        sql_count = f"SELECT Name,Class,{count_field} from {table}"
        cursor2.execute(sql_count)
        result2 = cursor2.fetchall()
        for i in range(len(result2)):
            if result2[i][2] == 3:
                sql_tStrike = f"INSERT INTO {table2}(Date, Name, Class, Reason, Prefect_Teacher) VALUES (%s, %s, %s, %s, %s)"
                data_tStrike = (str(today), result2[i][0], result2[i][1], "Three strikes", "N/A")
                cursor2.execute(sql_tStrike, data_tStrike)
                sql_count_query = f"SELECT Name FROM {table}"
                cursor2.execute(sql_count_query)
                result = cursor2.fetchall()
                if name == result[i][0]:
                    sql_increment = f"UPDATE uniform_counter SET No_of_Violations = No_of_Violations + 1 where Name = '{result[i][0]}'"
                    cursor2.execute(sql_increment)
                else:
                    counted_list(table2, table3, count_field2)

    alerts("No_of_Violations", "No_of_Detentions", "uniform_counter", "lunch_detention", "dt_counter")
    alerts("No_of_Detentions", "No_of_Saturday_Detentions", "dt_counter", "saturday_detention", "saturday_dt_counter")

    conn.commit()
    conn.close()

detention_list()

while True:
    proceed = str(input("Do you want to access any more services? (Y/N)"))
    if proceed != "Y" and proceed != "N":
        print("Invalid input, please try again!")
        continue
    else:
        break

if proceed == "Y":
    detention_list()
if proceed == "N":
    print("THank you for using the app!")