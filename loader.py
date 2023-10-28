from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import PyPDFLoader

class WordParser():
    def __init__(self):
        self.module="WP"
    
    def load_docs(self, path):
        # D:\SVCE\Chatgpt\Trials\Resume_da.docx
        loader = Docx2txtLoader(path)
        data = loader.load()

        return data
    
class PDFParse():
    def __init__(self):
        self.module="PP"

    def load_docs(self, path):
        # D:\SVCE\Chatgpt\Trials\2127200501079.pdf
        loader = PyPDFLoader(path)
        data = loader.load_and_split()

        return data

class Load():
    def __init__(self):
        self.module='load'
        self.type=None

    def identify_and_load(self,path):
        type=path.split('.')[-1]

        if type=='txt':
            # "D:\SVCE\Chatgpt\Trials\jd.txt"
            file = open(path)
            data = file.read()
            file.close()

        elif type=='docx':
            wp = WordParser()
            data = wp.load_docs(path)

        elif type=='pdf':
            pp = PDFParse()
            data = pp.load_docs(path)

        return data

