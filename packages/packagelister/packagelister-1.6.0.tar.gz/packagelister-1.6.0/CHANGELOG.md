# Changelog

## v1.5.1 (2023-05-02)

#### Fixes

* fix crash when trying to import something that isn't a module


## v1.5.0 (2023-05-01)

#### New Features

* add recursive option to get_packages_from_source
#### Others

* build v1.5.0
* update changelog


## v1.4.0 (2023-05-01)

#### New Features

* add get_packages_from_source()
#### Refactorings

* remove pathcrawler usage
* refactor scan to use get_packages_from_source
#### Others

* build v1.4.0
* update changelog


## v1.3.1 (2023-04-28)

#### Fixes

* update printbuddies.ProgBar usage to new version
#### Others

* build v1.3.1
* update changelog


## v1.3.0 (2023-04-15)

#### New Features

* add whosuses to scripts table
#### Refactorings

* move bulk of work into seperate function
#### Others

* build v1.3.0
* update changelog


## v1.2.0 (2023-04-12)

#### New Features

* add switch to add package versions with chosen relation when generating requirements.txt
#### Others

* build v1.2.0
* update changelog


## v1.1.3 (2023-03-22)

#### Others

* build v1.1.3


## v1.1.2 (2023-02-04)

#### Fixes

* (cli): change == to ~= when generating requirements.txt
#### Others

* update to build v1.1.2
* update changelog


## v1.1.1 (2023-01-25)

#### Fixes

* pyproject.toml indentation issue
#### Others

* build 1.1.1 dist files
* (cli): change abbreviated switches to single letters