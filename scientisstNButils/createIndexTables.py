import os
import json
import codecs
import re


def remove_html(cell):
    """Removes html elements from a Markdown cell

    :param cell: Markdown cell

    :return: Cell content (aka source) without html elements
    :rtype: string
    """
    cell_content = "".join(cell["source"])
    no_html = " ".join(re.split("<.*?>(.*)<.*?>", cell_content))
    return no_html


def get_metadata(cell):
    """Finds author and date of last update of a ScientISST Notebook

    :param cell: Markdown cell containing the metadata from a ScientISST Notebook

    :return:
        - (string) - Notebook authors
        - (string) - Date of last update of the ScientISST Notebook (dd/mm/aaaa)
    :rtype: tuple
    """
    cell = remove_html(cell)
    cell = cell.split("\n")
    cell.remove("")

    authors = cell[1].split("**")[2]
    last_update = cell[5].split("**")[2].split(",")[0]

    return authors, last_update


def get_tags(cell):
    """Finds keywords/tags from a ScientISST Notebook

    :param cell: Markdown cell containing the keywords from a ScientISST Notebook

    :return: (string) - Notebook tags
    :rtype: tuple
    """
    cell = remove_html(cell)
    return "".join(cell.split("\n")[1:])


def getNBInfoFromChapter(md_file, dir, master_table=True):
    """Finds notebooks in a directory, collects relevant information from each, and writes it on the MasterTable document.

    :param md_file: Markdown file
    :type dir: File I/O

    :param dir: Path to a chapter directory in ScientISST Notebooks
    :type dir: string
    """

    nb_folders_list = sorted(
        [
            f
            for f in os.listdir(dir)
            if (os.path.isdir(os.path.join(dir, f)) and f[0] != "_")
        ]
    )

    for nb_folder in nb_folders_list:

        path_nb_folder = os.path.join(dir, nb_folder)
        f = codecs.open(f"{os.path.join(path_nb_folder, nb_folder)}.ipynb", "r")
        source = f.read()
        nb_content = json.loads(source)

        authors, last_update = get_metadata(nb_content["cells"][4])
        tags = get_tags(nb_content["cells"][3])
        chapter = os.path.basename(dir)

        md_file.write(nb_folder + " | ")
        if master_table:
            md_file.write(chapter[0] + " | ")
        md_file.write(tags + "|")
        md_file.write(authors + "|")
        md_file.write(last_update + "|" + "\n")


def createMasterTable(scientisst_nb_dir):
    """Creates a Markdown file in the ScientISST Notebooks repository with a complete index table, comprehending all existing notebooks

    :param scientisst_nb_dir: Path to the root repository of the ScientISST Notebooks
    :type scientisst_nb_dir: string
    """

    file_name = "MasterTable"

    with open(os.path.join(scientisst_nb_dir, f"{file_name}.md"), mode="w") as md_file:
        md_file.write(
            "# ScientISST Notebooks \n This table provides an overview of the complete set of notebooks made available in this repository. \n\n ## Detailed Index:  \n"
        )
        md_file.write("Notebook | Chapter | Tags | Authors | Last update \n")
        md_file.write("--- | --- | --- | --- | --- \n")

        chapters_list = sorted(
            [
                f
                for f in os.listdir(scientisst_nb_dir)
                if (
                    os.path.isdir(os.path.join(scientisst_nb_dir, f))
                    and f[0] != "_"
                    and f[1] == "."
                )
            ]
        )

        for chapter in chapters_list:
            getNBInfoFromChapter(md_file, dir=os.path.join(scientisst_nb_dir, chapter))


def createChapterTables(scientisst_nb_dir):
    """Creates a Markdown file in the each chapter directory with a complete index table, comprehending all existing notebooks from that chapter

    :param scientisst_nb_dir: Path to the root repository of the ScientISST Notebooks
    :type scientisst_nb_dir: string
    """

    file_name = "README"

    chapters_list = sorted(
        [
            f
            for f in os.listdir(scientisst_nb_dir)
            if (
                os.path.isdir(os.path.join(scientisst_nb_dir, f))
                and f[0] != "_"
                and f[1] == "."
            )
        ]
    )

    for chapter in chapters_list:

        path_chapter = os.path.join(scientisst_nb_dir, chapter)

        with open(os.path.join(path_chapter, f"{file_name}.md"), mode="w") as md_file:
            md_file.write(
                f"# {chapter} \n This table provides an overview of the complete set of notebooks made available in this chapter. \n\n ## Detailed Index:  \n"
            )
            md_file.write("Notebook  | Tags | Authors | Last update \n")
            md_file.write("---  | --- | --- | --- \n")

            getNBInfoFromChapter(
                md_file,
                dir=os.path.join(scientisst_nb_dir, chapter),
                master_table=False,
            )


def createIndexTables(scientisst_nb_dir):
    """Calls necessary fucntions to create a Master Index Table and an Index Table for each chapter.

    :param scientisst_nb_dir: Path to the root repository of the ScientISST Notebooks
    :type scientisst_nb_dir: string
    """

    createMasterTable(scientisst_nb_dir)
    createChapterTables(scientisst_nb_dir)
