import os
import nbformat
from nbconvert import MarkdownExporter, PDFExporter, RSTExporter
from nbconvert.writers import FilesWriter

SUPPORTED_FORMATS = {"md", "pdf", "rst"}


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
        elif self.format == "rst":
            self.exporter = RSTExporter()
        else:
            self.exporter = MarkdownExporter()

    def convert(self, file):
        assert os.path.exists(file), f"this should not happen, path {file} must exist"
        body, resources = self.export(file)

        fw = FilesWriter()
        fw.build_directory = os.path.dirname(file)
        f_name = os.path.basename(file).replace(".ipynb", "")
        fw.write(body, resources, notebook_name=f_name)

    def dst_path(self, file):
        return file.replace(".ipynb", f".{self.format}")

    def export(self, file):
        with open(file, "r", encoding=self.read_encoding) as f:
            nb = nbformat.read(f, as_version=4)
            body, resources = self.exporter.from_notebook_node(nb)
            return self.replace_image_names(body, resources, file)

    def replace_image_names(self, body, resources, file):
        f_name = os.path.basename(file).replace(".ipynb", "")
        names = resources["outputs"].keys()
        new_outputs = {}

        for i, old_key in enumerate(names):
            _, image_extension = os.path.splitext(old_key)
            output_name = f"{f_name}_{i}{image_extension}"
            new_outputs[output_name] = resources["outputs"][old_key]
            body = body.replace(old_key, output_name)

        resources["outputs"] = new_outputs
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
