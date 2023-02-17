# city-rents-api

- FastAPI
- MySQL
- Docker

## Setup

Please install `Docker` and `Docker compose` first.

https://www.docker.com/

After installation, clone this repository and run the following command to create a local Docker container.

git clone `https://github.com/lesilencieux/city-rents-api.git` # be  sure you are git installed in your machine

cd city-rents-api
chmod +x deploy.sh

or 

```bash
docker-compose down 
docker-compose build
docker-compose up -d
```

If you want to check the log while Docker container is running, then try to use following command:

```bash
docker-compose up
```

If Docker is running successfully, the API and DB server will be launched as shown in the following:

- API server: http://localhost:8000
- DB server: http://localhost:3306

_Be careful, it won't work if the port is occupied by another application._

If you want to check docker is actually working, then you can check it with following command:

```bash
docker ps
```

If you want to go inside of docker container, then try to use following command:

```bash
docker-compose exec mysql bash
docker-compose exec city_rents_api bash
```

For shutdown of the docker instance, please use following command:

```bash
docker-compose down
```

### Environment variable

Some of environment variable, like a database name and user is defined in `docker-compose.yml`.
You can customize it as you like.

If you will use docker, then please define your environment variable to `docker-compose.yml`.
However, you will NOT use docker, then please create `.env` file for your API server.

### DB Migrations

When creating DB docker container, docker will create predefined tables in `mysql/db` folder.
That help your team to control versions of database.

The sample table definition has already been created with the name `00_rent_table.sql`.

### API documentation

http://localhost:8000/api/v1/docs

![screen](https://github.com/lesilencieux/city-rents-api.git/city-rents-api/api/images/13.png)

### API Testing via swagger-ui

- Payload :

{
  "dep": 64,
  "area": 50,
  "price": 800
}

![screen](https://github.com/lesilencieux/city-rents-api.git/city-rents-api/api/images/12.png)

- Result

![screen](https://github.com/lesilencieux/city-rents-api.git/city-rents-api/api/images/11.png)


NB :  If the screens shot do not show properly you can got to se it directly in `/images` folder




