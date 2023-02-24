"""Module for SQLAlchemy models.

You have to implement your sqlalchemy models in app/db/sqlalchemy_models.py file so alembic can detect them.
Inherit your models from Base class.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
