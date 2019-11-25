use dbmaster;
drop table if exists q2_table;

create table q2_table (
	    uid bigint(20),
	    value longtext
);

LOAD DATA LOCAL INFILE '~/q2one.csv' INTO TABLE q2_table FIELDS TERMINATED BY '\t'
 ENCLOSED BY '"' LINES TERMINATED BY '\n';

create unique index uid_index on q2_table(uid);
