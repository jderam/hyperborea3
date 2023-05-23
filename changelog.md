# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.4] - 2023-05-22
### Changed
- Use flit as the tool for building and publishing

## [0.6.1] - 2023-02-18
### Added
- Added class ability descriptions (only partially)

## [0.6.0] - 2023-02-08
### Changed
- Removed Docker stuff from Makefile
- Updated `make gen_requirements` to use `--resolver=backtracking`
- Added `make rebuild_venv` command
- Recompiled requirements files on python 3.11
- Added upgrade `pip` and install `pip-tools` steps to `make resync_requirements` to eliminate the need to do those steps manually.
- Moved `list_tables()`, `list_views()`, and `get_count_from_table()` functions in `db` module.
- Updated list of `VALID_SQL_TABLES`
- Updated `get_languages()` function to include default racial languages.

### Added
- Added `ipython` as a dev requirement

## [0.5.4] - 2023-02-08
### Added
- Added `character_id` to PlayerCharacter, a 32-character UUID
- Added python 3.11 to test matrix

## [0.5.3] - 2023-02-06
### Fixed
- Fixed patronymic modification for the Pictish name "Segovax"
- Fixed patronymic modification for the Viking names:
  - Björn
  - Gedda
  - Hákon
  - Magnus

## [0.5.2] - 2023-02-03
### Added
- Added name generation

## [0.4.6] - 2023-01-20
### Added
- Added Eye Colour, Hair Colour, Complexion to character generation

## [0.4.5] - 2023-01-19
### Added
- Added languages to character generation

## [0.4.4] - 2022-12-31
### Added
- Added height and weight to character generation

## [0.4.3] - 2022-12-31
### Added
- Added age to character generation

## [0.4.2] - 2022-12-30
### Fixed
- Reload all spells to ensure everything in the database is the latest

## [0.4.1] - 2022-12-30
### Fixed
- Fix some html formatting issues with spells

## [0.4.0] - 2022-12-30
### Changed
- Regenerate requirements.txt
- Update documentation

## [0.3.10] - 2022-12-30
### Added
- Added 6th-level spells to database. Spells are complete!

## [0.3.9] - 2022-10-07
### Changed
- Switch to using pyproject.toml instead up setup.py
- Updates to Makefile, dev toolchain

## [0.3.8] - 2022-10-03
### Added
- Added secondary skill to character generation

## [0.3.7] - 2022-09-25
### Added
- Added 5th level spells
