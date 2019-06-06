# Item Catalog - Introduction of cryptocurrencies

A simple web application that provides a list of items within a variety of categories and integrate google oauth2 user registration and authentication. Local permission system is implmented for only authenticated users having the ability to post, edit, and delete their own items.

## Prerequisites

- Python 3
- Vagrant
- VirtualBox
- SQLalchemy
- flask framework

## Set Up

- Clone the [fullstack-nanodegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm).
- Look for the _catalog_ folder and replace it with the contents of this respository.

## Usage

Launch the Vagrant VM from inside the _vagrant_ folder with:

`vagrant up`

Then access the shell with:

`vagrant ssh`

Then move inside the catalog folder:

`cd /vagrant/catalog`

Initialize the database
`python database_setup.py`

Populate the database with some initial data
`python lots_of_items.py`

Then run the application:

`python project.py`

After the last command you are able to browse the application at this URL:

`http://localhost:8000/`

## JSON endpoints

Return JSON of all catalogs

`/catalog/JSON`

Return JSON of specific item

`/catalog/<string:catalogName>/<string:itemName>/JSON`

Return JSON of items for a specific catalog

`/catalog/<string:catalogName>/items/JSON`
