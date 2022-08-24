import re
import os

nb_cells_index = {"tags": 3, "metadata": 4}


def remove_html(cell):
    """Removes html elements from a Markdown cell

    :param cell: Markdown cell

    :return: Cell content (aka source) without html elements
    :rtype: string
    """
    cell_content = "".join(cell["source"])
    no_html = " ".join(re.split("<.*?>(.*)<.*?>", cell_content))
    return no_html


def get_metadata(cells):
    """Finds author and date of last update of a ScientISST Notebook

    :param cell: Markdown cell containing the metadata from a ScientISST Notebook

    :return:
        - (string) - Notebook authors
        - (string) - Date of last update of the ScientISST Notebook (dd/mm/aaaa)
    :rtype: tuple
    """
    cell = remove_html(cells[nb_cells_index["metadata"]])
    cell = cell.split("\n")
    cell.remove("")

    authors = cell[1].split("**")[2]
    last_update = cell[5].split("**")[2].split(",")[0]

    return authors, last_update


def get_tags(cells):
    """Finds keywords/tags from a ScientISST Notebook

    :param cell: Markdown cell containing the keywords from a ScientISST Notebook

    :return: (string) - Notebook tags
    :rtype: tuple
    """
    cell = remove_html(cells[nb_cells_index["tags"]])
    return "".join(cell.split("\n")[1:])


def get_colab_link(title, chapter):
    """Returns the link to open the Notebook using Google Colab.
    :param title: Title of Notebook.
    :type title: string

    :param chapter: Name of chapter where Notebook is included.
    :type chapter: string

    :return: [ReturnDescription]
    :rtype: string
    """

    title_no_spaces = title.replace(" ", "%20")
    title_no_extension = os.path.splitext(title_no_spaces)[0]
    chapter_no_spaces = chapter.replace(" ", "%20")
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/scientisst/notebooks/blob/master/{chapter_no_spaces}/{title_no_extension}/{title_no_spaces})"
