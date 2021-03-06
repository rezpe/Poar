## Poar - The easiest way to make your GAE apps RESTful compliant

Poar is a WSGI Application inside a Google App Engine Web App that handles data storage for your CRUD application and uses REST Protocol. I created it for my protoype applications where I needed a fast way to support this.

## How to use:

### Step 1: Include the Poar.py file into your GAE app

### Step 2: Add this in the app.yaml file to redirect "data" Request to Poar:

```yaml
- url: /data.*
  script: Poar.py
```

### Step 3: Include the definition of Store in the other Python files to use the Store class:

```python
class DictModel(db.Model):
    def to_dict(self):
        temp = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
        temp["id"] = unicode(self.key().id())
        return temp

class Store(DictModel):
	name = db.StringProperty()
        content = db.TextProperty()
        typeo = db.StringProperty()
	date = db.DateTimeProperty()
	owner = db.UserProperty()
```

### Step 4: Enjoy experimentation in GAE !

# I would love to get your feedback :)
