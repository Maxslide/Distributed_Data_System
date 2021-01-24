
CREATE TABLE Course_Offered1
(
  Course_Code INT NOT NULL,
  Course_Name VARCHAR(100) NOT NULL,
  CourseType enum('CSE','ECE','HSME') NOT NULL,
  Credits INT NOT NULL,
  PRIMARY KEY (Course_Code),
  UNIQUE (Course_Name)
);

CREATE TABLE teaches1
(
  Faculty_Id INT NOT NULL,
  Course_Code INT NOT NULL,
  PRIMARY KEY (Faculty_Id, Course_Code),
  FOREIGN KEY (Faculty_Id) REFERENCES Faculty1(Faculty_Id),
  FOREIGN KEY (Course_Code) REFERENCES Course_Offered1(Course_Code)
);

CREATE TABLE Opts1
(
  Grade INT NOT NULL,
  Roll_No INT NOT NULL,
  Course_Code INT NOT NULL,
  PRIMARY KEY (Roll_No, Course_Code),
  FOREIGN KEY (Roll_No) REFERENCES Student_Info1(Roll_No),
  FOREIGN KEY (Course_Code) REFERENCES Course_Offered1(Course_Code)
);

CREATE TABLE BTP_IS_Hon1
(
  Proj_Type enum('BTP','IS','Hon') NOT NULL,
  Grade INT NOT NULL,
  Project_Info VARCHAR(300) NOT NULL,
  Roll_No INT NOT NULL,
  Faculty_Id INT NOT NULL,
  PRIMARY KEY (Roll_No, Faculty_Id),
  FOREIGN KEY (Roll_No) REFERENCES Student_Info1(Roll_No),
  FOREIGN KEY (Faculty_Id) REFERENCES Faculty1(Faculty_Id)
);


CREATE TABLE Course_Offered_Prerequisite1
(
  Prerequisite VARCHAR(100) NOT NULL,
  Course_Code INT NOT NULL,
  PRIMARY KEY (Prerequisite, Course_Code),
  FOREIGN KEY (Course_Code) REFERENCES Course_Offered1(Course_Code)
);

CREATE TABLE Student_Info1
(
  Roll_No INT NOT NULL,
  Branch enum('CSE','ECE','CSD','CLD','CND','ECD','CHD') NOT NULL,
  email_id VARCHAR(100) NOT NULL,
  CGPA FLOAT NOT NULL,
  PRIMARY KEY (Roll_No),
  UNIQUE (email_id)
);

CREATE TABLE Faculty1
(
  Faculty_Id INT NOT NULL,
  email_id VARCHAR(200) NOT NULL,
  Lab_Centre VARCHAR(100) NOT NULL,
  PhNo VARCHAR(20) NOT NULL,
  PRIMARY KEY (Faculty_Id),
  UNIQUE (email_id)
);
