# AI-clinic Python Developer Tech task

This is my solution to the tech task which is a part of Python Developer Tech task Automation position evaluation.

## Task Description

The task is to create a REST API using Python frameworks:
1. Download and install the laatest version of Python - https://www.python.org/downloads/
2. Download this repository either by using <code>git clone</code>, or just download it as a zip file
3. In your terminal, go to the folder to which this project was downloaded
4. In your terminal, type this commands:
    * <code>python -m venv venv</code>
    * <code>venv\scripts\activate</code>
    * <code>pip install -r requiremenets.txt</code>
    * <code>python manager.py makemigrations polls</code>
    * <code>python manager.py migrate</code>
    * <code>python manager.py runserver</code>

5. Type in your browser https://127.0.0.1:8000. Now you should see a screen with an error message. In order to use the REST API, refer to the next section.

## API

| API path | Request method | Description
| --- | --- | --- |
/api/team | GET | List of all available teams
/api/team/:id | GET | Get a team by id
/api/team | POST | Add a new team
/api/team/:id| DELETE | Remove an existing team
/api/team/:team_id/member | GET | List of all members of a specific team
/api/team/:team_id/member/:member_id | POST | Add a new member to a team
/api/team/:team_id/member/:member_id | DELETE | Remove an existing member from a team
/api/member | GET | List of all available members
/api/member/:id | GET | Get a member by id
/api/member | POST | Add a new member
/api/member/:id| DELETE | Remove an existing member
/api/member/:member_id/manager | GET | Get a member`s manager by member id
/api/member/:member_id/manager/:manager_id | POST | Set a manager to a specific member
/api/member/:member_id/manager/:manager_id | DELETE | Set a member`s manager as null

## Restrictions

* You cannot have a two different teams with the same name.
* You cannot have a two different members with the same email.
* Any member can be added to the team only once.
* You cannot have a closed loop of managers, meaning, if A is a manager to B and B is a manager to C then this means that you can`t set C as a manager to A.