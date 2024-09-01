# Self_Test
Test task for company "Self"

### Project features

* You will have the base admin panel
* Able to top up the account balance
* Able to withdraw
* Get the full transactions history

### How to use:

#### Clone the repo

```shell
git clone https://github.com/AcidInvader/Self_Test.git
```

#### Before running you need to apply the migrations by next commands

```shell
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```

#### Then you need to run dev server

```shell
python3 manage.py runserver
```
The swagger you will reach at http://127.0.0.1:8000/api/schema/swagger-ui/

### Optional, can create superuser and get in admin panel

```shell
python3 manage.py createsuperuser
```
The admin panel you will reach at http://localhost:8000/admin/login/?next=/admin/




