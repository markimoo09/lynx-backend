from ninja import NinjaAPI
from .models import Note
from pydantic import BaseModel
from typing import Optional

api = NinjaAPI()

class NoteBody(BaseModel):
  name: str
  description: Optional[str] = None
  prompt: str
  file_path: str

class Error(BaseModel):
  message: str


@api.post("/note", response={200: NoteBody, 500: Error})
def create_note(request, note: NoteBody):
  try:
    Note.objects.create(**note.model_dump())
    return 200, note
  except Exception as e:
    return 500, {"message": str(e)}


