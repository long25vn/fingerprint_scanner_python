# fingerprint_scanner_python

# install
### install postgresql
    docker run --name db -e POSTGRES_PASSWORD=123 -d -p 5432:5432 postgres:latest
	-----
    docker exec -it -u postgres db psql [ docker exec -it -u postgres db psql] 
	-----
    create table datatable (
    numerical int primary key not null,
    id int not null,
    name text not null, 
    date date not null,
    point int,
    timein time,
    timeout time,
    state int,
    timelate time,
    timeearly time);


----------
### install flask
    sudo pip install flask 
    sudo pip install wtforms
    sudo pip install psycopg2 # đọc cở sở dữ liệu
    sudo pip install psycopg2-binary


----------
### chạy ứng dụng
    git clone https://github.com/long25vn/fingerprint_scanner_python.git
    cd fingerprint_scanner_python/
    python control.py & \
    python pushdata.py

file pushdata chạy liên tục để đẩy dữ liệu trên máy chấm công về cơ sở dữ liệu, file control.py đọc dữ liệu trong cơ sở dữ liệu và hiển thị.

