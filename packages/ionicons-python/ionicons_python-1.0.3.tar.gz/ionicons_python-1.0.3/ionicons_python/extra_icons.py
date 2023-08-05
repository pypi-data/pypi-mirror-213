# import os
#
# for file in [icons for icons in os.listdir("colored_icons") if not icons.endswith("py")]:
#     with open("extra_icons.py", 'a') as f:
#         f.write(f'{file.split(".")[0].replace("-", "_") + "_icon"} = load_color_icon("{file}")\n')

from ionicons_python.load_icon import load_color_icon

chatgpt_icon = load_color_icon("chatgpt.svg")
gmail_icon = load_color_icon("gmail.svg")
google_docs_icon = load_color_icon("google-docs.svg")
google_drive_icon = load_color_icon("google-drive.svg")
google_sheets_icon = load_color_icon("google-sheets.svg")
google_slides_icon = load_color_icon("google-slides.svg")
google_color_icon = load_color_icon("google_color.svg")
python_color_icon = load_color_icon("python_color.svg")
streamlit_icon = load_color_icon("streamlit.svg")
