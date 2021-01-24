CREATE TABLE Course_Offered2
(
  Course_Code INT NOT NULL,
  Course_Name VARCHAR(100) NOT NULL,
  CourseType enum('CSE','ECE','HSME') NOT NULL,
  Credits INT NOT NULL,
  PRIMARY KEY (Course_Code),
  UNIQUE (Course_Name)
);

CREATE TABLE teaches2
(
  Faculty_Id INT NOT NULL,
  Course_Code INT NOT NULL,
  PRIMARY KEY (Faculty_Id, Course_Code),
  FOREIGN KEY (Faculty_Id) REFERENCES Faculty2(Faculty_Id),
  FOREIGN KEY (Course_Code) REFERENCES Course_Offered2(Course_Code)
);

CREATE TABLE Opts2
(
  Grade INT NOT NULL,
  Roll_No INT NOT NULL,
  Course_Code INT NOT NULL,
  PRIMARY KEY (Roll_No, Course_Code),
  FOREIGN KEY (Roll_No) REFERENCES Student_Info2(Roll_No),
  FOREIGN KEY (Course_Code) REFERENCES Course_Offered2(Course_Code)
);

CREATE TABLE BTP_IS_Hon2
(
  Proj_Type enum('BTP','IS','Hon') NOT NULL,
  Grade INT NOT NULL,
  Project_Info VARCHAR(300) NOT NULL,
  Roll_No INT NOT NULL,
  Faculty_Id INT NOT NULL,
  PRIMARY KEY (Roll_No, Faculty_Id),
  FOREIGN KEY (Roll_No) REFERENCES Student_Info2(Roll_No),
  FOREIGN KEY (Faculty_Id) REFERENCES Faculty2(Faculty_Id)
);


CREATE TABLE Course_Offered_Prerequisite2
(
  Prerequisite VARCHAR(100) NOT NULL,
  Course_Code INT NOT NULL,
  PRIMARY KEY (Prerequisite, Course_Code),
  FOREIGN KEY (Course_Code) REFERENCES Course_Offered2(Course_Code)
);

CREATE TABLE Student_Info2
(
  Roll_No INT NOT NULL,
  DOB DATE NOT NULL,
  DOJ DATE NOT NULL,
  PhNo VARCHAR(20) NOT NULL,
  PRIMARY KEY (Roll_No)
);

CREATE TABLE Faculty2
(
  Faculty_Id INT NOT NULL,
  First_Name VARCHAR(100) NOT NULL,
  Last_Name VARCHAR(100) NOT NULL,
  Gender enum('MALE','FEMALE','OTHERS') NOT NULL,
  PRIMARY KEY (Faculty_Id)
);

