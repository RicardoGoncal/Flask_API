from db import db


class ItemTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id_item"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.tag_id"))