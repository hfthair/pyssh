set names 'utf8mb4';

use dbmaster;

drop table if exists q3_table;

create table q3_table (
    user_id bigint(20), 
    tweet_id char(30), 
    created_at bigint(15), 
    tweet_text text,
    score int
) character set 'utf8mb4' collate 'utf8mb4_unicode_ci';

LOAD DATA LOCAL INFILE '~/q3one.csv' INTO TABLE q3_table FIELDS TERMINATED BY '\t' ENCLOSED BY '"' LINES TERMINATED BY '\n';

create index q3_index on q3_table(user_id, created_at);
