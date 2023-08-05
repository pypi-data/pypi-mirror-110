# vmail-cli

**DISCLAIMER: THIS APPLICATION IS STILL IN ALPHA/BETA STATE. DO NOT USE IT IN PRODUCTIVE ENVIRONMENTS IF YOU DON'T WHAT YOU'RE DOING!**

`vmail-cli` is a command line tool and library for managing a mail-server
database based on the great [HowTo](https://thomas-leister.de/en/mailserver-debian-stretch)
from [Thomas Leister](https://thomas-leister.de) written in Python 3. Although
the tutorial is using a MySQL/MariaDB database, this command line tool also
supports other backends.

## Requirements

- Python 3 (>= 3.7)

You should use a dedicated and non-privileged user account to run this CLI. You
could also rely on the packages provided by your GNU/Linux distribution. On a
Debian-based host, you can install the following packages:
- `python3-click`
- `python3-passlib`
- `python3-sqlalchemy`, with `python3-mysqldb` to use a MySQL database or
  `python3-psycopg2` for PostgreSQL
- `python3-tabulate`
- `python3-yaml`
- `python3-argon2` for Argon2 password hashing (optional)

Finally, you should follow the tutorial to have a working mail setup with
Postfix and Dovecot. Note that the database tables will automatically be
created by this CLI as needed.

## Installation
### Via pip

Install it with:

```sh
pip3 install --user vmail-cli
```

### Manually (for development)

Clone this repository or download the sources on your local machine, and go into
this directory.

Install all requirements with:

```sh
pip3 install -e .[test]
```

## Configuration

You can create your local configuration thanks to the wizard:

```sh
vmail-cli config init
```

You will have to create the database and the user if it is not already done. For
a MariaDB database, this can be done with:

```sql
CREATE DATABASE vmail;
GRANT ALL ON vmail.* TO 'vmail-cli'@'localhost' IDENTIFIED BY 'your-password';
```

Note that the local configuration is stored in a [YAML](https://yaml.org/) file
loaded by [confuse](https://confuse.readthedocs.io/en/latest/usage.html#search-paths).
It should be located in ``$XDG_CONFIG_HOME/vmail/config.yaml`` or
``~/.config/vmail/config.yaml`` on GNU/Linux. You could have a look at the
[default configuration](vmail/config_default.yaml) for available parameters.

## Usage

Use the `--help` argument to list available commands with their options:

```sh
vmail-cli --help
```

## License

It started as a fork of [`vmail-manager`](https://pypi.org/project/vmail-manager/)
written by Dominik Rimpf and licensed under the [MIT License](LICENSE).
