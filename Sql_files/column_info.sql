-- column_name, NULL_col , Extras, Default_col, Data_type_col, Key_col, Table_id
insert into column_info values ('DOB', 'NO', '', 'NULL', 'DATE', 'NONE', 1);
insert into column_info values ('DOJ', 'NO', '', 'NULL', 'DATE', 'NONE', 1);

INSERT INTO column_info VALUES ('Course_Code','NO', '', 'NULL','INT', 'PRI',2);
INSERT INTO column_info VALUES ('Course_Name','NO', '', 'NULL','VARCHAR(100)', 'UNI',2);

INSERT INTO column_info VALUES ( 'Faculty_Id', 'NO', '', 'NULL','INT', 'PRI',4);
INSERT INTO column_info VALUES ( 'First_Name', 'NO', '', 'NULL','VARCHAR(100)', 'NONE',4);