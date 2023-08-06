from mkdpdf import configuration
from mkdpdf.document.document import Document

class Report(Document):
    """
    Report is a time-bound document.
    """

    def __init__(self, date_publish:str = configuration.DATE_PUBLISH, format: str = configuration.FORMAT, filename: str = configuration.FILENAME, directory_path_output: str = configuration.DIRECTORY_PATH_OUTPUT, directory_path_templates: str = None):
        """
        Args:
            date_publish (string): 8601 date value
            directory_path_output (string): path of output directory
            directory_path_templates (string): path of template directory
            filename (string): name of output file
            format (enum): md || pdf
        """
        # update self
        self.date_publish = date_publish

        # initialize inheritance
        super(Report, self).__init__(
            directory_path_output=directory_path_output,
            directory_path_templates=directory_path_templates,
            filename=filename,
            format=format
        )
