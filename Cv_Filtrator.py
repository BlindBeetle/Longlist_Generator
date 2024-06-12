import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import docx
from PyPDF2 import PdfReader
import openai

# Import API key from config.py
try:
    from config import OPENAI_API_KEY
    openai.api_key = OPENAI_API_KEY
except ImportError:
    raise ValueError("No OpenAI API key found. Please create a config.py file with your OpenAI API key.")

def text_extract_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Unable to read PDF file: {file_path}, {str(e)}")
    return text

def text_extract_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        print(f"Unable to read DOCX file: {file_path}, {str(e)}")
        text = ""
    return text

def extract_criteria(file_path):
    print(f"Getting criteria from: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Criteria file not found at {file_path}")

    if file_path.endswith('.pdf'):
        criteria_text = text_extract_pdf(file_path)
    else:
        raise ValueError("Unsupported file type. Please provide a PDF file.")
    
    if not criteria_text:
        raise ValueError(f"Failed to get text from Criteria.pdf: {file_path}")
    
    return criteria_text

def openai_filtration(cv_text, criteria_text):
    prompt = (
        "Check if the following resume matches the given criteria:\n\n"
        f"Resume:\n{cv_text}\n\n"
        f"Criteria:\n{criteria_text}\n\n"
        "Answer 'yes' or 'no' and explain briefly why."
    )
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=70  # Normal amount = 50
    )
    answer = response.choices[0].text.strip().lower()
    return 'yes' in answer

def extract_cvs(cv_directory):
    cvs = []
    for filename in os.listdir(cv_directory):
        file_path = os.path.join(cv_directory, filename)
        if filename.endswith('.pdf'):
            cv_text = text_extract_pdf(file_path)
        elif filename.endswith('.docx'):
            cv_text = text_extract_docx(file_path)
        else:
            continue
        if cv_text:
            cvs.append((filename, cv_text))
    return cvs

def filter_cvs(cvs, criteria_text):
    matching_cvs = []
    for filename, cv_text in cvs:
        if openai_filtration(cv_text, criteria_text):
            matching_cvs.append(filename)
    return matching_cvs

def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]

# GUI application class
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CV Filtration")

        # Criteria file selection
        self.criteria_label = ttk.Label(root, text="Select Criteria File (PDF):")
        self.criteria_label.pack(pady=5)

        self.criteria_button = ttk.Button(root, text="Browse", command=self.select_criteria_file)
        self.criteria_button.pack(pady=5)

        self.criteria_file_path = tk.StringVar()
        self.criteria_file_entry = ttk.Entry(root, textvariable=self.criteria_file_path, width=50)
        self.criteria_file_entry.pack(pady=5)

        # CV files selection
        self.cvs_label = ttk.Label(root, text="Select CV Files (PDF or DOCX):")
        self.cvs_label.pack(pady=5)

        self.cvs_button = ttk.Button(root, text="Browse", command=self.select_cv_files)
        self.cvs_button.pack(pady=5)

        self.cvs_files_list = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50)
        self.cvs_files_list.pack(pady=5)

        # Process button
        self.process_button = ttk.Button(root, text="Process", command=self.process_files)
        self.process_button.pack(pady=10)

        # Results label
        self.results_label = ttk.Label(root, text="Matching CVs:")
        self.results_label.pack(pady=5)

        # Results list
        self.results_list = tk.Listbox(root, width=50)
        self.results_list.pack(pady=5)

    def select_criteria_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.criteria_file_path.set(file_path)

    def select_cv_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf"), ("DOCX files", "*.docx")])
        if files:
            self.cvs_files_list.delete(0, tk.END)
            for file in files:
                self.cvs_files_list.insert(tk.END, file)

    def process_files(self):
        criteria_path = self.criteria_file_path.get()
        if not criteria_path:
            messagebox.showerror("Error", "Please select a criteria file.")
            return

        cv_files = self.cvs_files_list.get(0, tk.END)
        if not cv_files:
            messagebox.showerror("Error", "Please select at least one CV file.")
            return

        try:
            criteria_text = extract_criteria(criteria_path)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to extract criteria: {str(e)}")
            return

        cvs = []
        for file_path in cv_files:
            if file_path.endswith('.pdf'):
                cv_text = text_extract_pdf(file_path)
            elif file_path.endswith('.docx'):
                cv_text = text_extract_docx(file_path)
            else:
                continue
            cvs.append((os.path.basename(file_path), cv_text))

        try:
            intersected_cvs = None
            for i in range(1, 4):
                matching_cvs = filter_cvs(cvs, criteria_text)
                if i == 1:
                    intersected_cvs = matching_cvs
                else:
                    intersected_cvs = intersection(intersected_cvs, matching_cvs)
            
            self.results_list.delete(0, tk.END)
            for cv in intersected_cvs:
                self.results_list.insert(tk.END, cv)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Main entry point
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()


