import os
from typing import Union
from typing_extensions import Literal
from string import Template
import pickle
import subprocess
from matplotlib.colors import BoundaryNorm
import pandas as pd
from pandas.core import base
import seaborn as sns
import matplotlib

# the best image type for each file type
image_types = {"html": "png", "htm": "png", "pdf": "eps"}


class Manager:
    def __init__(
        self,
        template: Union[str],
        context: Union[dict, str, None] = None,  # in memory context dict also supported
        assets_directory: str = "assets",
    ) -> None:
        self._template = template
        _template_splitname = self._template.split(".")
        _template_basename = ".".join(_template_splitname[:-1])
        _template_extension = _template_splitname[-1]
        if context is None:
            self._context = _template_basename + ".pkl"
        else:
            self._context = context
        if _template_extension != "md":
            raise Exception("Only markdown (.md) template types are supported.")
        self._rendered_markdown_file_name = "_" + self._template
        self._pdf_ouput_file_name = _template_basename + ".pdf"
        self._html_ouput_file_name = _template_basename + ".html"
        self._assets_directory = assets_directory
        if isinstance(self._context, str):
            self._context_file_type = self._context.split(".")[-1]
            assert (
                self._context_file_type == "pkl"
            ), "Only pkl context file types are currently supported"
        if not os.path.isdir(self._assets_directory):
            os.mkdir(self._assets_directory)

    def get_context(self):
        # if string, then it's serialized as pkl
        if isinstance(self._context, str):
            if self._context_file_type == "pkl":
                with open(self._context, "rb") as fn:
                    pickle_data = fn.read()
                return pickle.loads(pickle_data)
            else:
                raise Exception("Only .pkl context files are supported")
        else:
            return self._context

    def save_context(self, context_dict, append=False):
        # if string, then it's serialized as pkl
        if isinstance(self._context, str):
            if self._context_file_type == "pkl":
                if append:
                    with open(self._context, "rb") as fn:
                        _context_to_update = pickle.loads(fn.read())
                    _context_to_update.update(context_dict)
                    with open(self._context, "wb") as fn:
                        fn.write(pickle.dumps(_context_to_update))
                else:
                    with open(self._context, "wb") as fn:
                        fn.write(pickle.dumps(context_dict))
                return self._context  # return file name
            else:
                raise Exception("Only .pkl context files are supported")
        else:
            raise Exception(
                "Cannot save.  This Manager instance isn't using a pickle context file."
            )

    def _render_pandas_dataframe(self, df: pd.DataFrame, caption: str) -> str:
        md_string = df.to_markdown(index=False, numalign="center", stralign="center")
        # https://tex.stackexchange.com/questions/139106/referencing-tables-in-pandoc
        md_string += "\n\nTable: " + caption.replace("_", " ").title() + "\n\n"
        return md_string

    def _render_matplotlib_figure(  # and seaborn
        self,
        figure: Union[sns.axisgrid.FacetGrid, matplotlib.figure.Figure],
        caption: str,
        image_file_type: str,
    ) -> str:
        # returns a string, but ALSO saves the image to assets directory
        temp_file = (
            f"{self._assets_directory}/{caption.replace(' ','_')}.{image_file_type}"
        )
        figure.savefig(temp_file)
        md_string = f"![{caption.replace('_', ' ').title()}]({temp_file})"
        return md_string

    def _render_all_to_markdown(self, image_type: Literal["eps", "png"]):
        stringified_context = {}
        for label, value in self.get_context().items():
            if type(value) in [sns.axisgrid.FacetGrid, matplotlib.figure.Figure]:
                md_string = self._render_matplotlib_figure(value, label, image_type)
                stringified_context.update({label: md_string})
            elif type(value) == pd.DataFrame:
                md_string = self._render_pandas_dataframe(value, label)
                stringified_context.update({label: md_string})
            else:
                stringified_context.update({label: value})
        with open(self._template, "r") as fn:
            template_string = fn.read()
        template_object = Template(template_string)
        # safe_substitute allows you to include dollar signs
        rendered = template_object.safe_substitute(stringified_context)
        return rendered

    def _save_rendered_markdown_file(self, report_type: Literal["pdf", "html"]):
        with open(self._rendered_markdown_file_name, "w") as fn:
            fn.write(self._render_all_to_markdown(image_types[report_type]))
        return self._rendered_markdown_file_name

    def save_to_pdf(self) -> None:
        # converts markdown file to pdf file
        markdown_filename = self._save_rendered_markdown_file("pdf")
        subprocess.run(
            f"pandoc {markdown_filename} --pdf-engine xelatex -o {self._pdf_ouput_file_name}",
            shell=True,
            check=True,
        )

    def _render_to_html_body(self) -> str:
        # converts markdown file to html-body and then returns the body
        _markdown_filename = self._save_rendered_markdown_file("html")
        subprocess.run(  # markdown to html
            # f"pandoc --toc --standalone --css {latex_css} --css {syntaxhighlighting_css} {_markdown_filename} -o {self._html_ouput_file_name}",
            f"pandoc --toc --standalone --mathjax {_markdown_filename} -o {self._html_ouput_file_name}",
            shell=True,
            check=True,
        )
        with open(self._html_ouput_file_name, "r") as fn:
            pandoc_html = fn.read()
        return pandoc_html

    def save_to_html(self) -> str:
        mathjax_script = '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
        # https://latex.vercel.app/
        latex_css = '<link rel="stylesheet" href="https://latex.now.sh/style.css">'
        # mathjax_script = '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
        syntaxhighlighting_css = (
            '<link rel="stylesheet" href="https://latex.now.sh/prism/prism.css">'
        )
        syntaxhighlighting_script = (
            '<script src="https://cdn.jsdelivr.net/npm/prismjs/prism.min.js"></script>'
        )
        browsersync_script = """<script id="__bs_script__">//<![CDATA[
            document.write("<script async src='http://HOST:3000/browser-sync/browser-sync-client.js?v=2.26.14'><\/script>".replace("HOST", location.hostname));
        //]]></script>
        """
        css = [latex_css, syntaxhighlighting_css]
        # pandoc --css seems to place the css at the bottom of <head>
        scripts = [syntaxhighlighting_script, browsersync_script]  # pandoc does mathjax
        rendered = self._render_to_html_body()
        rendered = rendered.replace("<head>", "<head>\n" + "\n".join(css))
        # rendered = rendered.replace("</head>", "\n".join(css) + "\n</head>") # option 2
        rendered = rendered.replace("</body>", "\n".join(scripts) + "\n</body>")
        with open(f"{self._html_ouput_file_name}", "w") as fn:
            fn.write(rendered)
        return self._html_ouput_file_name


if __name__ == "__main__":
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "template", type=str, help="The template file path (md)",
    )
    args = parser.parse_args()
    splitname = args.template.split(".")
    basename = ".".join(splitname[:-1])
    extension = splitname[-1]
    if not os.path.isfile(basename + ".pkl"):
        print(f"{basename}.pkl not found.  Creating an empty context file...")
        with open(f"{basename}.pkl", "wb") as fn:
            fn.write(pickle.dumps({}))
    else:
        with open(f"{basename}.pkl", "rb") as fn:
            pickle_data = pickle.loads(fn.read())
        if len(pickle_data) == 0:
            print(
                f"[WARNING] {basename}.pkl contains no data.  Use pantex.Manager.save_context to create context."
            )
    m = Manager(args.template)
    m.save_to_pdf()
