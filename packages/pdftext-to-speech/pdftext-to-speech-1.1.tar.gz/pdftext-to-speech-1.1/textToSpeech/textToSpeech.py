import requests
import os
import PyPDF2


class Audio:

    def __init__(self, audio_filename, output_directory=""):
        self.audio_filename = audio_filename
        self.output_directory = output_directory

    def save_audio_file(self, audio_content):
        try:
            if not os.path.exists(self.output_directory) and self.output_directory != "":
                os.makedirs(self.output_directory)

            audio_path = os.path.join(self.output_directory, self.audio_filename)

            with open(audio_path, 'wb') as audio_file:
                audio_file.write(audio_content)

            return {"success" : True, "message" : "File saved successfully"}
        except Exception as err:
            return {"success": False, "message": err}


class AudioRequest:
    def __init__(self, url, querystring, headers):
        self.url = url
        self.querystring = querystring
        self.headers = headers

    def request_audio_data(self):
        response = requests.get(self.url, headers=self.headers, params=self.querystring)
        response.raise_for_status()
        return response.content

class File:
    def __init__(self, file_name, working_dir=""):
        self.file_name = file_name
        self.working_dir = working_dir

    def read_file(self):

        allowed_files = [".txt", ".pdf"]

        file_type = self.get_file_type(self.file_name)

        if file_type in allowed_files:

            file_path = os.path.join(self.working_dir, self.file_name)

            if file_type.lower() == ".pdf":

                with open(file_path, 'rb') as file:
                    # Create a PDF reader object
                    pdf_reader = PyPDF2.PdfReader(file)

                    # Initialize an empty string to store the text
                    text = ''

                    # Iterate over each page in the PDF
                    for page_num in range(len(pdf_reader.pages)):
                        # Extract the text from the current page
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()

                    # Return the extracted text
                    return {
                        "success": True,
                        "message": f"Pdf successfully read",
                        "txt": text
                    }
            elif file_type.lower() == ".txt":
                with open(file_path, 'r') as file:
                    text = file.read()
                    return {
                        "success": True,
                        "message": f"Text file successfully read",
                        "txt": text
                    }

        else:
            return {
                "success" : False,
                "message" : f"Please provide a file with the folliwing formats: {';'.join(allowed_files)}",
                "txt" : ""
            }


    @staticmethod
    def get_file_type(filename):
        _, file_extension = os.path.splitext(filename)
        return file_extension
