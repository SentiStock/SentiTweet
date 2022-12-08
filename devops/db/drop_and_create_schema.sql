DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- create postgres admin
create user postgres;

GRANT ALL PRIVILEGES ON DATABASE dbsentitweet to postgres;

ALTER ROLE postgres SUPERUSER;
