# sqlalchemy-challenge
Before You Begin
Create a new repository for this project called sqlalchemy-challenge. Do not add this assignment to an existing repository.

Clone the new repository to your computer.

Inside your local Git repository, create a directory for this Challenge. Use a folder name that corresponds to the Challenge, such as SurfsUp.

Add your Jupyter notebook and app.py to this folder. They’ll contain the main scripts to run for analysis. Also add the Resources folder, which contains the data files you will be using for this challenge.

Push the changes to GitHub or GitLab.

Part 1: Analyze and Explore the Climate Data
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:

Note that you’ll use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.

Use the SQLAlchemy create_engine() function to connect to your SQLite database.

Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.

Link Python to the database by creating a SQLAlchemy session.

IMPORTANT
Remember to close your session at the end of your notebook.

Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.
