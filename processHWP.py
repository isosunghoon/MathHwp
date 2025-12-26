import pyhwpx
import re
import pypandoc

def add_eq(hwp,eq):
  PATH = "./cache/temp.mml"
  html = pypandoc.convert_text("$$"+eq+"$$", to="html", format="latex", extra_args=["--mathml"])
  mathml = re.search(r"<math[\s\S]*?</math>", html).group()
  open(PATH,"w",encoding='UTF-8').write(mathml)
  hwp.import_mathml(PATH)

def preprocess(data):
  parts = data.split("$$")
  out = []
  for i, part in enumerate(parts):
    if i % 2 == 0:
      out.append(part)
    else:
      expr = part.strip()
      expr = expr.replace("\n", "")
      out.append(f"$${expr}$$")

  return "".join(out).split("\n")

def tex_to_hwp(files, output):
  hwp = pyhwpx.Hwp()
  open(output,"w").close()
  hwp.open(output)

  for file_path in files:
    data = open(file_path, encoding="UTF-8").read()
    data = preprocess(data)

    add_eq(hwp,"")

    for line in data:
      if line.startswith("$$"):
        hwp.ParagraphShapeAlignCenter()
        add_eq(hwp, line[2:-2])
        hwp.insert_text(" ")
      else:
        hwp.ParagraphShapeAlignLeft()
        for i, part in enumerate(line.split("$")):
          if i%2==0:
            hwp.insert_text(part)
          else:
            add_eq(hwp,part)
      
      print(line)
      hwp.BreakPara()