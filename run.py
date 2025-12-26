from processLLM import split_problems, create_tex
from processHWP import tex_to_hwp
from datetime import datetime

# INPUT_PATH = "./input/input.pdf"
INPUT_PATH = "./input/input.png"
OUTPUT_PATH = f"./output/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.hwp"

# image_list = split_problems(INPUT_PATH)

# li = []
# for i, image in enumerate(image_list):
#   li.append(create_tex(i, image))

# li = [create_tex(1, INPUT_PATH)]
li = ["./cache/1.tex"]

tex_to_hwp(li, OUTPUT_PATH)