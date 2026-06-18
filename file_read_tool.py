
from crewai import Tool
from unstructured.partition.auto import partition

class FileReadTool:
    @Tool("Read File Tool")
    def read_file(file_path: str) -> str:
        """Reads the content of a file given its path.
        Supports various file types including .txt, .md, .pdf, .docx.
        """
        try:
            elements = partition(filename=file_path)
            content = "\n".join([str(el) for el in elements])
            return content
        except Exception as e:
            return f"Error reading file {file_path}: {e}"
