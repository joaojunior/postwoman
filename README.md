# Assignment 1

## Background
The purpose of this assignment is to determine the basic problem solving and design skill of an
Algorithm engineer candidate.

## Our little story of dream
Jane studied software. But the job was completely indoor. So she became part time
postwoman. It’s exciting. She can visit different places every day in her town. Everyday she
goes to the post office to collect all the letters. And then she starts delivering them. She is not
like her colleagues who try to deliver as fast as possible. She wants to utilize this time to visit
different places. Hence she takes longer routes. Everytime she collects the posts from post
office, her boss suggests a route that she should use. She never follows that. Jane is quite
passionate about programming. She wants to automate the whole process. She want to visit
new places every now and then. If she can make it, she will sell this to her travel hungry
friends who have a similar job. Jane does not want to take too much time delivering her
packages since her boss will notice her inefficiency. Therefore, Jane doesn't mind if she
doesn't get to see everything on her first day.

## Expected Outcome
- It’s always better to start from designing the software
- A functional software that Jane can use to meet her travel hunger.
- Any question about the problem should be answered in assumptions.
- A full flexed service
- Surprise us!

# Assumptions
 - Jane does not return to PostOffice in the final of the day.
 - When exit from the PostOffice, the first place that Jane visit is always a place to deliver a letter.
 - Jane only can collect letters from 1 PostOffice.
 - Jane visit places within a `max_distance`. This valus is configured.
 - All places are consider with latitude and longitude and we will calculate the distance based on it.

# Idea
For resolve this problem, we will create an api that is possible input all the values and calculate the route for Jane.
We will create a database with 5 tables:
1) PostWoman: This table save the name of the postwoman, the postoffice that she will collect the letters and the value of `max_distance`(in km) to consider visit a place.
2) PostOffice: Table to save the name, latitude and longitute of the postoffice.
3) Letters: Table to save all the letters that the postwoman need to deliver.
4) PlaceToVisit: Table to save the places that the postwoman would like to visit.
5) RouteResult: Table to save the route and its total cost.

## API
The api is a RESTful api for us send GET's and POST's requests. It is composed by 5 endpoints:
- `/api/postwoman`: Endpoint to CRUD operations of postwoman.
- `/api/postoffice`: Endpoint to CRUD operations of postoffice.
- `/api/letters`: Endpoint to CRUD operations of letters.
- `/api/placetovisit`: Endpoint to CRUD operations of placetovisit.
- `/api/route`: Endpoint to calculate and return the route for a postwoman in a specific day.

## Calculate a route
To calculate a route for a specific postwoman and day, we create a direct graph where the set of nodes is: 1) PostOffice, that is the start point, 2) places to deliver a letter(Deliver Points) and 3) Places that the postwoman would like to visit(PlaceToVisit).

For each node in the set of nodes compost by nodes in 1) and 2) we create 2 arcs(source-->dest and dest-->source) with cost equal the distance calculated between the latitude and longitude of these nodes. At this point, we have a complete graph.

For the set of nodes compost by nodes in 2) and 3) we create an arc from a node in the set 3) to a node in the set 2) with cost equal the distance calculated between the latitude and longitude of these nodes. If this distance is less than or equal to `max_distance`, we add the reverse arc too. This is to be possible go from any PlaceToVisit to Deliver Points but is only possible go from Deliver Points to PlaceToVisit, if the distance is less than or equal the maximum distance allowed.

The heuristic to calculate the route is very simple and consist in go to nearest location not yet visited. To make this efficient, in the graph explained before,we use a MinHeap to store the adjacents nodes of a node. Each item in this MinHeap is compost by the distance and the node. Then, the first place of this MinHeap store the nearest adjacent node.

# Requirements
To run the solution is necessary we have the docker and the docker-compose installed in the host machine.
In the docker container, we will install all that is necessary:
- Python, version 3.7
- Django, version 2.1.7
- DjangoRestFramework, version 3.9.2
- Postgres, version 11.2

# How to run
To run the solution, from the main folder of this repo, we can run the command:
```
docker-compose up --build
```
After run this command, we can open the browser in the address: http://127.0.0.1:8000/api to interact with the solution.
The database already start with 1 PostOffice, 1 Postwoman, 1000 Letters(randomly distributed in 7 days) and 100 Places To Visit.
We can go to http://127.0.0.1:8000/api/route/, and send a Post for a PostWoman and date and then verify the route calculated.

# How to run the tests
To run the tests, from the main folder of this repo, we can run the command:
```
docker-compose -f docker-compose.yml -f docker-compose-tests.yml up --build --exit-code-from api
```

After run the tests we can see the report about coverage, flake8 and radon.

# Heroku
This solution was deployed in the heroku, and we can access in the address: https://postwoman.herokuapp.com/api/

# Improvements
- Put Nginx in front of gunicorn to manipulate the static files.
- Put the celery to calculate the route asynchronously.
