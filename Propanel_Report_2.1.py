# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 11:06:21 2019

@author: Pepecito_
Hello Team, this is the most recent version of the Propanel Report program.

Prep: In order to use this program, you will need to export the User Course Data from this page:
https://worldsciencescholars.com/wp-admin/admin.php?page=learndash-lms-reports
Move that file to the same folder that stores this program file.

Step 1: Now you are ready to start the program. After the running the program, you will be given a prompt:
'Enter the name of the Course Data: '. Enter the name of the file WITHOUT the .csv tag 
into the terminal/iPython console.

Step 2: Next, the program will as you to 'Please choose a course.' and will list all courses in alphabetical order.
Enter the number associated with the course you want to analyze.

Step 3: Then, the program will ask you to choose between '1.) 2018 Cohort or 2.) 2019 Cohort: '.
Enter the number you associated with the appropiate cohort.

Step 4: Lastly, the program will give a option to generate a list of students and their completion rates
based on a threshold you chose.

Step 5: When the program is finished. Check the folder that contains the program. There should now be a txt file
named in the following format:
Scholars_Progress_Report_MM_DD_YYYY.
Where MM_DD_YYYY is that days date.
Running the program multiple times a day will append your results to the day's text file.

This is designed this way so that you can run the program on the courses you need on that day and 
then simply attach the txt.file to the Scholars Progress Report email.

