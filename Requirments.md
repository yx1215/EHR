# Requirments
1. Your document must have a table of contents.

2. All class, method names, code must be in monospace font. Use a font like Courier, Monaco, etc.

3. All figures must be labeled.

4. Do not draw the diagrams by hand – use a diagraming tool.

5. All pages must be numbered.

6. Your documentation should follow consistent formatting for sections, headers, etc., for the entire document.

7. Your documentation should be at least 5 pages but not more than 10 pages.
 
<!--  -->Start of main contents

# SEEHR Documentation


- [x] [Introdution](#Introduction)
- [x] [Design Process](#Design-Process)
- [x] [Use Cases](#Use-Cases)
    - [General Cases](#General-Cases)
    - [Administrators](#Administrators)
    - [Doctors](#Doctors)
    - [Patients](#Patients)
- [ ] [Architecture & Design](#Architecture/Design)
- [ ] [Reflection](#Reflection)
    - [x] Relection By Yixiang Xiao
    - [ ] Relection By Yunxiao Song
    - [x] Relection By Xiyan Cai
    - [x] Relection By Chonglin Zhu
## Introduction
(2pts)

A brief description of your project (make use of HW1)

- With more and more people enjoying electronic medical device and devote more trust in it, it is feasible to build an electronic health record (EHR) system to cut down hospitals’ spending on hiring people working for registration and reduce the time spent on searching and scheduling. EHR stores patients’ medical history records without the risk of losing the medical history book. By the means of data, it stores all settings that could provide plenty of health care service for patients. Also, it provides doctors with decision opportunities based on the recorded information; meanwhile, it offers automated and streamlined workflows.
- The final name of our system is SEEHR, which is a combination of SE (Software Engineering) and EHR (Electronic Health Record). However, it can also be understood as See HR since our project focuses more on the administrative perspective. 

## Design Process
(5pts)
- We release the bi-weekly artifects throught the semester. The order is: 
    1. Login, registration: In the first iteration, we mostly learnt to get familiar with the coding language and environment. The login and registration situations are different among different stakeholders (see [General Cases](#General-Cases))
    2. Request appointment, accept appointment: This stage connected the functions of patients' and doctors' by sending and accepting appointment requests, respectively.
    3. Medical history report: It is a refactored stage. In the end, after each appointment, a doctor is required to finish the medical history report regarding to that appointment. Doctors can view their patients' medical history but cannot edit it.
    4. Message System
    5. Emergency contact button, Send notification: 
        - The emergency contact button is designed at first. It may not seem to be reasonable comparing to directly dialing 120. However, if a doctor is logging into his account in his phone, once a patient clicks this button, he will receive an instant message marked urgent. Then the doctor can choose to present at the hospital even if he is not on duty to support the treatment. 
        - As for sending notification, it is a function that is not initially planned. Although the message system provides some apis to send notifications to a certain person, a recent recieved notification will not be presented on the dashboard without manually refreshing the homepage, unlike the delicated page for message. Then we decided to present the notification as a flashed message from HTML instead of a received message. 
- In the first two stages, the development was not too complicated. However, we have refactored the medical history report for many times. 
    - It is due to the problematic use case design at first.
    - Previously, we plan to associate the medical history report with each patient as a database feature in the type of "text". 
    - As more and more report was added, the text became too long to handle by a doctor. The doctor may have the risk of modifying or deleting the previous medical history of a patient, which was not user friendly.
    - After refactoring, each medical report is associated with an appointment as a database feature. Therefore, doctors will only have the read access to other reports and can only edit the report.
- We also encounter some problems when merge the message system into our main system. 
    - Since we design the message system and the main system separately, they have different backend server code. Message system uses node js while the main system uses flask. 
    - At first, when we tried to merge them together, we always see the error of CORS policy violation so that the message system is not working properly.
    - Later we found out that CORS is used to prevent cross origin request for safty issues and this is because we set different origins for the message system and the main system: one is `http://localhost` and one is `http://127.0.0.1`. After we fix this, the message system can then working properly with our main system.
- In the last iteration, we didn't encounter any big problems. 

## Use Cases
(5pts)

This should include the user stories and use cases which you implemented in your project. You do not need to mention the requirements which were dropped.
### General Cases

- **Register/Login**
There are three types of users in our system: administrators, patients and doctors. Administrators are the managers of the system. There is a screte key in the system and only people who are authenticated by the hospital can get the key and create administrator accounts. Patients are the most common types of users, anyone will be able to register an account for patient. Users cannot register doctor accounts by themselves since not everyone is elligible to be a doctor. So only the administrators are able to craete doctor accounts for users. 
        
- **Forget Password**
Users will be able to change passwords in case they forget the passwords. To change the password, the users have to provide some information of the account when registering it such as the email and phone number used to register the account.

- **Message System**
We provide the functionality of sending messages in our system. Anyone would be able to send message to others prividing the email address that they want to send thr message to. And anyone who receives the message will get a notification.

### Administrators
- **Browse doctors**
Administrators can view a list of the doctors registered in the system and select a doctor to see his or her detail information.

- **Add/Delete Doctors**
Administrators can help doctors create doctor accounts. Also, as manager of the system, they are also able to delete doctor accounts from system when the user of the account retires.

### Patients
- **Edit Personal Information**
Patients will be able to edit their persoanl information such as weight, height and emergency contacts. However, they are not able to change information such as their name or date of birth because these information should only be provided when they register the account.
- **Make Appointments**
Patients will be able to make appointments with doctors. This user case has two different situations.
    - **Patients do not have a provider yet**
    If a patient does not have a doctor as their provider, they can choose any doctor in the system to make appointments with. They will also be able to search for doctors providing information such as time slots wanted, doctor name and appointment duration.
    - **Patients already have a provider**
    If a patient already has a provider, he or she can only make appointments with that specific doctor in the provided time slots.
    
- **View Medical History**
The system will provide a time line of all the appointments along with the corresponding medical history.

- **Visiting Warning**
The system will automatically notice the patient if the patient hasn't made an appointment with a doctor in 30 days, to remind the patient check his or her status with a doctor in time.

- **Emergency Alert Button**
There is a button on the right up corner of the patient's home page. When the patient is suddenly in danger, he or she can press the button to inform all the doctors in the system that he or she is danger and need help.

### Doctors
- **Accpet Appointments**
Doctors can accept appoitments made by the patients. However, they will not be able to reject the appointments since the time slots are provided by themselves so it's their responsiblity to accept the appoitments and take care the patients.

- **Manage Schedule**
Doctors will be able to manage their own schedules.
    - **Add/Delete Time Slots**
    Doctors will be able to add new time slots for patients for make appointment with. In the same way, doctors can delete free schedules before they are booked. 
    - **View Schedule Detail**
    Doctors can select one time slots and view the detail schedule information such as if the schedule has been occupied and if yes it will also show the information of the patient who made the appointment.

- **Medical History Report**
Doctors will be able to manage the medical history reports.
    - **View History Report**
    Doctors will be able to view the history report for each appoitment separately as well as view all the reports for a patient as a whole.
    - **Edit History Report**
    Doctors will also be able to edit the report for each of the appointment made with him. The doctor can only edit the report for one time slots at a time and this can prevent him from changing the report for other slots by mistake.
    
## Architecture/Design
(5pts)

Include multiple UML diagrams to show the important parts of your system (you must have UML diagrams).

Describe in a top-down manner the architecture of your system.

Include enough details about the design of your system such that anyone who refers to your documentation can understand the major components of your system and how they are related.

Describe how the choice of the framework influence the design of your system.


- The following is the Class Diagram.

| ![](https://i.imgur.com/LojYIhE.png)|
| :--: |
|  *Use Case Diagram*  |
- The following is the Use Case Diagram.

Login and registration are first released. Then we are able to access the interface of different stakeholders. Three interfaces of three types of stakeholders are set as blackboxes and we are able to add functionalities to it.

| ![](https://i.imgur.com/J35HtTu.png) |
| :--: |
|  *Class Diagram*  |



## Reflection
(3pts)
Include personal reflections on the project and process by each team member. Describe what you learned.
- **Reflection By Yixiang Xiao**
During the whole process of doing the project, I am in charge of the backend part design as well as some Javascript code for front end. Overall I think I've done a good job since I've finished most of the functionalities we planned at the beginning of the process except for some deprecated functions. However, there are still several things that I have to reflect on. Testing is one of the things that I didn't do well. I didn't write unit test along with the backend code. Instead, I test the backend code directly using the front end code after it is finished. This is not that efficient since I have to wait until the front end is done can I test my backend code. There are several ways of improvements to this. The first is writing the unit test code along with the backend code. The second way to test the code without the frontend is to use some external softwares such as Postman, which allows me to send queries to the server directly. The second thing I want to reflect on is how I deal with the interaction between the frontend and backend. At first I used ajax to send jqueries from frontend to backend. However, ajax is used to send queries to backend without refreshing the page. This means that after submiting the queries, the user has to refresh the page to view the changes, which is not very user friendly. So later on I changed these ajax queries to a simple statement `loaction.href={{url_for('target function')}} + required parameters.`. This can directly send parameters to backend and call the target function as well as refresh the page automatically which can make our system more convenience for our users. I've also realize the importance of Github during the process and the fact that I have to learn more about how to make use of it to do version control. One thing we didn't do well is that we always push code to the master branch. This may lead to a problem that almost everytime we push we may encounter a conflict and have to resolve it manually, which is not efficient. To do better, each person should create his own branches and push code to that specific branch by himself. And at last we can merge these branches together to get our final project.

- **Reflection By Yunxiao Song**

- **Reflection By Xiyan Cai**
    - I have mostly done the backend part of the project in addition to the separated message system. I also planned and organized each weekly meetings to facilitate the project progress. As a relection, I at first chose to use Python Flask as our base language since all of the team members are familiar with Python. However, it was actually a good moment to push myself to learn a new programming language and get command of it by practicing it on a project. Besides, our team did not plan the whole agile progress and the specific tasks of each team member, which resulted in the problems like less communication within the team and missing a teammate during several iterations. 
    - When we were designing the user cases, we did not consider the aspect of being user friendly. Instead, the purpose of our design lied in how to connect the systems as a whole and make it function smoothly. Therefore, it resulted in the unser-unfriendly experiences like adding medical history report. Therefore, we should have put the user-friendly design into consideration at every moment of conducting a design.
    - Last but not the least, we did not have the document to keep the process of our work and to be refered at any time when we had confusion on the design.
- **Reflection By Chongling Zhu** I mainly designed and built the message system and incorporated it into the main system, and also helped fix some bugs in the main system. I learned a lot in the development of this software engineering project. Firstly, I realized that practice makes perfect. I had learned a lot of front-end and back-end developing techniques in either previous coursework or internship experiences. This project gave me the opportunity to practice those techniques again. In the process, I found out that I previously had some wrong understandings on some usages of the frameworks, and I also master some novel usages of them. Though the practice, my skills got improved again. Secondly, I was mainly working on solo projects previously, where I took care of everything on my own and in my own way. However, this is a group project, where there's a division of work involved. So we need to agree on a lot of things at first, which is difficult because different people tend to have different opinions. Likewise, I found out that I may have some difficulties understanding codes written by other group members. All of the factors make it a real "software engineering" project, which gives me a bite of what would be like in my future careers. The project lets me learn how to communicate and work with other people to achieve something like "1+1>2." Last but not least, the course content itself had a good introduction to some basic concepts on software engineering, which not only broadens my understandings and also helps me better implement this project. In a word, it was a really great experience.
