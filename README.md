![foodgram workflow](https://github.com/DKudrik/foodgram/actions/workflows/main.yml/badge.svg)


# foodgram project

Visit the project at foodgram-project.gq (or http://84.201.177.46/)


Foodgram is a project that features plenty of recipes of different cuisine

### Prerequisites

Install Docker

### Installing

To start a project:
1. Go to a 'foodgram-project' folder
2. Type 'docker-compose up' in terminal
3. Aplly migrations:
  * docker-compose exec web python manage.py migrate --noinput
4. Create superuser
  * docker-compose exec web python manage.py createsuperuser
5. Collect static
  * docker-compose exec web python manage.py collectstatic --no-input

## Built With

* [Python](https://www.python.org/) - The programming language used
* [Docker](https://maven.apache.org/) - Platform to deliver software in packages (containers)
* [Postgres](https://www.postgresql.org/) - DB used

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/DKudrik/project/tags). 

## Authors

* **Denis Kudrik** - *Initial work* - [DKudrik](https://github.com/DKudrik/foodgram-project)

## License

This project is licensed under the MIT License

