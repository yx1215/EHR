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


- [Intordution](#Introduction)
- [Design Process](#Design-Process)
- [Use Cases](#Use-Cases)
    - [General Cases](#General-Cases)
    - [Administrators](#Administrators)
    - [Doctors](#Doctors)
    - [Patients](#Patients)
- [Architecture & Design](#Architecture-Design)
- [Reflection](#Reflection)

## Introduction
(2pts)

A brief description of your project (make use of HW1)

- With more and more people enjoying electronic medical device and devote more trust in it. It is feasible to build an electronic health record (EHR) system to cut down hospitals’ spending on hiring people working for registration and reduce the time spent on searching and scheduling. EHR stores patients’ health conditions. By the means of data, it stores all settings that could provide plenty of health care service for patients. Also, it provides doctors with decision opportunities based on the recorded information; meanwhile, it offers automated and streamlined workflows.

## Design Process
(5pts)
- Make sure to address the issues of iterative development, refactoring, testing and collaborative development (even if you are not using XP, you have to address these issues in your documentation).
## Use Cases
(5pts)

This should include the user stories and use cases which you implemented in your project. You do not need to mention the requirements which were dropped.
### General Cases

- **Register/Login**
There are three types of users in our system: administrators, patients and doctors. Administrators are the managers of the system. There is a screte key in the system and only people who are authenticated by the hospital can get the key and create administrator accounts. Patients are the most common types of users, anyone will be able to register an account for patient. Users cannot register doctor accounts by themselves since not everyone is elligible to be a doctor. So only the administrators are able to craete doctor accounts for users. 
        
- **Forget Password**
Users will be able to change passwords in case they forget the passwords. To change the password, the users have to provide some information of the account when registering it such as the email and phone number used to register the account.

- **Chat System**
We provide the functionality of chatting in our system. Anyone would be able to send message to others prividing the email address that they want to send message to.

        
    
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

- Include multiple UML diagrams to show the important parts of your system (you must have UML diagrams).
- Describe in a top-down manner the architecture of your system.
- Include enough details about the design of your system such that anyone who refers to your documentation can understand the major components of your system and how they are related.
- Describe how the choice of the framework influence the design of your system.
## Reflection
(3pts)
Include personal reflections on the project and process by each team member. Describe what you learned.
- **Reflection By Yixiang Xiao**

- **Reflection By Yunxiao Song**

- **Reflection By Xiyan Cai**

- **Reflection By Chongling Zhu**