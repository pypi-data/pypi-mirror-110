# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Unreleased

## 2021.6.5 (18 June)

### Added

* Settings dialog in the GUI (File -> Settings).
  The preferred manga language can now be set through there.
* The manga info panel now shows the languages in the manga.

### Changed

* Mangadex urls must now start with `mangadex.org/title`.

### Removed

* Dependency on dataclasses-json.

### Fixed

* The GUI now shows chapters for the current language set.
* The Mangadex source now adds all languages to the manga.
* Mangadex chapter urls will now open correctly when clicked in the GUI.
* Downloading through the CLI. `Parser.by_url` was given the shorthash instead of the url.

## 2021.6.4 (16 June)

### Changed

* All source-related abstract base classes (i.e `Parser`) now reside in `tankobon/sources/base.py`.
  The source modules have been updated accordingly to reflect this.
* The method `Parser.parser` has been renamed to `Parser.by_url` to make it clearer what it is actually for.

## 2021.6.3 (14 June)

### Changed

* The root manga index file (at `~/.local/share/tankobon/index.json`) is now compressed with GZip.
  This should have significant space savings on disk, especially for large indexes (with a lot of manga).

## 2021.6.2 (11 June)

### Changed

* The bottom GUI in the toolbar now shows the correct colour icons (white for a dark system theme, and vice versa).
* Added locate button in the toolbar.

## 2021.6.1 (5 June)

### Added

* Dependency on [MangaDex.py](https://github.com/Proxymiity/MangaDex.py).
* Progess bar and about box in the GUI.
* Mangadex source (not complete yet).

### Changed

* Versioning system is now based on date in the form of `YYYY.MM.patch`, where patch is the release number for that month.
* Renamed `tankobon.parsers` to `tankobon.sources`.

### Fixed

* Checks for None when presenting Metadata objects in the GUI.
  Previously, any None values would cause `TypeError`.
