import re
import os
import wget

nb_cells_index = {"top_banner": 0, "tags": 2, "metadata": 3, "bottom_banner": -1}


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
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://githubtocolab.com/scientisst/notebooks/blob/master/{chapter_no_spaces}/{title_no_extension}/{title_no_spaces}.ipynb)"


def add_to_resources(url, resources_path):

    download_error = False

    url = (
        url.replace("src", "")
        .replace("=", "")
        .replace('"', "")
        .replace("'", "")
        .replace(" ", "")
    )

    url = (
        url.replace("github.com", "raw.githubusercontent.com")
        .replace("/blob", "")
        .replace("?rawtrue", "")
    )

    file_name = url.split("/")[-1]
    file_path = os.path.join(resources_path, file_name)

    if not os.path.exists(file_path):
        try:
            wget.download(url, out=file_path)
        except Exception:
            download_error = True

    relative_link = f'src="./_Resources/{file_name}"'
    if download_error:
        return None, file_path
    else:
        return relative_link, None


def replace_cell_links(cell, resources_path):

    download_errors = []

    for i, line in enumerate(cell["source"]):

        if "top-banner" not in line and "bottom-banner" not in line:
            abs_links_list = re.findall("src[ ]*=[ ]*[\"']https[^ ]*[\"']", line)

            for abs_link in abs_links_list:
                relative_link, download_error = add_to_resources(
                    abs_link, resources_path
                )

                if download_error is not None:
                    download_errors += [download_error]

                else:

                    cell["source"][i] = cell["source"][i].replace(
                        abs_link, relative_link
                    )

    if download_errors:
        print("Did not manage to download the following files:")
        print(*download_errors, sep="\n")

    return cell
