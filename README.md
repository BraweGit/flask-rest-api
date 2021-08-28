# flask-rest-api

Simple REST API written with Flask-RESTful, Flask-SQLAlchemy and marshmallow.

**Example endpoints:**

Add Item:
```
curl -d '{"name" : "curlname", "description" : "curldescription"}' -H "Content-Type: application/json" -X POST localhost:5000/items
```

Get Items:
```
curl -XGET localhost:5000/items
```

Get Item:
```
curl -XGET localhost:5000/items/1
```

Tests:
```
python -m unittest
python3 -m unittest
```
