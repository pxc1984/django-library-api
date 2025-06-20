# Template project with JWT authorization

## Env variables:

| Key               | Value                                                 |
|-------------------|-------------------------------------------------------|
| DJANGO_SECRET_KEY | str formatted secret key                              |
| DJANGO_DEBUG      | "TRUE" if debug enabled and anything else if disabled |
| DATABASE          | possible options are<br/>- SQLITE3<br/>- POSTGRESQL   |

### Database configuration

If you are using **POSTRESQL** database, you should set the following environmental variables

| Key      | Default value                 |
|----------|-------------------------------|
| NAME     | mydatabase                    |
| USER     | mydatabaseuser                |
| PASSWORD | mypassword                    |
| HOST     | 127.0.0.1                     |
| PORT     | 5432                          |

If you are using **SQLite** database, you should set the following environmental variables

| Key  | Default value |
|------|---------------|
| NAME | db.sqlite3    |
