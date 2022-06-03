from datetime import datetime
from typing import List

from sqlalchemy import column, Column, Integer, String, DateTime

from loader import db_gino
import sqlalchemy as sa


class BaseModel(db_gino.Model):
    __abstract__ =True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self,self._column_name_map[column.name])
            for column in columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimeBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db_gino.func.now())
    updated_at = Column(DateTime(True),
                        default=db_gino.func.now(),
                        onupdate=db_gino.func.now(),
                        server_default=db_gino.func.now())


class BSModel(BaseModel):
    __tablename__ = "bsmodel"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

print(BSModel())

