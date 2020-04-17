import os
import nbformat
from nbconvert import MarkdownExporter, PDFExporter
from nbconvert.writers import FilesWriter

SUPPORTED_FORMATS = {"md", "pdf"}


class Formatter:
    def __init__(self, output):
        assert output in SUPPORTED_FORMATS, f"supported formats are {SUPPORTED_FORMATS}"
        self.read_encoding = "utf-8"
        self.write_encoding = "utf-8"
        self.format = output

        if self.format == "pdf":
            pdf = PDFExporter()
            pdf.exclude_output_prompt = True
            pdf.exclude_input = True
            self.exporter = pdf
        else:
            self.exporter = MarkdownExporter()

    def convert(self, file):
        assert os.path.exists(file), f"this should not happen, path {file} must exist"
        body, resources = self.export(file)

        fw = FilesWriter()
        fw.write(body, resources, notebook_name=file.replace(".ipynb", ""))

    def dst_path(self, file):
        return file.replace(".ipynb", f".{self.format}")

    def export(self, file):
        with open(file, "r", encoding=self.read_encoding) as f:
            nb = nbformat.read(f, as_version=4)
            body, resources = self.exporter.from_notebook_node(nb)
            return body, resources

    def needs_format(self, file):
        f_path = self.dst_path(file)

        if not os.path.exists(f_path):
            return True

        notebook_modified = os.stat(file).st_mtime
        formatted_modified = os.stat(f_path).st_mtime

        return notebook_modified > formatted_modified

    def save_figures(self, resources):
        if "outputs" not in resources:
            return

        for name, bytes_ in resources["outputs"]:
            print(f"name = {name}, bytes = {len(bytes_)}")

        for key, value in resources.items():
            pass
