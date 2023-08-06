import os
import re

from mkdpdf import configuration
from mkdpdf.document.document import Document
from mkdpdf.md.md import MD
from mkdpdf.pdf.pdf import PDF

class Documentation(Document):
    """
    Documentation is a Markdown or Portable Document Format document.
    """

    def __init__(self, format: str = configuration.FORMAT, filename: str = configuration.FILENAME, directory_path_output: str = configuration.DIRECTORY_PATH_OUTPUT, directory_name_templates: str = None):
        """
        Args:
            directory_name_templates (string): directory name of sub directory inside base templates directory
            directory_path_output (string): path of output directory
            filename (string): name of output file
            format (enum): md || pdf
        """

        # initialize inheritance
        super(Documentation, self).__init__(
            directory_name_templates=directory_name_templates,
            directory_path_output=directory_path_output,
            filename=filename,
            format=format
        )

    def SUBTEMPLATE_FUNCTIONS(self, functions: list) -> str:
        """
        Construct the methods section of a single markdown file.

        Args:
            functions (list): list of Python Function objects

        Returns:
             A string of markdown content for the class functions part.
        """
        return "%s%s" % (
            "### Methods%s" % configuration.GITFLAVOR_RETURN if functions[0].is_method else str(),
            configuration.GITFLAVOR_RETURN.join([
                configuration.GITFLAVOR_RETURN.join([
                    "#### _[method]_ [%s](%s)" % (
                            d.function_name,
                            "/".join([
                                d.url_git,
                                "/".join(d.object_path.split(".")[0:-1])
                            ]).rstrip("/") + "#L%s" % d.object_line
                        ) if d.is_method else "## _[function]_ [%s](%s)" % (
                            d.function_name,
                            "/".join([
                                d.url_git,
                                "/".join(d.object_path.split(".")[0:-1])
                            ]).rstrip("/") + "#L%s" % d.object_line
                        ),
                    d.docstring.description if d.docstring.description else str(),
                    "<br>".join(d.docstring.urls) if d.docstring.urls else str(),
                    configuration.GITFLAVOR_BREAK_RETURN.join([
                        "```python",
                        "from %s import %s" % (
                            ".".join(d.object_path.split(".")[0:-1]),
                            d.function_name
                        ),
                        "```"
                    ]) if not d.is_method else str(),
                    "<br>".join([
                        "**Returns**: %s" % d.docstring.returns if d.docstring.returns else str(),
                        "_**Raises**: %s_" % "; ".join([
                            ": ".join([
                                x,
                                d.docstring.raises[x]
                            ]) for x in d.docstring.raises
                        ]) if d.docstring.raises else str(),
                        "_**References**: %s_" % ", ".join([
                            x["value"] for x in d.docstring.attributes["references"]
                            ]) if d.docstring.attributes and "references" in [x.lower() for x in d.docstring.attributes] else str()
                    ]) if (d.docstring.returns or d.docstring.raises) else str(),
                    "".join([
                        configuration.GITFLAVOR_RETURN.join([
                            "##### %s" % x.title() if functions[0].is_method else "### %s" % x.title(),
                            configuration.GITFLAVOR_BREAK_RETURN.join([
                                "| label | required | type | description | default |",
                                "| :-- | :-- | :-- | :-- | :-- |",
                                configuration.GITFLAVOR_BREAK_RETURN.join([
                                    "| %s | %s | %s | %s | %s |" % (
                                        y,
                                        "✓" if d.object_params[y] == "empty" else str(),
                                        type(d.object_params[y]).__name__ if d.object_params[y] and d.object_params[y] != "empty" else (d.object_annotations[y] if d.object_annotations[y] and d.object_annotations[y] != "empty" else str()),
                                        [
                                            z for z in d.docstring.attributes[d.object_param_label]
                                            if z["key"] == y
                                        ][0]["value"] if x == d.object_param_label and len([z for z in d.docstring.attributes[d.object_param_label] if z["key"] == y]) > 0 else str(),
                                        d.object_params[y] if d.object_params[y] != "empty" else str()
                                    ) for y in d.object_params
                                ])
                            ]) if len(d.object_params) > 0 else str()
                        ]) for x in d.docstring.attributes if x != "references" and len(d.object_params) > 0
                    ]) if d.docstring.attributes else str()
                ]) for d in functions
            ])
        ) if functions else str()

    def SUBTEMPLATE_INIT(self, pyclass):
        """
        Construct the class initialization.

        Args:
            pyclass (class): Python class object

        Returns:
             A string of markdown content for the class initialization.
        """

        return "### Initialization%s" % (
            "".join([
                "%s#### %s%s%s" % (
                    configuration.GITFLAVOR_RETURN,
                    d.title(),
                    configuration.GITFLAVOR_RETURN,
                    configuration.GITFLAVOR_BREAK_RETURN.join([
                        "| label | required | type | description | default |",
                        "| :-- | :-- | :-- | :-- | :-- |",
                        configuration.GITFLAVOR_BREAK_RETURN.join([
                            "| %s | %s | %s | %s | %s |" % (
                                y,
                                "✓" if pyclass.init.object_params[y] == "empty" else str(),
                                type(pyclass.init.object_params[y]).__name__ if pyclass.init.object_params[y] and pyclass.init.object_params[y] != "empty" else (pyclass.init.object_annotations[y] if pyclass.init.object_annotations[y] and pyclass.init.object_annotations[y] != "empty" else str()),
                                [
                                    z for z in pyclass.init.docstring.attributes[pyclass.init.object_param_label]
                                    if z["key"] == y
                                ][0]["value"] if d == pyclass.init.object_param_label and len([z for z in pyclass.init.docstring.attributes[pyclass.init.object_param_label] if z["key"] == y]) > 0 else str(),
                                pyclass.init.object_params[y] if pyclass.init.object_params[y] != "empty" else str()
                            ) for y in pyclass.init.object_params
                        ])
                    ]) if len(pyclass.init.object_params) > 0 else str()
                ) for d in pyclass.init.docstring.attributes if d != "references"
            ])
        ) if pyclass.init and pyclass.init.docstring.attributes else str()
        """
            "%s % (
                ,
                "`%s`" % v["key"] if v["key"] else str(),
                "✔" if v["required"] else str(),
                "**%s**" % v["type"] if v["type"] else str(),
                "<br>".join([
                            "`%s`" % d.strip() for d in v["value"].split("|")
                        ]) if "|" in v["value"] else v["value"],
                v["default"]
            )
        """
