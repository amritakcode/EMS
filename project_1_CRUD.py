#Importing modules
import csv
from pprint import pprint
import re 
import mysql.connector

#Crating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "ems_database" 
)

cursor = mydb.cursor(buffered=True)
cursor.execute("SELECT * FROM employees")


#Custom exception
class NotOption(Exception): pass
class AgeException(Exception): pass

#Created class called Employee
class Employee:
    
    #U/I- terminal console
    def main():
        print("Welcome to the Employee Management System.")
        print("Press: ")
        print("1 to Add Employee Information")
        print("2 to Delete Employee Information")
        print("3 to Update Employee Information")
        print("4 to Display Employee Information")
        print("5 to Exit")

        try: 
            option = int(input("Enter your option number here: "))
            if option == 1:
                Employee.createEmployees()
            elif option == 2:
                Employee.deleteEmployees()
            elif option == 3:
                Employee.updateEmployees()
            elif option == 4:
                Employee.getEmployees()
            elif option == 5:
                exit(0)
            else:
                raise NotOption
        except NotOption:
            print("Invalid option. Please try again.")

##########################################################################################################################################
    #Created employees and added their information into a csv file 
    def createEmployees():
        #Reading the CSV file 
        header = []
        employee_list = []
        try:
            with open("./resources/employees.csv", "r") as file:
                read = csv.DictReader(file, ["First Name", "Last Name", "Age", "ID", "Date of Employment", "Salary", "Department"])
                header = next(read)
                for row in read:
                    employee_list.append(row)
        except FileNotFoundError: print("File Not Found")


        maxNumOfEmployees = int(input("How many employees do you want to add (int)? "))
        counter = 1

        while counter <= maxNumOfEmployees:
            employees = {}
            try: 
                age = int(input("Enter your age (int): "))
                if age < 18:
                    raise AgeException
                firstName = input("Enter your first name: ").capitalize()
                lastName = input("Enter your last name: ").capitalize()
                while True:
                    dateOfEmployment = input("Enter your date of employment (MM/DD/YYYY): ")
                    match = re.search("^\d{2}\/\d{2}\/\d{4}$" ,dateOfEmployment)
                    if match:
                        break
                    else:
                        print("Please enter the correct date in this format - MM/DD/YYYY")
                try:
                    salary = int(input("Enter your salary (int): "))
                except ValueError: 
                    print("You can only enter an integer.")
                department = input("Enter your department: ")
            except AgeException:
                print("You must be 18 or older to work.")
                continue
            
            maxID = 0
            for i in range(len(employee_list)):
                if maxID < int(employee_list[i].get("ID")):
                    maxID = int(employee_list[i].get("ID"))
            maxID+=1

            employees["First Name"] = firstName
            employees["Last Name"] = lastName
            employees["Age"] = age
            employees["ID"] = maxID
            employees["Date of Employment"] = dateOfEmployment
            employees["Salary"] = salary
            employees["Department"] = department

            employee_list.append(employees)
            data_user = (firstName,lastName,age,maxID,dateOfEmployment,salary,department)
            cursor.execute("""INSERT INTO employees(First_Name, Last_Name, Age, ID, Date_of_Employment, Salary, Department) VALUES(%s,%s,%s,%s,%s,%s,%s)""",data_user)
            mydb.commit()
            counter+=1

            #Write employee information to the csv file
            try:
                with open("./resources/employees.csv", "wt", newline="") as file:
                    writer = csv.DictWriter(file, header)
                    writer.writeheader()
                    writer.writerows(employee_list)
            except FileNotFoundError: print("File Not Found")

