# Orbit Database - Introduction

#### Welcome to the Orbit Database repository and documentation. All project documentation is included within this repository and consists of markdown files and comments within the code. These are presented in real time by the "ZeroDocs" Orbit application which renders this content to HTML in real-time.

This project is the NoSQL database that underpins the Orbit Framework. The interface is written in Python3 and uses LMDB as it's back-end key/value store. Please don't be put off by the <i>written in Python</i> statement, the database performs well and in many cases surpasses what you might expect from a dedicated database engine such as MariaDB or Postgres. The software architecture looks like this;

<table><tr><td><img style="height:350px" src="https://gitlab.com/madpenguin/orbit-database/-/raw/main/images/orbit_database.png" /></td><td>
<h3 style="padding-left:1.4em">Primary design goals</h3>

* Must perform well in a Python multi-processing environment
* Must integrate well with Python based microservices
* Must be easy to deploy in a cloud environment
* Must be easily testable in a Python environment
* Must offer the same basic functionality as mainstream database engines
* Must facilitate efficient real-time triggers when data is changed
* Must be easy to replicate in real time
</td></tr></table>

Although these goals are entirely subjective, when compared to Python applications using traditional SQL databases, in general these goals have arguably been surpassed. If you are looking for a fast primary database to use in a native non-Python environment, then look elsewhere. If you need a database system with more capacity for use outside of Python, then consider Orbit-Database as a cache / real-time buffer between your 'real' database and each user's screen. If all you need is a read-speed of a few hundred thousand records a second, and an ACID write speed of 20,000 per second, look no further!

### Database Features

* Schemaless / NoSQL model, but with dynamic ORM system
* Database interface effectively reads and writes Python objects
* Secondary indexes can be created using any Python expression / function
* Secondary indexes support primary and duplicate variants
* The storage engine supports ACID Transactions
* Locking system enables massively parallel writing over many processes
* Super lightweight, pip installable Python3 library with no persistent server

This database has been around since 2017 and had gone through a number of incarnations to arrive at this point. It started life as a quick and dirty solution to a long running problem and has morphed into a relatively polished solution which is now the cornerstone of Orbit Communicator and the Orbit Framework.

### What does it look like?

As a basic example, if we wanted to have a database with a table called people, and within that table store records of individuals, we might have something like the following. We would start by setting up an ORM model for the table which consists of two classes. The first is uses to represent an individual, or a single records within the table, the second to represent a collection of individuals, or a collection of records.

```python
from orbit_orm import BaseTable, BaseCollection

class PeopleTable (BaseTable):
    norm_table_name = 'people'

class PeopleCollection (BaseCollection):
    table_class = PeopleTable
```

Once we have this, we can open up a database and start work on some data. When we open the database we need to tell it which ORM models we'll be using (PeopleCollection in this case) and the name of the database. At a basic level a PeopleCollection() object resolves to an iterator for the contents of the table. Iterators always yield a <i>result</i> object, which in turn contains a <i>doc</i> object, which is your record. (or Person in this instance)

```python
from orbit_database import OrbitDatabase
from schema.People import PeopleCollection

OrbitDatabase([PeopleCollection]).open('my_database')
for result in PeopleCollection():
    person = result.doc
    print(f'Name={person._name} Age={person._age}')
```

## Todo List (features)

* Deploy new indexing on OC + test - running - wip
* Write V2 conversion routine - wip

* Implement rename table in shell
* Implement rename index in shell


* Freelist management and compression for full-text indexcies
* Resting encryption for specific fields and raw blobs and words
* Better form of JSON for reading fields without deserialisation