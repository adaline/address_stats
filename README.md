# address_stats

## Getting started

### Install virtualenv

```bash
pip3 install virtualenv
source env/bin/activate
```

### Install requirements

```
pip install -r requirements.txt
```

### Import data

```
python3 init_database.py
```

### Run the tests

```
pytest
```

### Run the app

```bash
python3 app.py
```

You should be able to access the app on: http://localhost:5000/

### Endpoints

- `/count` - delivers the number of buildings per zip code.

  Example response:

  ```json
  { "count": 123 }
  ```

- `/distribution` - shows the distribution of years in which buildings were added to the dataset.

  Exmaple response:

  ```json
  [{ "1960": 949 }, { "1993": 118 }, { "1994": 6 }, { "2011": 1 }]
  ```

Both can be filtered by postocdes, multiple postocdes should be separated by `;` eg:

- `/count/10997` - view only 10997 count
- `/count/10997;10969` - view 10997 and 10969 count
- `/distribution/10997;10969` - distribution across 10997 and 10969 postcodes