##########################################################################################################################################
    #Will update employee information 
    def updateEmployees():
    #Reading the CSV file 
        header = []
        employee_list = []
        try:
            with open("./resources/employees.csv", "r") as file:
                read = csv.DictReader(file, ["First Name", "Last Name", "Age", "ID", "Date of Employment", "Salary", "Department"])
                header = next(read)
                for row in read:
                    employee_list.append(row)
        except FileNotFoundError: print("File Not Found")

        for i in range(len(employee_list)):
            id = employee_list[i].get("ID")
            firstName = employee_list[i].get("First Name")
            lastName = employee_list[i].get("Last Name")
            print(f"{id}: {firstName} {lastName}")

        numID = int(input("Select ID of employee you wish to update the information: "))
        print("Displayed are the options you can choose to change.")
        print("Press")
        print("1 for First Name")
        print("2 for Last Name")
        print("3 for Age")
        print("4 for Salary")
        print("5 for Department")
        
        option = int(input("Select the option number you choose to update: "))

        for i in range(len(employee_list)):
            if numID == int(employee_list[i].get("ID")):
                if option == 1:
                    updateFirstName = input("Enter updated First Name here: ")
                    employee_list[i].update({"First Name" : updateFirstName})
                    cursor.execute("UPDATE employees SET First_Name = %s WHERE id = %s", (updateFirstName, numID))
                elif option == 2:
                    updateLastName = input("Enter updated Last Name here: ")
                    employee_list[i].update({"Last Name" : updateLastName})
                    cursor.execute("UPDATE employees SET Last_Name = %s WHERE id = %s", (updateLastName, numID))
                elif option == 3:
                    while True:
                        try:
                            updateAge = int(input("Enter updated Age here: "))
                            break
                        except ValueError:
                            print("Age must be an integer.")
                    employee_list[i].update({"Age" : updateAge})
                    cursor.execute("UPDATE employees SET Age = %s WHERE id = %s", (updateAge, numID))
                elif option == 4:
                    while True:
                        try:
                            updateSalary = input("Enter updated Salary here: ")
                            break
                        except ValueError:
                            print("Salary must be an integer.")
                    employee_list[i].update({"Salary" : updateSalary})
                    cursor.execute("UPDATE employees SET Salary = %s WHERE id = %s", (updateSalary, numID))
                elif option == 5:
                    updateDepartment = input("Enter updated Department here: ")
                    employee_list[i].update({"Department" : updateDepartment})
                    cursor.execute("UPDATE employees SET Department = %s WHERE id = %s", (updateDepartment, numID))
                break

        mydb.commit()

        #Write employee information to the csv file
        try:
            with open("./resources/employees.csv", "wt", newline="") as file:
                writer = csv.DictWriter(file, header)
                writer.writeheader()
                writer.writerows(employee_list)
        except FileNotFoundError: print("File Not Found")

##########################################################################################################################################
    #Will delete employee information 
    def deleteEmployees():
    #Reading the CSV file 
        header = []
        employee_list = []
        try:
            with open("./resources/employees.csv", "r") as file:
                read = csv.DictReader(file, ["First Name", "Last Name", "Age", "ID", "Date of Employment", "Salary", "Department"])
                header = next(read)
                for row in read:
                    employee_list.append(row)
        except FileNotFoundError: print("File Not Found")  

        for i in range(len(employee_list)):
            id = employee_list[i].get("ID")
            firstName = employee_list[i].get("First Name")
            lastName = employee_list[i].get("Last Name")
            print(f"{id}: {firstName} {lastName}") 

        numID = int(input("Select ID of employee you wish to delete the information: "))
        for i in range(len(employee_list)):
            if numID == int(employee_list[i].get("ID")):
                employee_list.pop(i)
                cursor.execute("DELETE FROM employees WHERE id = %s", (f"{numID}", ))
                break

        mydb.commit()

        #Write employee information to the csv file
        try:
            with open("./resources/employees.csv", "wt", newline="") as file:
                writer = csv.DictWriter(file, header)
                writer.writeheader()
                writer.writerows(employee_list)
        except FileNotFoundError: print("File Not Found")

##########################################################################################################################################
    #Will display employee information 
    def getEmployees():
    #Reading the CSV file 
        header = []
        employee_list = []
        displayDepart = [] 
        try:
            with open("./resources/employees.csv", "r") as file:
                read = csv.DictReader(file, ["First Name", "Last Name", "Age", "ID", "Date of Employment", "Salary", "Department"])
                header = next(read)
                for row in read:
                    employee_list.append(row)
        except FileNotFoundError: print("File Not Found")  

        #if they want to search by department
        department = input("Do you want to search employees by their department (Y/N)? ")
        if department == "Y":
            departmentList = []
        
            departmentList = [i[6] for i in cursor]
            print(f"Here is the list of departments available to choose from: {set(departmentList)}")
            choice = input("Which department would you like to see? ")
            displayDepart = [i for i in departmentList if i == choice]

        cursor.execute("SELECT * FROM employees")

        for i in cursor:
            if not displayDepart:
                id = i[3]
                firstName = i[0]
                lastName = i[1]
                print(f"{id}: {firstName} {lastName}")
            else:
                if displayDepart[0] == i[6]:
                    id = i[3]
                    firstName = i[0]
                    lastName = i[1]
                    print(f"{id}: {firstName} {lastName}")

        numID = int(input("Select ID of employee you wish to see the information display: ")) 
        for i in range(len(employee_list)):
            if numID == int(employee_list[i].get("ID")):
                pprint(employee_list[i])
                break

Employee.main()
