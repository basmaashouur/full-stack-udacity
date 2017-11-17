#Logs Analysis 

By Basma Ashour, in fulfillment of Udacity's [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)

### About

This project is a tool for reporting some queries in a large database with over milion rows.
The tool runs three reports for answers to the following questions:
- What are the most popular three articles of all time?
- Who are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

### Pre-Requirements
#### For Linux users
1. Python 3
2. PSQL
#### For windows and Mac users
1. Python 3
2. Vagrant
3. VirtualBox

### setup
#### For Linux users
1. 

First you must have the PostgreSQL newsdata.sql database running from the FSND virtual machine.

- From the 'vagrant' directory, run ```vagrant up```.
- SSH to the virtual machine with ```vagrant ssh```.
- Connect to the psql database with ```psql -d news```
