from ninja import NinjaAPI
from .models import Note
from pydantic import BaseModel
from typing import Optional, List

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
    return note
  except Exception as e:
    return 500, {"message": str(e)}

@api.get("/note/{note_id}", response={200: NoteBody, 500: Error, 404: Error})
def get_note(request, note_id: int):
  try:
    note = Note.objects.get(id=note_id)
    return NoteBody(
      name=note.name,
      description=note.description,
      prompt=note.prompt,
      file_path=note.file_path
    )
  except Exception as e:
    return 500, {"message": str(e)}
  except Note.DoesNotExist:
    return 404, {"message": "Note not found"}

@api.get("/note", response={200: List[NoteBody], 500: Error, 404: Error})
def get_notes(request):
  try:
    notes = Note.objects.all()
    return [NoteBody(
      name=note.name,
      description=note.description,
      prompt=note.prompt,
      file_path=note.file_path
    ) for note in notes]
  except Exception as e:
    return 500, {"message": str(e)}
  except Note.DoesNotExist:
    return 404, {"message": "Note not found"}
