# CHANGELOG for udn_songbook

This project attempts to adhere to [semantic versioning](https://semver.org)

## 1.1.1
- more sane boolean template vars
- new kwargs for templates (song & index)
- updated dependencies (new versions of blck/click/weasyprint etc)

## 1.1.0
- add page IDs
- adds rendering code & template for songs
- use pychord for chord naming
- add transposition code using pychord
- fix chord parsing to handle 'tails' like '*'
- page numbering and content deduplication

## 1.0.4
- require python >= 3.8

## 1.0.3
- dependency updates
  - Adds LXML dependency
  - python >= 3.7
- black-formatted
- adds pre-commit checks (black, flake8)
- adds index template

## 1.0.2
- update dependencies for PyYAML (5 or greater)

## 1.0.1
- update dependencies for newer versions of
  - BeautifulSoup4 4.9.3 to 5
  - ukedown v2-3
  - Markdown v3-4

## 1.0.0
- Initial Release (limited functionality)
- creates Song and SongBook objects from directories and files.
- Generates Index
