# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy import create_engine
# from flask_sqlalchemy import SQLAlchemy
# from app import db
# # db = SQLAlchemy()
# # print(db)

# Base = automap_base(db.Model)
# engine = create_engine('postgresql://xymzimekksmhco:46887cbb0d16af42586a19224f5b3a37a1ce8f60b6bf15c182f36963a1c5c854@ec2-23-20-224-166.compute-1.amazonaws.com:5432/d3n66vadq0jsq8')
# Base.prepare(engine, reflect=True)

# for record in db.session.query(Base.classes.challenges).all():
#   print(record)
# # print(Base.classes.keys())

from app import Base

Challenge = Base.classes.get('challenges' or None)
User = Base.classes.get('users' or None)
Course = Base.classes.get('courses' or None)
Attempt = Base.classes.get('attempts' or None)
Enroll = Base.classes.get('enrolled' or None)


