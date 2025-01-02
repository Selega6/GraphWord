import os
import re
from collections import Counter
from nltk.corpus import stopwords
import nltk

# Descargar los recursos necesarios de NLTK
nltk.download("stopwords")

class WordProcessor:
    def __init__(self, input_dir, output_file, lower_bound=3, upper_bound=5):
        self.input_dir = input_dir
        self.output_file = output_file
        self.stop_words = set(stopwords.words("english"))
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def process_files(self):
        if not os.path.exists(self.input_dir):
            print(f"Input directory '{self.input_dir}' does not exist.")
            return

        word_counter = Counter()

        for filename in os.listdir(self.input_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.input_dir, filename)
                if os.path.isfile(file_path):
                    print(f"Processing file: {file_path}")
                    word_counter.update(self.process_file(file_path))
        return word_counter

    def process_file(self, file_path):
        """Extract relevant words from a single file and count their frequency."""
        text = self.extract_book_content(file_path)

        # Extraer palabras alfabéticas del texto
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        # Filtrar palabras irrelevantes y por longitud
        filtered_words = [
            word for word in words
            if word not in self.stop_words and self.lower_bound <= len(word) <= self.upper_bound
        ]
        return Counter(filtered_words)

    def extract_book_content(self, file_path):
        """Extract the main content of a Gutenberg book, excluding metadata."""
        # Expresiones regulares para identificar los marcadores
        start_marker = re.compile(r"\*\*\* START OF (THE )?PROJECT GUTENBERG EBOOK", re.IGNORECASE)
        end_marker = re.compile(r"\*\*\* END OF (THE )?PROJECT GUTENBERG EBOOK", re.IGNORECASE)
        
        content_lines = []
        is_in_content = False

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                # Buscar el marcador de inicio
                if start_marker.search(line):
                    is_in_content = True
                    print("Start marker found")
                    continue  # Saltar la línea del marcador
                
                # Buscar el marcador de fin
                if end_marker.search(line):
                    is_in_content = False
                    print("End marker found")
                    break  # Terminar al encontrar el marcador de fin
                
                # Agregar líneas dentro del contenido
                if is_in_content:
                    content_lines.append(line)

        return "".join(content_lines)