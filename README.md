## Backend BLCK DEVELOPERS tontine app

>>:bomb: :moneybag: :dollar::bomb: :moneybag: :dollar::bomb: :moneybag: :dollar::bomb: :moneybag: :dollar::bomb: :moneybag: :dollar::bomb: :moneybag: :dollar::bomb: :moneybag: :dollar:

***
## PRIVATE CLONE USING SSH

Configure your ssh and clone using ssh
here a helpful link

> [https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/](https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/)

## Requirements
**To run this project correctly you must have:**

>- python 3.8 (or 3.9)
>- docker (latest)
>- postgresql (optional)
---

if you've installed postgresql locally please do the following:
>  + create a superuser with following credentials:
>    + `EMAIL=abdoufermat5@blckdev.sn` if you decide to create your own make sure to update `.env`file
>    + `PASSWORD=Fanta1976`
>    + command (`psql console`):
>    
>    ```sh
>    sudo -u postgres psql
>    CREATE ROLE 'abdoufermat5@blckdev.sn' LOGIN SUPERUSER PASSWORD 'Fanta1976'
>    
>  + create a database called `test_backend` and give access to your created superuser
>    + command (`psql console`):
>    
>    ```sh
>    sudo -u postgres psql
>    CREATE DATABASE test_backend;
>    GRANT ALL PRIVILEGES ON DATABASE test_backend TO 'abdoufermat5@blckdev.sn';
>    
NB: if you stuck on `psql console` you can do all above instructions using `pgAdmin4`
## Usage

**Create `virtualenv` and Install `requirements.txt`**

In root folder open terminal and run:

>>```bash 
>>python3 -m venv venv
>>source venv/bin/activate
>>cd test_backend
>>pip install -r requirements.txt

In root folder open terminal and:

1. Run project locally

>>```bash
>>docker-compose up -d --build


2. Run project on staging

>>```bash
>>docker-compose -f docker-compose-staging.yml up -d --build

* IMPORTANT: **DON'T RUN** the `docker-compose.prod.yml` file

+ NB: by default a superuser with credentials `EMAIL=blck.dev@ept.sn`and
`PASSWORD=Fermat1976`is created if you're running staging docker



**Run server locally without docker (if you have already installed `postgresql`)**
+ change the environment variable used

Go to `settings.py` and change the `env_file` variable to:
```python
env_file = os.path.join(PROJECT_PATH, ".env")
```
then at the root folder run:
>> ```python test_backend/manage.py runserver 8002```

<hr/>

**HERE ARE DEFAULT LINKS:**

+ if local/staging docker

> **SWAGGER UI: homepage -- LIST OF ALL ENDPOINTS**

>> [localhost:1332/](http://localhost:1332/)

> **SWAGGER UI: full documentation**

>> [localhost:1332/doc/](http://localhost:1332/doc/)

> **ADMIN**

>> [localhost:1332/admin/](http://localhost:1332/admin/)

+ if local without docker

> **SWAGGER UI: homepage -- LIST OF ALL ENDPOINTS**

>> [localhost:8002/](http://localhost:8002/)

> **SWAGGER UI: full documentation**

>> [localhost:8002/doc/](http://localhost:8002/doc/)

> **ADMIN**

>> [localhost:8002/admin/](http://localhost:8002/admin/)
