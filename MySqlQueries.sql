CREATE TABLE MemberDetails
(
  MemberID INT NOT NULL auto_increment,
  MemberName VARCHAR(50) NOT NULL,
  MemberEmail VARCHAR(100) NOT NULL,
  MemberPassword VARCHAR(50) NOT NULL,
  MemberAddress VARCHAR(250) NOT NULL,
  PRIMARY KEY (MemberID)
);

CREATE TABLE MealPlanDetails
(
  MealPlanID INT NOT NULL auto_increment,
  MealPlanName VARCHAR(250) NOT NULL,
  NoOfDaysMealPlan INT NOT NULL,
  MealPlanDescription VARCHAR(500) NOT NULL,
  PRIMARY KEY (MealPlanID)
);

CREATE TABLE SubscriptionDetails
(
  SubscriptionID INT NOT NULL auto_increment,
  SubscriptionName VARCHAR(100) NOT NULL,
  SubscriptionType VARCHAR(100) NOT NULL,
  SubscriptionPrice NUMERIC(11,2) NOT NULL,
  NoOfDaysSubcription INT NOT NULL,
  PRIMARY KEY (SubscriptionID)
);

CREATE TABLE WorkoutDetails
(
  WorkoutID INT NOT NULL auto_increment,
  WorkoutName VARCHAR(250) NOT NULL,
  WorkoutType VARCHAR(250) NOT NULL,
  WorkoutTimeTotalHours INT NOT NULL,
  NoOfDaysWorkout INT NOT NULL,
  PRIMARY KEY (WorkoutID)
);

CREATE TABLE MemberHealthRecords
(
  MemberHealthRecordID INT NOT NULL auto_increment,
  MemberAge INT NOT NULL,
  MemberHeight NUMERIC(11,2) NOT NULL,
  MemberWeight NUMERIC(11,2) NOT NULL,
  MemberProfession VARCHAR(250) NOT NULL,
  MemberMedicalAilments VARCHAR(250) NOT NULL,
  MemberBMI VARCHAR(250) NOT NULL,
  MemberGender VARCHAR(10) NOT NULL,
  MemberID INT NOT NULL,
  MealPlanID INT NOT NULL,
  SubscriptionID INT NOT NULL,
  WorkoutID INT NOT NULL,
  PRIMARY KEY (MemberHealthRecordID),
  FOREIGN KEY (MemberID) REFERENCES MemberDetails(MemberID),
  FOREIGN KEY (MealPlanID) REFERENCES MealPlanDetails(MealPlanID),
  FOREIGN KEY (SubscriptionID) REFERENCES SubscriptionDetails(SubscriptionID),
  FOREIGN KEY (WorkoutID) REFERENCES WorkoutDetails(WorkoutID)
);

CREATE TABLE TrainerDetails
(
  TrainerID INT NOT NULL auto_increment,
  TrainerName VARCHAR(100) NOT NULL,
  TrainerEmail VARCHAR(100) NOT NULL,
  TrainerPassword VARCHAR(50) NOT NULL,
  TrainerYrsOfExperience INT NOT NULL,
  TrainerGender VARCHAR(10) NOT NULL,
  PRIMARY KEY (TrainerID)
);

CREATE TABLE TrainerAssignmentDetails
(
  TrainerAssignmentID INT NOT NULL auto_increment,
  TrainerID INT NOT NULL,
  MemberID INT NOT NULL,
  PRIMARY KEY (TrainerAssignmentID),
  FOREIGN KEY (TrainerID) REFERENCES TrainerDetails(TrainerID),
  FOREIGN KEY (MemberID) REFERENCES MemberDetails(MemberID)
);