CREATE TABLE Table_info
(
  Table_Name VARCHAR(200) NOT NULL,
  Table_id INT NOT NULL,
  No_of_Fragments INT NOT NULL,
  Fragmentation_type enum('VF','DHF','HF') NOT NULL,
  No_of_Columns INT NOT NULL,
  PRIMARY KEY (Table_id)
);

CREATE TABLE Sites
(
  id INT NOT NULL,
  ip VARCHAR(200) NOT NULL,
  passoword VARCHAR(200) NOT NULL,
  username VARCHAR(200) NOT NULL,
  databasename VARCHAR(200) NOT NULL,
  DatabaseType VARCHAR(200) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE fragmentted_table
(
  fragment_name VARCHAR(200) NOT NULL,
  fragment_id INT NOT NULL,
  frag_condition VARCHAR(200) NOT NULL,
  Table_id INT NOT NULL,
  PRIMARY KEY (fragment_id),
  FOREIGN KEY (Table_id) REFERENCES Table_info(Table_id)
);

CREATE TABLE column_info
(
  Column_name VARCHAR(200) NOT NULL,
  NULL_col enum('NO','YES') NOT NULL,
  Extras VARCHAR(200),
  Default_col VARCHAR(200),
  Data_type_col VARCHAR(100) NOT NULL,
  Key_col enum('PRI','UNI','NONE'),
  Table_id INT NOT NULL,
  PRIMARY KEY (Column_name, Table_id),
  FOREIGN KEY (Table_id) REFERENCES Table_info(Table_id)
);

CREATE TABLE Allocation
(
  fragment_id INT NOT NULL,
  site_id INT NOT NULL,
  PRIMARY KEY (fragment_id, site_id),
  FOREIGN KEY (fragment_id) REFERENCES fragmentted_table(fragment_id),
  FOREIGN KEY (site_id) REFERENCES Sites(id)
);