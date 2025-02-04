# Скрипт пересоздания базы данных
export PGPASSWORD=admin
psql --host 127.0.0.1 -p 5432 -U postgres -d test -c "drop database app"
psql --host 127.0.0.1 -p 5432 -U postgres -d test -c "create database app" 