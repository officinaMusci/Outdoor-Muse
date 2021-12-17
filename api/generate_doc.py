import os
import subprocess


def generate_html_doc(
    project_path:str,
    doc_path:str='',
    force:bool=False
) -> None:
    """Generates an HTML documentation folder using project docstrings"""
    doc_path = ['--output-dir', doc_path] if doc_path else []
    force = ['--force'] if force else []
    subprocess.Popen(
        [
            'pdoc',
            '--html',
            project_path
        ]
        + doc_path
        + force
    )


if __name__ == '__main__':
    app_path = os.path.dirname(os.path.realpath(__file__))
    generate_html_doc(
        app_path,
        os.path.join(
            app_path,
            'static',
            'doc'
        ),
        True
    )