# models/__init__.py
# Import all models here so that Base.metadata knows about every table
# before create_all() is called in main.py.

from app.models.user_temp import User           # noqa: F401  (side-effect import)
from app.models.notification import Notification  # noqa: F401
