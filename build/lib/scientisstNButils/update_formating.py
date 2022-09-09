import os
import sys
import json
import codecs
import argparse

from scientisstNButils.get_from_directory import get_chapters_list, get_nb_folders_list
from scientisstNButils.get_from_notebook import replace_cell_links

# from get_from_directory import get_chapters_list, get_nb_folders_list
# from get_from_notebook import replace_cell_links


def links_to_relative(scientisst_nb_dir):
    """Updates all absolute links (images and documents) to relative links for all notebooks. If _Resources folder does not exist, it is created.

    :param scientisst_nb_dir: Path to the root repository of the ScientISST Notebooks
    :type scientisst_nb_dir: string
    """

    chapters_list = get_chapters_list(scientisst_nb_dir)

    for chapter in chapters_list:

        path_chapter = os.path.join(scientisst_nb_dir, chapter)
        nb_folders_list = get_nb_folders_list(path_chapter)

        for nb_folder in nb_folders_list:
            path_nb_folder = os.path.join(path_chapter, nb_folder)

            f = codecs.open(f"{os.path.join(path_nb_folder, nb_folder)}.ipynb", "r")
            source = f.read()
            nb_content = json.loads(source)

            for i, cell in enumerate(nb_content["cells"]):
                cell = replace_cell_links(
                    cell, os.path.join(path_nb_folder, "_Resources")
                )
                nb_content["cells"][i] = cell

            new_source = json.dumps(nb_content)
            with open(
                f"{os.path.join(path_nb_folder, nb_folder)}.ipynb", "w"
            ) as outfile:
                outfile.write(new_source)


def links_to_relative_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        dest="scientisst_nb_dir",
        help="Path to the local ScientISST Notebooks repository.",
    )
    opt = parser.parse_args()
    scientisst_nb_dir = opt.scientisst_nb_dir

    links_to_relative(scientisst_nb_dir)
