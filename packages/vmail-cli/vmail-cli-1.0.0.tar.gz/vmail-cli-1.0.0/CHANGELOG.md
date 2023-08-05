# Changelog

All notable changes to `vmail-cli` will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 1.0.0 - 2021-06-19
### Added
- Make password scheme configurable and use SHA512-CRYPT as default

### Changed
- Uniformize and reduce sub-commands to `list`, `add`, `edit` and `remove`
- Rename configuration sections and regroup `DB.dialect` and `DB.driver` into
  `database.type`
- Remove arguments related to the configuration to only use YAML files, except
  for the database user's password
- Replace poetry by setuptools for the Python packaging
