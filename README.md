![YamDB workflow](https://github.com/DKudrik/yamdb_final/actions/workflows/main.yml/badge.svg)


# foodgram project

Visit the project at foodgram.gq (or http://130.193.56.221/)


Foodgram is a project that features plenty of recipes of different cuisine

### Prerequisites

Install Docker

### Installing

To start a project:
1. Go to a 'amdb_final' folder
2. Type 'docker-compose up' in terminal
3. Go to api_yamdb container and aplly migrations
* To get into a container with postgres DB or with api_yamdb project open a new terminal tab 
   and type 'docker ps', then choose ID of the container and type 'docker exec -it <container_id> bash'
*  To fill a DB with test data you can use fixtures.json file:
    - Copy test data to an api_yamdb container with command 'docker cp fixtures.json <container_id>:code/' 
    - Being in the container open shell 'python3 manage.py shell'
    - type 'from django.contrib.contenttypes.models import ContentType'
    - type 'ContentType.objects.all().delete()'
    - type 'quit()'
    - type 'python manage.py loaddata fixtures.json'
*  To create a superuser in api_yamdb container type 'python manage.py createsuper'

## Built With

* [Python](https://www.python.org/) - The programming language used
* [Docker](https://maven.apache.org/) - Platform to deliver software in packages (containers)
* [Postgres](https://www.postgresql.org/) - DB used

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/DKudrik/project/tags). 

## Authors

* **Denis Kudrik** - *Initial work* - [DKudrik](https://github.com/DKudrik/infra_sp2)

## License

This project is licensed under the MIT License

