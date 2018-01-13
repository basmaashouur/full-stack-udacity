# Item Catalog Application

By Basma Ashour, in fulfillment of Udacity's [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)

## About
This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates categories and their items. 
OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

### Pre-Requirements
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Setup
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
4. Launch the Vagrant VM (`vagrant up`)
5. Log into Vagrant VM (`vagrant ssh`)
6. Navigate to `cd/vagrant` as instructed in terminal
7. Setup application database `python /project4/dbsetup.py`
8. *Insert fake data `python /project4/fill.py`
9. Run application using `python /project4/app.py`
10. Access the application locally using http://localhost:8000


## JSON Endpoints
The following are open to the public:

Catalog JSON: `/catalog/JSON`
    - Displays the whole Categories.

Category Items JSON: `/catalog/<int:category_id>/items/JSON/`
    - Displays items for a specific category

Category Item JSON: `/catalog/<int:category_id>/<int:item_id>/JSON/`
    - Displays a specific category item.
