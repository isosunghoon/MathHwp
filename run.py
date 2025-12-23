from processLLM import split_problems, create_tex
from processHWP import tex_to_hwp

INPUT_PATH = "./input/input.pdf"
OUTPUT_PATH = "./input/output.pdf"

image_list = split_problems(INPUT_PATH)

li = []
for i, image in enumerate(image_list):
  li.append(create_tex(i, image))

tex_to_hwp(li, OUTPUT_PATH)