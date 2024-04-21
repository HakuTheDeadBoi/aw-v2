New version of antique-watchgod!
I am completely rewriting it in OOP style, trying to make it as modular as possible.

Modules working:
  - trhknih.py (my first scraper)
  - timestamper
  - mailer
  - classes: Record, Query, ConstraintGroup, Constraint, Scraper

Modules in progress:
  - logger (or loggerfactory)
  - scrapermanager
  - queryparser

Modules missing:
  - scheduler
  - some app.run script or something like that
  - whole frontned section and Flask app at the background