"""
import sys
import pandas as pd
import numpy as np
from datetime import datetime






#Method used to open the Exported Course Data.
def open_file():
    file_name = input("Enter the name of the Course Data CSV: ")+'.csv'
    try:
        file = pd.read_csv(file_name, delimiter = ',')
        courses = file.course_title.unique()
        choose_course(file,courses)
    except FileNotFoundError:
           print("File Not Found. Please try again.")
           
#Method to choose which course to analyze.      
def choose_course(file,courses):
    course_number = 1
    
    print('Please choose a course.')
    for course in courses: 
        print(str(course_number) + '.) '+ course)
        course_number+=1
        
    choice = input('Choice: ')
    
    
    filter_data(file, courses[int(choice)-1])

#Method to choose cohort.
def filter_data(file,course_name):
    cohort_2018 = list(range(31, 76))
    cohort_2019 = list(range(133,163))
    
    
    
    choice = input('1.) 2018 Cohort or 2.) 2019 Cohort: ')
    if choice == '1':
        cohort = cohort_2018
        cohort_name = '2018 Cohort'
    elif choice == '2':
        cohort = cohort_2019
        cohort_name = '2019 Cohort'
    else:
        print('Please enter 1 or 2 to choose a cohort.')
    
    
    course_data = file.loc[(file['user_id'].isin(cohort)) & (file['course_title']==course_name)]
    report(course_data, course_name, cohort_name)

#Method to generate the report.
def report(course_data, course_name, cohort_name):
    course_data = course_data.values.tolist()
    
    
    # This line and subsequent copies open the output txt file for day
    report_file = open('Scholars_Progress_Report_'+datetime.today().strftime('%m_%d_%Y')+'.txt','a')
    
    #Stores original stdout for resetting output to terminal later
    old_stdout = sys.stdout
    #Changes output to output txt file
    sys.stdout = report_file
    
    
    #These values keep track of how many scholars have completion rate within a certain range.
    # For reference these variables show how many scholars in the list described above
    not_started = 0 # Unstarted
    quarter_1 = 0 # q1 or 0-25%
    quarter_2 = 0 # q2 or 25-50%
    quarter_3 = 0 # q3 or 50-75%
    quarter_4 = 0 # q4 or 75+%
    ninety_five = 0 # ninefive or 95+%
    
    completed = 0 # This references the amount of scholars who completed the course.
    total = 0 #This is the total amount of scholars
    
    #Used for generating the lists at the end of the program
    unstarted = []
    q1 = []
    q2 = []
    q3 = []
    q4 = []
    ninefive = []
    
    for row in course_data:
        if row[9] != row[9] and row[5]==0:
            not_started+=1
            unstarted.append([row[1], 0])
        else:
            completion_rate = round((row[5]/row[6]) *100)
            if completion_rate >= 0 and completion_rate < 25:
                quarter_1+=1
                q1.append([row[1],completion_rate])
                            
            if completion_rate >= 25 and completion_rate < 50:
                quarter_2+=1
                q2.append([row[1],completion_rate])
            if completion_rate >= 50 and completion_rate < 75:
                quarter_3+=1
                q3.append([row[1],completion_rate])
            if completion_rate >= 75:
                quarter_4+=1
                q4.append([row[1],completion_rate])
            if completion_rate >= 95:
                ninety_five+=1
                ninefive.append([row[1],completion_rate])
            if completion_rate == 100:
                completed+=1
        total+=1
    
    # Generates the first part of the report
    print("Propanel Report for " + course_name + " (" + cohort_name + ")" )
    print("Not Started: " + str(not_started))
    print("0-25%: " + str(quarter_1))
    print("25-50%: " + str(quarter_2))
    print("50-75%: " + str(quarter_3))
    print("75-100%: " + str(quarter_4))
    print("95% and Above: " + str(ninety_five))
    print("Percent Completed: " + str(int(completed/total *100)) + "%")
    print("Total: " + str(total))
    print()
    
    #Resets output to terminal
    report_file.close()
    sys.stdout = old_stdout
    
    print("Would you like a list of students who have...")
    print("1.)...started the course?")
    print("2.)...a completion rate of 25% or above?")
    print("3.)...a completion rate of 50% or above?")
    print("4.)...a completion rate of 75% or above?")
    print("5.)...a completion rate of 95% or above?")
    print("6.)...not started the course?")
    
    choices(unstarted, q1,q2,q3,q4,ninefive)

#Method for generating the list and the end of each report
def choices(unstarted, q1,q2,q3,q4,ninefive):
    user_input = input('Choice: ')
    report_file = open('Scholars_Progress_Report_'+datetime.today().strftime('%m_%d_%Y')+'.txt','a')
    old_stdout = sys.stdout
    sys.stdout = report_file
    print()
    i=1
    if user_input == '1':
        print("The following students have started the course...")
        for scholar in sorted([*q1, *q2, *q3, *q4]):
            print(str(i) + ".) "+ scholar[0] + ", " + str(scholar[1]) + "%")
            i+=1
    elif user_input == '2':
        print("The following students have a completion rate of 25% or higher...")
        for scholar in sorted([*q2, *q3, *q4]):
            print(str(i) + ".) "+ scholar[0] + ", " + str(scholar[1]) + "%")
            i+=1
    elif user_input == '3':
        print("The following students have a completion rate of 50% or higher...")
        for scholar in sorted([*q3, *q4]):
            print(str(i) + ".) "+ scholar[0] + ", " + str(scholar[1]) + "%")
            i+=1
    elif user_input == '4':
        print("The following students have a completion rate of 75% or higher...")
        for scholar in q4:
            print(str(i) + ".) "+ scholar[0] + ", " + str(scholar[1]) + "%")
            i+=1
    elif user_input == '5':
        print("The following students have a completion rate of 95% or higher...")
        for scholar in ninefive:
            print(str(i) + ".) "+ scholar[0] + ", " + str(scholar[1]) + "%")
            i+=1
            
    elif user_input == '6':
        print("The following students have not started the course...")
        for scholar in unstarted:
            print(str(i) + ".) "+ scholar[0] + ", " + str(scholar[1]) + "%")
            i+=1
    else:
        report_file.close()
        sys.stdout = old_stdout
        print("Please enter a number 1 through 6.")
        choices()
    print()
    #Resets output to terminal
    sys.stdout = old_stdout

#Starts program
open_file()
