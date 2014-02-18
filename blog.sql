CREATE DATABASE IF NOT EXISTS compSciConferenceDB;
GRANT ALL PRIVILEGES ON compSciConferenceDB.* to 'blogUser'@'localhost' 
identified by 'blogPassword';
USE compSciConferenceDB;

CREATE TABLE conferences
(
  conference_id INT NOT NULL AUTO_INCREMENT,
  conference_name VARCHAR(175) NOT NULL,
  acronym VARCHAR(20) default NULL,
  district VARCHAR(25) default NULL,
  country VARCHAR(25) default NULL,
  venue VARCHAR(100) default NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  PRIMARY KEY(conference_id)
);

INSERT INTO conferences VALUES (NULL, 'International Conference on Information Communication and Embedded Systems', 'ICICES', 'Madras', 'India', 'The S.A. Engineering College (SAEC) Campus', '2014-02-27', '2014-02-28');
