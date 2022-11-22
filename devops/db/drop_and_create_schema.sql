DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- create rds admin user en postgres admin
create user rdsadmin;
create user postgres;

GRANT ALL PRIVILEGES ON DATABASE dbsentitweet to rdsadmin;
GRANT ALL PRIVILEGES ON DATABASE dbsentitweet to postgres;