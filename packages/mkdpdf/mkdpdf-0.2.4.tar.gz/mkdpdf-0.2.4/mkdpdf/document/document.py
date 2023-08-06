import inspect
import os
import re
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mkdpdf

from mkdpdf import configuration
from mkdpdf.md.md import MD
from mkdpdf.pdf.pdf import PDF
from mkdpdf.utilities import clean

class Document:
    """
    Document is a Markdown or Portable Document Format document.
    """

    def __init__(self, title: str = None, format: str = configuration.FORMAT, filename: str = configuration.FILENAME, directory_path_output: str = configuration.DIRECTORY_PATH_OUTPUT, directory_name_templates: str = None, directory_path_templates: str = None, email_host: str = None):
        """
        Args:
            directory_path_output (string): path of output directory
            directory_path_templates (string): path of template directory
            directory_name_templates (string): directory name of sub directory inside base templates directory
            email_host (string): email domain from which to send
            filename (string): name of output file
            format (enum): md || pdf
        """

        # determine where submodule is
        # package or console script
        stack_callers = [d[1] for d in inspect.stack() if d[1].startswith("/tmp/ipykernel_") or (not d[1].endswith(".py") and d[1] != "<string>")]
        run_from_stack = len([d for d in stack_callers if "bin" not in d]) > 0

        # if running from stack
        if run_from_stack:

            stack_kernel_file = stack_callers[0]
            index_of_stack_kernel = [d[1] for d in inspect.stack()].index(stack_kernel_file)
            file_path_stack = inspect.stack()[index_of_stack_kernel - 1][1]
            directory_path_stack_caller = "/".join(file_path_stack.split("/")[0:-1])
            # determine where core templates are
            file_path_stack = inspect.stack()[index_of_stack_kernel - 2][1]
            directory_path_stack_core = "/".join(file_path_stack.split("/")[0:-1])

        else:
            directory_path_stack_core = os.path.join(mkdpdf.__path__[0], self.__class__.__name__.lower())

        # update self
        self.email_host = email_host
        self.format = format.lower()
        self.directory_path_output = directory_path_output

        # get base template directory
        directory_path_templates = directory_path_templates if directory_path_templates else  (os.path.join(directory_path_stack_caller, "templates", self.format) if run_from_stack else os.path.join(configuration.DIRECTORY_PATH_PACKAGE, self.__class__.__name__.lower(), "templates", self.format))
        self.directory_path_templates = os.path.join(directory_path_templates, directory_name_templates) if directory_name_templates else directory_path_templates
        self.directory_path_templates_core = os.path.join(directory_path_stack_core, "templates", self.format) if run_from_stack else directory_path_templates

        # initialize inheritance
        self.document = PDF(
            directory_path_templates=self.directory_path_templates
        ) if self.format == "pdf" else MD(
            directory_path_templates=self.directory_path_templates
        )

        # update self attributes dependent on the type of document
        self.filename = "%s.%s" % (
            filename if filename else self.__class__.__name__.lower(),
            self.format
        )
        self.file_path = os.path.join(self.directory_path_output, self.filename)
        self.title = title if title else self.filename.split(".%s" % self.format)[0]

    def assemble(self, main: str = None, header: str = None, footer:str = None) -> tuple:
        """
        Determine templates to generate Markdown.

        Args:
            footer (string): file path of markdown partial or partial value
            header (string): file path of markdown partial or partial value
            main (string): file path of markdown partial or partial value

        Returns:
            A tuple (footer, header, main) where each is a markdown partial representing a section of the layout.
        """

        content_footer = footer
        content_header = header
        content_main = main

        # footer
        template_footer = self.template("footer", footer)
        content_footer = self.transpile(footer, template_footer) if isinstance(footer, dict) else template_footer

        # header
        template_header = self.template("header", header)
        content_header = self.transpile(header, template_header) if isinstance(header, dict) else template_header

        # main
        template_main = self.template("main", main)

        content_main = self.transpile(main, template_main) if isinstance(main, dict) else template_main

        return (content_footer, content_header, content_main)

    def construct(self, header: str, main: str, footer: str):
        """
        Construct document.

        Args:
            footer (string): Markdown partial
            header (string): Markdown partial
            main (string): Markdown partial

        Returns:
            A variable object representing the proper render class for the format-type of document.
        """

        return self.document.construct(header, main, footer)

    def email(self, text: str, sender: str, recipients: list, html: str = None, host: str = None, subject: str = None):
        """
        Email a document in text and html formats via SMTP.

        Args:
            host (string): email domain from which to send
            html (string): html content
            recipients (list): email addresses
            sender (string): email address
            subject (string): email subject text
            text (string): text content
        """

        HOST = host if host else self.email_host
        TO = [recipients] if isinstance(recipients, str) else recipients

        # initialize message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject if subject else self.title
        msg["From"] = sender
        msg["To"] = ";".join(TO)

        # assemble content
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html if html else "<div>%s</div>" % text, "html")

        # attach content to message
        msg.attach(part1)
        msg.attach(part2)

        # send message
        server = smtplib.SMTP(HOST, port=587)
        server.starttls()
        server.login(sender, os.environ["EMAIL_PASSWORD"])
        server.sendmail(sender, TO, msg.as_string())
        server.quit()

    def generate(self, main = None, header = None, footer = None, to_file: bool = False):
        """
        Generate document.

        Args:
            footer (string || dictionary): partial or file path for footer template or key/value pairs to find/replace in package template
            header (string || dictionary): partial or file path for header template or key/value pairs to find/replace in package template
            main (string || dictionary): partial or file path for main template or key/value pairs to find/replace in package template
            to_file (boolean): TRUE if content should be written to file

        Returns:
            A string representing the full content.
        """

        # get base
        f, h, m = self.assemble(
            main=main,
            header=header,
            footer=footer
        )

        # build document
        content = self.construct(h, m, f)

        # render
        if to_file: self.render(content, self.file_path)

        return content

    def render(self, content, file_path: str):
        """
        Render document to filesystem.

        Args:
            content (string): partial of Markdown or HTML
            file_path (string): output file path
        """

        content = content if self.format != "md" else clean(content)

        self.document.render(content, file_path)

    def template(self, type: str, section) -> str:
        """
        Determine template from provided or core class template.

        Args:
            section (string || dictionary): partial or file path for template or key/value pairs to find/replace in package template
            type (enum): footer || header || main

        Returns:
            A string representing a template partial.
        """

        result = section

        # template is considered to be a string partial
        # it may or may not actually be a template with values to be replaced
        is_template = isinstance(section, str) and os.path.exists(section)

        # get core template path
        file_path = os.path.join(self.directory_path_templates, "%s.%s" % (type, configuration.TEMPLATES[self.format]))

        # provided template is valid
        if is_template:

            # get provided template path
            file_path = section if section.startswith("/") else os.path.join(os.path.dirname(__file__), section)

            # use specified template
            with open(file_path, "r") as f:

                # read into string
                result = f.read()

        # try to load template for use
        else:

            # check for template in current stack
            if os.path.exists(file_path):

                # use specified template
                with open(file_path, "r") as f:

                    # read into string
                    result = f.read()

            # check for package
            else:

                # template from mkdpdf
                file_path_core = os.path.join(self.directory_path_templates_core, "%s.%s" % (type, self.format))

                # check for core template
                if os.path.exists(file_path_core):

                    # use core template
                    with open(file_path_core, "r") as f:

                        # read into string
                        result = f.read()

        return result

    def transpile(self, section: dict, template: str) -> str:
        """
        Replace placeholders in templates with provided content.

        Args:
            section (dictionary): key/value pairs to find/replace in package template
            template (string): partial section of document

        Returns:
            A string representing a partial in the file format of the template.
        """

        result = template

        # check if subtemplates are in result
        if result and "SUBTEMPLATE_" in result:

            # get subtemplates
            subtemplates = re.findall(r"SUBTEMPLATE_.+", result)

            # loop through subtemplates
            for placeholder in subtemplates:

                # get subtemplate method
                subtemplate_method = getattr(self, placeholder)

                # generate content for subtemplate
                subtemplate = subtemplate_method(section[placeholder])

                # update reference dictionary
                section[placeholder] = subtemplate

        # loop through keys
        for key in section:

            # set replacement content
            replacement = section[key]

            # look for markdown table format when processing pdf format
            if self.format == "pdf" and "| :-- |" in section[key]:

                # convert markdown to html
                replacement = self.document.table(section[key])

            # replace in template
            result = result.replace(key, replacement)

        return result
