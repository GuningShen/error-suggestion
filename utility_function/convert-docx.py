import docx

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Replace with the actual path to your .docx file
docx_path = "../input_data/tutorial-noquiz.docx"
tutorial_content = extract_text_from_docx(docx_path)
print(tutorial_content)

output_file_path = "../input_data/tutorial-noquiz.txt"
# Write the data to the specified path
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(tutorial_content)