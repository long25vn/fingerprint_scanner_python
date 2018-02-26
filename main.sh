docker run --name db -e POSTGRES_PASSWORD=123 -d -p 5432:5432 postgres:latest
docker exec -it -u postgres db psql
sudo pip install flask 
sudo pip install wtforms
sudo pip install psycopg2
sudo pip install psycopg2-binary
