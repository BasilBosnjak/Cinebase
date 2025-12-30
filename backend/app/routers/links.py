from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from ..models import Link
from ..schemas import LinkUpdate, LinkResponse

router = APIRouter(prefix="/links", tags=["links"])

@router.put("/{link_id}", response_model=LinkResponse)
def update_link(link_id: UUID, link_update: LinkUpdate, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    update_data = link_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(link, field, value)

    db.commit()
    db.refresh(link)
    return link

@router.delete("/{link_id}", status_code=204)
def delete_link(link_id: UUID, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()
    return None
