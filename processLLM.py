from openai import OpenAI
from pdf2image import convert_from_path
import base64
import io
import json
from PIL import Image

OPENAI_API_KEY = open('./secret').read()
client = OpenAI(api_key = OPENAI_API_KEY)

def to_base64(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def split_problems(path):
#   images = convert_from_path(path, dpi=300, fmt="png")
#   idx = 1
#   i = 0
#   for image in images:
#     i += 1
#     response = client.chat.completions.create(
#       model="gpt-4.1",
#       messages=[
#         {
#           "role": "system",
#           "content": (
#             "You are a document layout analysis model. "
#             "Your task is to identify complete problem blocks using pixel coordinates. "
#             "A problem block may start or end outside the current page."
#           )
#         },
#         {
#           "role": "user",
#           "content": [
#             {
#               "type": "text",
#               "text": (
#                 "This image is a SINGLE PAGE of a multi-page math document.\n\n"
#                 "Each problem block consists of a full problem statement AND its entire solution.\n"
#                 "Do NOT separate problems and solutions into different blocks.\n\n"
#                 "IMPORTANT:\n"
#                 "- A problem block may CONTINUE from the previous page.\n"
#                 "- A problem block may CONTINUE to the next page.\n"
#                 "- You MUST NOT discard incomplete problem blocks.\n\n"
#                 "Segment the image into COMPLETE PROBLEM BLOCKS using PIXEL COORDINATES.\n\n"
#                 "For each problem block, return:\n"
#                 "- start_y: top Y pixel coordinate of the block ON THIS PAGE\n"
#                 "- end_y: bottom Y pixel coordinate of the block ON THIS PAGE\n"
#                 "- open_start: true if the problem clearly started BEFORE this page\n"
#                 "- open_end: true if the problem clearly continues AFTER this page\n\n"
#                 "RULES:\n"
#                 "- All coordinates must be PIXEL coordinates relative to THIS image.\n"
#                 "- Ignore parts that is not a problem or a solution.\n"
#                 "- Assume full image width; only vertical (Y-axis) segmentation is required.\n"
#                 "- Blocks must be returned in top-to-bottom order.\n"
#                 "- If a problem starts near the bottom and does not finish, you MUST set open_end = true."
#               )
#             },
#             {
#               "type": "image_url",
#               "image_url": {
#                 "url": f"data:image/png;base64,{to_base64(image)}"
#               }
#             }
#           ]
#         }
#       ],
#       response_format={
#         "type": "json_schema",
#         "json_schema": {
#           "name": "problem_blocks",
#           "schema": {
#             "type": "object",
#             "properties": {
#               "blocks": {
#                 "type": "array",
#                 "items": {
#                   "type": "object",
#                   "properties": {
#                     "start_y": {
#                       "type": "integer",
#                       "description": "Top Y pixel coordinate of the problem block on this page"
#                     },
#                     "end_y": {
#                       "type": "integer",
#                       "description": "Bottom Y pixel coordinate of the problem block on this page"
#                     },
#                     "open_start": {
#                       "type": "boolean",
#                       "description": "True if the problem started before this page"
#                     },
#                     "open_end": {
#                       "type": "boolean",
#                       "description": "True if the problem continues after this page"
#                     }
#                   },
#                   "required": [
#                     "start_y",
#                     "end_y",
#                     "open_start",
#                     "open_end"
#                   ]
#                 }
#               }
#             },
#             "required": ["blocks"]
#           }
#         }
#       }
#     )
#     data = json.loads(response.choices[0].message.content)
#     print(data)
#     for problem in data['blocks']:
#       print(idx, i)
#       crop = image.crop((0, problem['start_y'], image.width, problem['end_y']))
#       if problem['open_start']:
#         idx -= 1
#         prev_img = Image.open(f"./cache/{idx}.png")
#         canvas = Image.new("RGB", (crop.width, prev_img.height + crop.height), "white")
#         canvas.paste(prev_img, (0, 0))
#         canvas.paste(crop, (0, prev_img.height))
#         canvas.save(f"./cache/{idx}.png")
#       else:
#         crop.save(f"./cache/{idx}.png")
#       idx+=1
  return []

def create_tex(num, path):
  SYSTEM_PROMPT = r"""
  You are a transcription system for mathematical content.

  Your task is to extract ONLY the mathematical problems and explanations
  from the image and convert them into LaTeX fragments.

  Rules:
  - Do NOT create a full LaTeX document.
  - Do NOT use \documentclass, \begin{document}, or \end{document}.
  - Output only raw LaTeX content (equations, texts).
  - Preserve the original wording and structure as much as possible.
  - Mathematical expressions must be written in valid LaTeX.
  - Do NOT add explanations or commentary.
  - Do NOT invent content that does not appear in the image.
  """

  USER_PROMPT = r"""
  This image contains a math problem and its explanation.

  Convert ONLY the content into LaTeX fragments with the following rules:

  1. Output plain LaTeX content only (no preamble, no document environment).
  2. Keep paragraph breaks using blank lines.
  3. Inline math → only $...$
  4. Displayed equations → only $$...$$
  5. Preserve numbering like (1), (2), (a), (b) if present.
  6. Do NOT summarize, rewrite, or normalize.

  Return only the LaTeX fragment.
  """

  img = Image.open(path)
  response = client.responses.create(
    model="gpt-5.2",
    input=[
      {"role": "system", "content": [{"type": "input_text", "text": SYSTEM_PROMPT}]},
      {
        "role": "user",
        "content": [
          {"type": "input_text", "text": USER_PROMPT},
          {"type": "input_image", "image_url": f"data:image/png;base64,{to_base64(img)}"},
        ],
      },
    ],
  )
  output_path = f"./cache/{num}.tex"
  f = open(output_path,"w",encoding="UTF-8")
  f.write(response.output_text)
  return output_path