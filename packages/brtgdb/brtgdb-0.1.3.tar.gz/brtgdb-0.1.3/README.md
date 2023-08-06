# BRTG database connector
Simple package to establish connection with mysql/mariadb database using sqlalchemy.

## Prerequisite
Define environmental variables before lunching connector.

DB_HOST=host.com
DB_PORT=3306
DB_USER=your_user
DB_PASS=your_password

## Installation
From package directory:

```
pip install .
```

## Usage
Import
```
from brtgdb import BrtgDB
from dotenv import load_dotenv

load_dotenv()
db = BrtgDB()
```

With pandas
```
pd.read_sql("SELECT ....", db.conn)
```

functions
```
db.execute(query)
```