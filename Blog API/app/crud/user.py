from app.models.user import User
def create_user(db,user):
    new_user=User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 