# Slangeuib REST API

## Installation
### Docker
* Install docker
* Install docker-compose
* Set environment variable for `API_KEY`
* Run `docker-compose up`  

--------
### Manual
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
* Setup an environment variable for `API_KEY` which communicating services need in an Authorization: token \<key\> header
* Start server 
  * For production `pipenv run production`
  * For development `pipenv run start`
* Remember to populate the database.

## Usage
---
### Specific question types
3 question types, each have their own endpoint for micromanagment.
`/api/v1/dropdown`  
`/api/v1/multichoice`  
`/api/v1/fillin`  
#### GET
Get to any of the 3 endpoints will return all questions of that type.  


#### POST
**Requires Authorization**  
Adds a question to any of the endpoints.  There is a type lock on all of them to 
prevent sending wrong types and fields.

#### PUT
**Requires Authorization**  
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
### By id
The id let's you get or delete a specific question
`/api/v1/dropdown/<id>`  
`/api/v1/multi_choice/<id>`  
`/api/v1/fill_in/<id>` 

#### GET
Returns the question that matches the id

#### DELETE
**Requires Authorization**  
Deletes the question with the matching id

---

### Sets
Return a set of a specific question type, with a limit.  
`/api/v1/dropdown/set/<limit>`  
`/api/v1/multi_choice/set/<limit>`  
`/api/v1/fill_in/set/<limit>` 

#### GET
Returns a list of questions.  The limit decides how many entires the list contains.  
Specifying a limit higher than available questions will error.  The list is randomized.


These endpoints also support queries for filtering questions.  
**Example:**  
`GET /api/v1/dropdown/set/2?difficulty=2`  

Support multiple queries  
**Example:**  
`GET /api/v1/dropdown/set/2?difficulty=2&tags=loops`

Support lists in queries by seperating with `,`  
**Example:**  
`GET /api/v1/dropdown/set/2tags=loops,operators`


### Questions endpoint
This is the main endpoint for getting question sets.
It uses queries to determine how many of each question type is requested

`/api/v1/questions`  

#### GET
**Example:**
`GET /api/v1/questions?dropdown=2&multichoice=1`  

This will request a set of 2 random dropdown questions and 1 multichoice question.

This endpoint also support filter queries.

**Example:**
`GET /api/v1/questions/?dropdown=3&tags=loops,lists&difficulty=3`

This will return a set of 3 dropdown questions that contain either loops or lists, with a difficulty of 3.  Multiple tags only increase what to look for, it's not an `and this` look up.

#### POST
**Requires Authorization**  

Same as posting to the specific question endpoint, but requires that you specify which type of question it is with the `type` field


`api/v1/questions/:id`

#### DELETE
Same as deleting to a specific endpoint, but since the ids are unique you dont have to specify type with this.

### Feedback
---
`/api/v1/feedback`

#### GET
Gets all feedback

#### PUT
Edit feedback

#### POST
Post a new feedback


`/api/v1/feedback/:id`
#### GET 
Get a specific feedback object

#### DELETE
Deletes a specific feedback


`/api/v1/question_feedback`
#### GET
gets all question feedbacks

#### POST
posts a new set of feedbacks for a question


`/api/v1/question_feedback/set`
#### POST
Returns a list of feedbacks for a list of questions.
Only takes a list of question ids


### Data
---
`/api/v1/data`

#### GET
Gets all data

#### PUT
Edit data

#### POST
Post a new data entry


`/api/v1/dataset`
#### POST
posts a list of data entries for batch processing

#### DELETE
DELETES THE ENTIRE TABLE.