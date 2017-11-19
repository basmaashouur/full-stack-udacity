# Logs Analysis 

By Basma Ashour, in fulfillment of Udacity's [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)

### About

This project is a tool for reporting some queries in a large database with over milion rows.
The tool runs three queries for answering to the following questions:
- What are the most popular three articles of all time?
- Who are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

### Pre-Requirements

- Python 3
- Vagrant
- VirtualBox

### Setup 

- Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)<br>
- Download or clone from github [fullstack-nandegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm)</br>
- Clone this reposit''ory
- Download psql database news [Download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

### Creating views

1. Create tables oviews and nviews.
```
CREATE VIEW oviews AS
SELECT time::date AS day, count(*) AS stat
FROM log
WHERE status != '200 OK'
GROUP BY day
ORDER BY day DESC;

CREATE VIEW nviews AS
SELECT time::date AS day, count(*) AS stat
FROM log
WHERE status = '200 OK'
GROUP BY day
ORDER BY day DESC;
```
 
### Run

- From the 'vagrant' directory, run ```vagrant up```
- SSH to the virtual machine with ```vagrant ssh``` Load the data with ``` psql -d news -f newsdata.sql ```
- Connect to the psql database with ```psql -d news```
- Run the ``` creating views```
- Run logs.py using ``` python3 logs.py ```
