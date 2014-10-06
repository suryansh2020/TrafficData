# Not meant to be run, this is just a reminder for Mariadb

# start & stop mariadb service
sudo systemctl stop mariadb.service
sudo systemctl start mariadb.service

# login
mysql -u root -p

# check status of mariadb service
service mariadb status

## further references
#https://mariadb.com/kb/en/mariadb/documentation/getting-started/a-mariadb-primer/a-mariadb-primer-02-logging-in/
# https://ask.fedoraproject.org/en/question/43459/how-to-start-mysql-mysql-isnt-starting/
