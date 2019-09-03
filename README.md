# Simple wsgi application
As four otus homework simple wsgi application is a primitive wsgi framework. By creating this framework you will get basic understanding off how it works in real life in big complex frameworks such as flask and django.
## Installaltion
Clone project from repository
```bash 
git clone https://github.com/ilearnToday/otus_simple_wsgi_app.git
```
Install requirements.txt
```bash
 pip install -r requirements.txt 
```
## Usage
Full example you can check in example.py 
```python
from core.py import Application

app = Application()

@app.register_route('/index/')
def index_page(env):
    return {
            'text': 'Hello world!'    
}
```
Run uwsgi:
```bash
uwsgi --http :9090 --wsgi-file example.py 
```
 Your site will be [here](http://localhost:9090)
## Requirements
```Jinja2==2.10.1```
```uWSGI==2.0.18```
