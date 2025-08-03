from cmd import PROMPT
from ninja import NinjaAPI
from .models import Note
from pydantic import BaseModel
from typing import Optional, List
import markdown

api = NinjaAPI()

class NoteBody(BaseModel):
  name: str
  description: Optional[str] = None
  prompt: str
  file_path: str

class AnalyzeNoteBody(BaseModel):
  note_id: int
  markdown: str

class AnalyzeNoteResponse(BaseModel):
  section_name: str
  section_content: str

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

@api.post("/analyze_note", response={200: AnalyzeNoteResponse, 500: Error})
def analyze_note(request, body: AnalyzeNoteBody):

  # Get the note name and its prompt
  try:
    note = Note.objects.get(id=body.note_id)
  except Exception as e:
    return 500, {"message": str(e)}

  noteFilePath = note.file_path
  notePrompt = note.prompt

  markdown_section_level = body.markdown.count("#")
  markdown_section = body.markdown

  in_markdown_section = False
  section_content = []
  section_name = ""

  # Open and extract data from the file
  with open(noteFilePath, "r") as file:
    for line in file:
      line_stripped = line.strip()

      if in_markdown_section and line_stripped.startswith("#") and line_stripped.count("#") <= markdown_section_level:
        break

      if in_markdown_section and line_stripped != "" and not "![[" in line_stripped:
        section_content.append(line)

      if line_stripped.startswith("#"):
        if line_stripped == markdown_section:
          in_markdown_section = True
          section_name = line_stripped.replace("#", "").strip()
          continue

  return AnalyzeNoteResponse(
    section_name=section_name,
    section_content="\n".join(section_content)
  )



