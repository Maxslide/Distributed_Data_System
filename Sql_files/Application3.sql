CREATE TABLE Course_Offered3
(
  Course_Code INT NOT NULL,
  Course_Name VARCHAR(100) NOT NULL,
  CourseType enum('CSE','ECE','HSME') NOT NULL,
  Credits INT NOT NULL,
  PRIMARY KEY (Course_Code),
  UNIQUE (Course_Name)
);

CREATE TABLE Student_Info3
(
  Roll_No INT NOT NULL,
  First_Name VARCHAR(100) NOT NULL,
  Last_Name VARCHAR(100) NOT NULL,
  Gender enum('MALE','FEMALE','OTHERS') NOT NULL,
  PRIMARY KEY (Roll_No)
);

CREATE TABLE Faculty3
(
  Faculty_Id INT NOT NULL,
  PRIMARY KEY (Faculty_Id)
);

CREATE TABLE teaches3
(
  Faculty_Id INT NOT NULL,
  Course_Code INT NOT NULL,
  PRIMARY KEY (Faculty_Id, Course_Code),
  FOREIGN KEY (Faculty_Id) REFERENCES Faculty3(Faculty_Id),
  FOREIGN KEY (Course_Code) REFERENCES Course_Offered3(Course_Code)
);

CREATE TABLE Opts3
(
  Grade INT NOT NULL,
  Roll_No INT NOT NULL,
  Course_Code INT NOT NULL,
  PRIMARY KEY (Roll_No, Course_Code),
  FOREIGN KEY (Roll_No) REFERENCES Student_Info3(Roll_No),
  FOREIGN KEY (Course_Code) REFERENCES Course_Offered3(Course_Code)
);

CREATE TABLE BTP_IS_Hon3
(
  Proj_Typessh enum('BTP','IS','Hon') NOT NULL,
  Grade INT NOT NULL,
  Project_Info VARCHAR(300) NOT NULL,
  Roll_No INT NOT NULL,
  Faculty_Id INT NOT NULL,
  PRIMARY KEY (Roll_No, Faculty_Id),
  FOREIGN KEY (Roll_No) REFERENCES Student_Info3(Roll_No),
  FOREIGN KEY (Faculty_Id) REFERENCES Faculty3(Faculty_Id)
);

CREATE TABLE Faculty_Qualification3
(
  Qualification VARCHAR(100) NOT NULL,
  Faculty_Id INT NOT NULL,
  PRIMARY KEY (Qualification, Faculty_Id),
  FOREIGN KEY (Faculty_Id) REFERENCES Faculty3(Faculty_Id)
);

CREATE TABLE Course_Offered_Prerequisite3
(
  Prerequisite VARCHAR(100) NOT NULL,
  Course_Code INT NOT NULL,
  PRIMARY KEY (Prerequisite, Course_Code),
  FOREIGN KEY (Course_Code) REFERENCES Course_Offered3(Course_Code)
);
