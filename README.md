# Linkcat Access
This library allows you to access the Linkcat backend in a programatic way. This is accomplished through user impersonation and html parsing.

## Currently working data functions:
  * linkcat.get_checked_out_books() - returns currently checked out books, along with basic metadata

## Todo:
  * Abstract out library card storage in config
  * Login failure is not properly detected (always returns true)
