from ninja import NinjaAPI
from .models import Note
from pydantic import BaseModel
from typing import Optional, List
from asgiref.sync import sync_to_async
from analyzer.analyzer import analyze_note as ai_summarizer

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
  section_content: str

class WriteToNoteBody(BaseModel):
  note_id: int
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

@api.post("/note/write", response={200: Error, 500: Error})
async def write_to_note(request, body: WriteToNoteBody):
  note_id = body.note_id
  section_content = body.section_content

  if not body.note_id or not body.section_content:
    return 500, {"message": "Invalid request"}

  try:
    note = await sync_to_async(Note.objects.get)(id=note_id)
    note_location = note.file_path

    with open(note_location, "a", encoding="utf-8") as file:
      file.write("\n\n")
      file.write(section_content + "\n")

    return 200, {"message": "Note updated"}
  except Exception as e:
    print("Failed with this error: ", e)
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

@api.put("/note/{note_id}", response={200: NoteBody, 500: Error, 404: Error})
def update_note(request, note_id: int, body: NoteBody):
  try:
    note = Note.objects.get(id=note_id)
    note.name = body.name
    note.description = body.description
    note.prompt = body.prompt
    note.file_path = body.file_path

    note.save()
    return 200, body
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
async def analyze_note(request, body: AnalyzeNoteBody):

  # Get the note name and its prompt
  try:
    note = await sync_to_async(Note.objects.get)(id=body.note_id)
  except Exception as e:
    return 500, {"message": str(e)}

  noteFilePath = note.file_path
  notePrompt = note.prompt

  markdown_section_level = body.markdown.count("#")
  markdown_section = body.markdown

  in_markdown_section = False
  section_content = []

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
          continue

  if len(section_content) == 0:
    return 500, {"message": "No content found"}

  response = await ai_summarizer(section_content)
  if response is None:
    return 500, {"message": "Failed to analyze note"}

  return AnalyzeNoteResponse(
    section_content=response
  )




