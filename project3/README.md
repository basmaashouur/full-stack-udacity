# Logs Analysis 

By Basma Ashour, in fulfillment of Udacity's [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)

### About

This project is a tool for reporting some queries in a large database with over milion rows.
The tool runs three queries for answering to the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### Pre-Requirements

1. Python 3
2. Vagrant
3. VirtualBox

### Setup

1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)<br>
2. Download or clone from github [fullstack-nandegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm)</br>
3. Clone this repository


### Run

1. From the 'vagrant' directory, run ```vagrant up```
2. SSH to the virtual machine with ```vagrant ssh``` Load the data with ``` psql -d news -f newsdata.sql ```
3. Connect to the psql database with ```psql -d news```
