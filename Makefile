prod:
	apt-get update
	apt-get -y install -f python3-pip python3-dev libpq-dev postgresql postgresql-contrib
	pg_ctlcluster 11 main start
	su - postgres -c "psql -c \"CREATE DATABASE project_server\""
	su - postgres -c "psql -c \"CREATE USER project_server_user WITH PASSWORD 'server'\""
	su - postgres -c "psql -c \"ALTER ROLE project_server_user SET client_encoding TO 'utf8'\""
	su - postgres -c "psql -c \"ALTER ROLE project_server_user SET default_transaction_isolation TO 'read committed'\""
	su - postgres -c "psql -c \"ALTER ROLE project_server_user SET timezone TO 'UTC'\""
	su - postgres -c "psql -c \"ALTER USER project_server_user CREATEDB\""
	su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE project_server TO project_server_user\""
	apt-get -y install -f pipenv
	pipenv install --system
	python manage.py makemigrations
	python manage.py migrate