# install

    docker run --name db -e POSTGRES_PASSWORD=123 -d -p 5432:5432 postgres:latest
	-----
    docker exec -it -u postgres db psql
	-----
    create table datatable2 (
    numerical serial primary key not null,
    id int not null,
    name text not null, 
    date date not null,
    point int,
    timein time,
    timeout time,
    state int,
    timelate time,
    timeearly time);
    -----
    create table usertable (
    uid int primary key not null,
    id int not null,
    name text not null, 
    privilege text,
    password text,
    groupid text);

----------

    sudo pip install flask 
    sudo pip install wtforms
    sudo pip install psycopg2
    sudo pip install psycopg2-binary


----------

