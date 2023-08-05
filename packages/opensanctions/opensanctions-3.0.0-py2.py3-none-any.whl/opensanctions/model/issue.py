from banal import is_mapping
from sqlalchemy import func, Column, Integer, Unicode, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from opensanctions import settings
from opensanctions.model.base import Base, db, ENTITY_ID_LEN


class Issue(Base):
    __tablename__ = "issue"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    level = Column(Unicode, nullable=False)
    module = Column(Unicode)
    dataset = Column(Unicode, index=True, nullable=False)
    message = Column(Unicode)
    entity_id = Column(Unicode(ENTITY_ID_LEN), index=True)
    entity_schema = Column(Unicode)
    data = Column(JSONB, nullable=False)

    @classmethod
    def save(cls, event):
        data = dict(event)
        for key, value in data.items():
            if hasattr(value, "to_dict"):
                value = value.to_dict()
            data[key] = value
        issue = cls()
        data.pop("timestamp", None)
        issue.timestamp = settings.RUN_TIME
        issue.module = data.pop("logger", None)
        issue.level = data.pop("level")
        issue.message = data.pop("event", None)
        issue.dataset = data.pop("dataset")
        entity = data.pop("entity", None)
        if is_mapping(entity):
            issue.entity_id = entity.get("id")
            issue.entity_schema = entity.get("schema")
        elif isinstance(entity, str):
            issue.entity_id = entity
        issue.data = data
        db.session.add(issue)

    @classmethod
    def clear(cls, dataset):
        pq = db.session.query(cls)
        pq = pq.filter(cls.dataset.in_(dataset.source_names))
        pq.delete(synchronize_session=False)

    @classmethod
    def query(cls, dataset=None):
        q = db.session.query(cls)
        if dataset is not None:
            q = q.filter(cls.dataset.in_(dataset.source_names))
        q = q.order_by(cls.id.asc())
        return q

    @classmethod
    def agg_by_level(cls, dataset=None):
        q = db.session.query(cls.level, func.count(cls.id))
        if dataset is not None:
            q = q.filter(cls.dataset.in_(dataset.source_names))
        q = q.group_by(cls.level)
        return {l: c for (l, c) in q.all()}

    def to_dict(self):
        # TODO: should this try and return an actual nested entity?
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "level": self.level,
            "module": self.module,
            "dataset": self.dataset,
            "message": self.message,
            "entity_id": self.entity_id,
            "entity_schema": self.entity_schema,
            "data": self.data,
        }
