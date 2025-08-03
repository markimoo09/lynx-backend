from pydantic import BaseModel
from pydantic_ai import Agent, ModelSettings

SYSTEM_PROMPT = """
You will be summarizing, refining, and/or organizing notes given to you.
Format your output in markdown format, this is an example you can follow:

# July 25 2025 - API Authentication

## Summary
- Created a new API authentication system
- Modify Supabase JWT Access Token Claims to include the subscription status
- Utilize the modified token for API authentication

### JWT Architecture
- Detail 1
- Detail 2
- Detail 3
"""

agent = Agent(
  'google-gla:gemini-2.5-flash-lite',
  settings=ModelSettings(
    temperature=0.3
  ),
  system_prompt=SYSTEM_PROMPT
)

