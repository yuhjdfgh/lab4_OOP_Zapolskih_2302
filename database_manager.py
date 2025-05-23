from sqlalchemy.orm import Session
from models import SessionLocal, ArtObject, Painting, Sculpture

def create(table, params):
    db = SessionLocal()
    try:
        art_object = ArtObject(title=params[0], author=params[1])
        db.add(art_object)
        db.flush()
        
        if table == 'painting':
            painting = Painting(
                size=int(params[2]),
                type_color=params[3],
                art_object_id=art_object.id
            )
            db.add(painting)
        else:
            sculpture = Sculpture(
                weight=float(params[2]),
                material=params[3],
                art_object_id=art_object.id
            )
            db.add(sculpture)
        
        db.commit()
        return art_object.id
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_all_paintings():
    db = SessionLocal()
    try:
        paintings = db.query(ArtObject, Painting)\
            .join(Painting, ArtObject.id == Painting.art_object_id)\
            .all()
        
        return [
            (art.id, art.title, art.author, painting.size, painting.type_color)
            for art, painting in paintings
        ]
    finally:
        db.close()

def get_all_sculptures():
    db = SessionLocal()
    try:
        sculptures = db.query(ArtObject, Sculpture)\
            .join(Sculpture, ArtObject.id == Sculpture.art_object_id)\
            .all()
        
        return [
            (art.id, art.title, art.author, sculpture.weight, sculpture.material)
            for art, sculpture in sculptures
        ]
    finally:
        db.close()

def read(table, id):
    db = SessionLocal()
    try:
        if table == 'painting':
            result = db.query(
                ArtObject.title,
                ArtObject.author,
                Painting.size,
                Painting.type_color
            ).join(
                Painting, ArtObject.id == Painting.art_object_id
            ).filter(
                ArtObject.id == id
            ).first()
            
            if result:
                return result
        
        else:
            result = db.query(
                ArtObject.title,
                ArtObject.author,
                Sculpture.weight,
                Sculpture.material
            ).join(
                Sculpture, ArtObject.id == Sculpture.art_object_id
            ).filter(
                ArtObject.id == id
            ).first()
            
            if result:
                return result  # (title, author, weight, material)
        
        return None
    finally:
        db.close()

def update(table, params):
    db = SessionLocal()
    try:
        art_object = db.query(ArtObject).get(params[0])
        if art_object:
            art_object.title = params[1]
            art_object.author = params[2]
            
            if table == 'painting':
                painting = db.query(Painting)\
                    .filter(Painting.art_object_id == params[0])\
                    .first()
                if painting:
                    painting.size = int(params[3])
                    painting.type_color = params[4]
            else:
                sculpture = db.query(Sculpture)\
                    .filter(Sculpture.art_object_id == params[0])\
                    .first()
                if sculpture:
                    sculpture.weight = float(params[3])
                    sculpture.material = params[4]
            
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def delete(table, id):
    db = SessionLocal()
    try:
        art_object = db.query(ArtObject).get(id)
        if art_object:
            db.delete(art_object)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
