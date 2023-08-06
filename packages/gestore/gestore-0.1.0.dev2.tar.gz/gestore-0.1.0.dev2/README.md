# gestore
Django object management

> “gestore” just means “manager” in Italian.

A set of tools that will help you to 
- Export objects and all other objects related to it. 
- Import exported objects back.
- Delete objects and all other objects related to it entirely from database.


> **Note**
> 
> Object Import/Delete are not production ready. Use with caution

## Why using this tool
This idea came out of Appsembler Multi Cluster UI/UX Workflows.This tool is 
very useful for supporting multiple clusters, there are other reasons why 
having robust Export/Import/Delete functionality on your app would be highly 
beneficial:
- Frees your site from lots of data you are not using. It's a great idea to
  export such data to a file system which can be imported later.
- Decreases the overhead for data tools.
- Removes old data, to keep your costs down and improve performance 
  of aggregation functions (e.g. data pipelines)
- Deletes old objects as customers churn.
- Data export is very useful for GDPR reasons
- Some customers want their data now for DR (disaster recovery) reasons, not 
  because they’re churning.
- If you are strongly motivated to create a separate cluster for data that 
  already exists on a current one.
- Lowers the risk of objects (e.g. trial users) being able to crack 
  your site isolation and access data from paying customers.


## Get started

Not implemented yet

## How it works?
This tool uses BFS to explore all objects in the DB from the given one. In the
following GIF, let's assume you want to export object number 3, gestore will 
fetch its data and process all the objects its connected to, so that when you
import them back again, data will be fully functional
![Breadth first search animation](https://media.giphy.com/media/v6P6CSXDAthrRA4ZHi/giphy.gif)


### Export functionality
This will help you exporting all object-related data once triggered. For every 
model being processed, we get its data, and the data of its keys; (Foreign, 
ManyToMany, OneToOne) until we reach a base model that's not connected to any 
other model. If the key of any of these related fields is None, then we hit a 
leaf node.

We use a BFS technique to scrape data element by element from the database 
until we hit a leaf node that doesn't have any relations. For each processed 
object, we store its data, and add its children's data.


#### Command Usage

```shell
python manage.py exportobjects [-d] [-o OUTPUT] objects
```
Objects is a list of objects to be exported. Each of these arguments must match
the following syntax: `<app_id>.<Model>.<object_id>`

##### Example
```shell
python manage.py exportobjects auth.User.10 demoapp.Book.4 -o /path/to/exp.json
```

#### Command Arguments

- `objects`. The main argument of the `exportobjects`. Its representation is
  described above.
- `--debug` flag is optional, use it to prevent any file writing. This is 
  helpful in case you want to see the JSON output of the data before writining
  it on your system.
- `--output` is an optional argument that takes a path string of the location 
  in which you want to store the exprts file.
  

### Import functionality

- Will not commit changes if something went wrong


#### Command Usage

```shell
python manage.py importobjects [-d] [-o] path
```

##### Example
```shell
python manage.py importobjects /path/to/exp.json
```

#### Command Arguments

- `path`. The main argument of the `importobjects`. It should point to an
  export file on you local system.
- `--debug` performs a dry run. Will not commit or save any changes to the DB.
- `--override` DANGEROUS. A flag that will tell the command to override objects
  in the DB with the ones being imported in case of a conflict.


### Delete functionality
Not implemented yet.

### Demo app
This app is created for the sole purpose of testing and visualising the manager
commands in action. No other functionality is expected out of this app.


## Challenges
- **Platform state**: When exporting data from your project, it's assumed that
  importing it back will take place in the same project with the same 
  datastructures. If you upgrade a library that you're using its models, and 
  these models were changed (fields removed, added, type changed) you are going
  to face some problems.
- **Object conflicts** 
  - Some data like _usernames_ are unique cluster wide, if we’re importing 
    such data from another cluster, some could be duplicated or overridden.
  - Some exported objects might have a similar ID to a totally different object
    in the database, this tool will flag these objects for you so you know what
    to change and what to override.

## Reporting Security Issues
Please do not report security issues in public. Email us 
on security@appsembler.com.
