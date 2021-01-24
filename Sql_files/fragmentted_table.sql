INSERT INTO fragmentted_table 
VALUES ('Course_Offered1', 1, ' CourseType = "CSE" ', 2);
INSERT INTO fragmentted_table 
VALUES ('Course_Offered2', 2, ' CourseType = "ECE" ', 2);
INSERT INTO fragmentted_table 
VALUES ('Course_Offered3', 3, ' CourseType = "HSME" ', 2);

INSERT INTO fragmentted_table 
VALUES ('Course_Offered_Prerequisite1', 4, ' Course_Offered.CourseType(Course_Offered_Prerequisite.Course_Code) = "CSE" ', 3);
INSERT INTO fragmentted_table 
VALUES ('Course_Offered_Prerequisite2', 5, ' Course_Offered.CourseType(Course_Offered_Prerequisite.Course_Code) = "ECE" ', 3);
INSERT INTO fragmentted_table 
VALUES ('Course_Offered_Prerequisite3', 6, ' Course_Offered.CourseType(Course_Offered_Prerequisite.Course_Code) = "HSME" ', 3);

INSERT INTO fragmentted_table 
VALUES ('teaches1', 7, ' Course_Offered.CourseType(teaches.Course_Code) = "CSE" ', 7);
INSERT INTO fragmentted_table 
VALUES ('teaches2', 8, ' Course_Offered.CourseType(teaches.Course_Code) = "ECE" ', 7);
INSERT INTO fragmentted_table 
VALUES ('teaches3', 9, ' Course_Offered.CourseType(teaches.Course_Code) = "HSME" ', 7);

INSERT INTO fragmentted_table 
VALUES ('Opts1', 10, ' Course_Offered.CourseType(Opts.Course_Code) = "CSE" ', 6);
INSERT INTO fragmentted_table 
VALUES ('Opts2', 11, ' Course_Offered.CourseType(Opts.Course_Code) = "ECE" ', 6);
INSERT INTO fragmentted_table 
VALUES ('Opts3', 12, ' Course_Offered.CourseType(Opts.Course_Code) = "HSME" ', 6);

INSERT INTO fragmentted_table 
VALUES ('Faculty1', 13, 'Faculty_Id email_id Lab_center,PhNo', 4);
INSERT INTO fragmentted_table 
VALUES ('Faculty2', 14, ' Faculty_Id First_Name Last_Name Gender ', 4);
INSERT INTO fragmentted_table 
VALUES ('Faculty3', 15, ' Faculty_Id ', 4);

INSERT INTO fragmentted_table 
VALUES ('Student_info1', 16, ' Roll_No Branch email_id CGPA ', 1);
INSERT INTO fragmentted_table 
VALUES ('Student_info2', 17, ' Roll_No DOB DOJ PhNo ', 1);
INSERT INTO fragmentted_table 
VALUES ('Student_info3', 18, ' Roll_No First_Name Last_Name Gender ', 1);

INSERT INTO fragmentted_table 
VALUES ('BTP_IS_Hon1', 19, ' Proj_Type = "BTP" ', 8);
INSERT INTO fragmentted_table 
VALUES ('BTP_IS_Hon2', 20, ' Proj_Type = "IS" ', 8);
INSERT INTO fragmentted_table 
VALUES ('BTP_IS_Hon3', 21, ' Proj_Type = "Hon" ', 8);

INSERT INTO fragmentted_table 
VALUES ('Faculty_Qualification3', 22, ' Faculty_Id ', 5);