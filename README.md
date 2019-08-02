# Slangeuib REST API

## Installation
* Install [python 3.7](https://www.python.org/downloads/release/python-372/)
* Install MongoDb 
  * [Windows](https://www.mongodb.com/dr/fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-4.0.11-signed.msi/download)
  * [Ubuntu 18.04](https://www.mongodb.com/dr/repo.mongodb.org/apt/ubuntu/dists/bionic/mongodb-org/4.0/multiverse/binary-amd64/mongodb-org-server_4.0.11_amd64.deb/download)
  * [MacOs](https://www.mongodb.com/dr/fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-4.0.11.tgz/download)
  * [Other](https://www.mongodb.com/download-center/community)
* Ensure python and pip is installed and in PATH
* Install `pipenv`
  * Windows: `py -m pip install pipenv`
  * Unix: `python3 -m pip install pipenv`
* Navigate to root of project (running dir/ls should show Pipfile)
* Install server `pipenv install`
* Start server 
  * For production `pipenv run production`
  * For development `pipenv run start`


## Usage
---
`/api/v1/dropdown`  
`/api/v1/multi_choice`  
`/api/v1/fill_in`  
### GET
Get to any of the 3 endpoints will return all questions of that type.  


### POST
Adds a question to any of the endpoints.  There is a type lock on all of them to 
prevent sending wrong types and fields.

### PUT
Changes one or more questions by providing a body with a old and new field.  e.g:
```json
{
    "old": {
        "_id": "someid"
    },
    "new": {
        "question_text": "the new value for question_text to given id"
    }
}
```
Any fields can be used in both old and new to select one or multiple questions, and edit multiple fields.

---
Other endpoints are:  

---
`/api/v1/dropdown/<id>`  
`/api/v1/multi_choice/<id>`  
`/api/v1/fill_in/<id>` 

Available methods: **GET** & **DELETE**

---

`/api/v1/dropdown/set/<limit>`  
`/api/v1/multi_choice/set/<limit>`  
`/api/v1/fill_in/set/<limit>` 

Available methods: **GET**  

These endpoints also support queries for filtering questions.  
**Example:**  
`GET /api/v1/dropdown/set/2?difficulty=2`  

Support multiple queries  
**Example:**  
`GET /api/v1/dropdown/set/2?difficulty=2&tags=loops

Support lists in queries by seperating with `,`  
**Example:**  
`GET /api/v1/dropdown/set/2tags=loops,operators`