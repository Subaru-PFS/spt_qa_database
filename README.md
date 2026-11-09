# spt_qa_database
Database to store QA outputs from DRP as well as observation conditions.

## Installation

```sh
pip install .          # library: sqlalchemy and psycopg (3)
pip install -e '.[dev]'  # plus alembic, pytest, pandas, ...
```

Connect with a `postgresql+psycopg://user@host:port/dbname` URL. SQLAlchemy 2.1
also accepts plain `postgresql://` for psycopg 3, but older versions map that to
psycopg2, which is no longer installed.
