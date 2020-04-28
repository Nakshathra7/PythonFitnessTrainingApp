# IS 437 Final Project Documentation

## Project Title : 

#### Fitness Training Web App
 
## Project Description:

##### The main purpose of this project is to create online fitness training application for users. The application will have three roles - Member, Trainer, Admin. The Member, Admin and Trainer can perform CRUD operations for their role based functionalities. The Member will provide the personal and health record details. The Trainer will provide trainer information, workout, and meal plan details. The Admin will analyze the member application and assign the trainer to each member. The application will have seven tables - Member Details, Member Health Records, Workout details, Trainer Details, Meal Plan Details, Subscription Details, TrainerAssignment Details. The Admin based on the subscription and health record details will assign trainer to each member. Trainer after analyzing BMI and health record details will provide workout and meal plan suggestions to assigned member. Once after the mealplan and workout assignment by trainer is done, the corresponding member can view their details. Login will be common screen for admin, member and trainer with login credentials as Email and password. Separate sign up form for member and trainer, once after successful sign up the member/trainer can proceed for login.

## Member Use Cases:

* Member Creates Memeber Personal Profile
* Member Updates Memeber Personal Profile
* Member Read Memeber Personal Profile
* Member Creates Health Records
* Member Reads Health Records
* Member Updates Health Records
* Member Read Assigned Workout Details
* Member Read Assigned Meal Plan
* Member Read Subscription

## Trainer Use Cases:

* Trainer Creates Trainer Personal Profile
* Trainer Read Trainer Personal Profile
* Trainer Updates Trainer Personal Profile
* Trainer Reads Assigned Member Health Records
* Trainer Creates MealPlan & Workout for Assigned Member

* Trainer Creates Workout Details
* Trainer Read Workout Details
* Trainer Updates Workout Details
* Trainer Delete Workout Details

* Trainer Creates Meal Plan
* Trainer Read Meal Plan
* Trainer Updates Meal Plan
* Trainer Delete Meal Plan

## Admin Use Cases:

* Admin Create Subscription 
* Admin Read Subscription
* Admin Update Subscription
* Admin Delete Subscription

* Admin Read Member Health Record Details
* Admin Read Trainer Details
* Admin Create Trainer Member Assignment

## Login Information 

| Role  | Email| Password|
| ----- | ------------- |------------- |
| Admin | admin  | admin |
| Member | abc@def.com | 2wsxz |
| Trainer | xyz@def.com | 12345 |

## Relational Schema

![GitHub Logo](/images/FitnessTraining_RelationalDiagram.png)
