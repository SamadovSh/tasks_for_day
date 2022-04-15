from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base, TodoItem

engine = create_engine("sqlite:///tasks.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()

for desc in ('прочитать книгу', "помыть посуду", "поесть", "поспать"):
    t = TodoItem(desc)
    s.add(t)

s.commit()
