# flask-rest-api

Simple REST API written with Flask-RESTful, Flask-SQLAlchemy and marshmallow.

**Example endpoints:**

Add Item:
```
curl -XPOST -d '{"name" : "curlname", "description" : "curldescription"}' -H "Content-Type: application/json" localhost:5000/items
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
python -m tests.test_item
```
