from typing import List
from db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from models import Contacts
from schemas import ContactBase, ContactResponse, UserModel
from models import User
from libgravatar import Gravatar


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contacts]:
    return db.query(Contacts).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contacts:
    return db.query(Contacts).filter(Contacts.id == contact_id).first()


async def create_contact(body: ContactResponse, db: Session = Depends(get_db)) -> Contacts:
    contact_data = body.dict()
    contact = Contacts(**contact_data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactResponse, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact:
        for attr, value in body.dict(exclude_unset=True).items():
            setattr(contact, attr, value)
        db.commit()
        db.refresh(contact)

    return contact


async def delete_contact(contact_id: int, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def get_contacts(skip: int, limit: int, db: Session, current_user: User) -> List[Contacts]:
    return db.query(Contacts).filter_by(user=current_user).offset(skip).limit(limit).all()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
