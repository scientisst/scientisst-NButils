import os
import json
import codecs
import argparse
import pandas as pd

from scientisstNButils.get_from_notebook import get_metadata, get_tags, get_colab_link


def get_NB_info_from_chapter(md_file, dir, master_table=True):
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

        authors, last_update = get_metadata(nb_content["cells"])
        tags = get_tags(nb_content["cells"])
        chapter = os.path.basename(dir)

        md_file.write(nb_folder + " | ")
        if master_table:
            md_file.write(chapter[0] + " | ")
        md_file.write(tags + "|")
        md_file.write(authors + "|")
        md_file.write(last_update + "|" + "\n")


def create_master_table(scientisst_nb_dir):
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
            get_NB_info_from_chapter(
                md_file, dir=os.path.join(scientisst_nb_dir, chapter)
            )


def create_chapter_tables(scientisst_nb_dir):
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

            get_NB_info_from_chapter(
                md_file,
                dir=path_chapter,
                master_table=False,
            )


def create_new_course_md(md_path, index_table):
    """[Summary]
    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """

    with open(md_path, "r") as f:
        lines = f.readlines()

    lines_strip = [l.strip() if l != "\n" else l for l in lines]
    program_start = lines_strip.index("## Program")

    content = lines[: program_start + 3]

    with open(md_path, "w") as md_file:
        md_file.write("".join(content))
        md_file.write(index_table.to_csv(sep="|", index=False, header=False))


def update_courses_tables(scientisst_nb_dir):

    """Goes through every course program and updates the metadata from the corresponding notebooks
    :param courses_dir: Path to the '_Courses' folder
    :type courses_dir: string
    """

    courses_dir = os.path.join(scientisst_nb_dir, "_Courses")

    courses_list = sorted([f for f in os.listdir(courses_dir) if f.endswith(".md")])

    for course in courses_list:

        with open(os.path.join(courses_dir, course), "r") as f:
            lines = [l.strip() for l in f.readlines() if l != "\n"]

        table_start = lines.index("## Program") + 1
        table = pd.read_table(
            os.path.join(courses_dir, course),
            sep="|",
            header=table_start,
            names=lines[table_start].split(" | "),
        )

        for ind in table.index:

            row = table.iloc[ind]

            chapter_index = [
                ch[:2]
                for ch in os.listdir(scientisst_nb_dir)
                if (
                    os.path.isdir(os.path.join(scientisst_nb_dir, ch))
                    and ch[0] != "_"
                    and ch[1] == "."
                )
            ].index(f"{row['Title'][0]}.")

            chapter_dir = os.path.join(
                scientisst_nb_dir,
                [
                    ch
                    for ch in os.listdir(scientisst_nb_dir)
                    if (
                        os.path.isdir(os.path.join(scientisst_nb_dir, ch))
                        and ch[0] != "_"
                        and ch[1] == "."
                    )
                ][chapter_index],
            )

            try:
                nb = codecs.open(
                    f"{os.path.join(chapter_dir, row['Title'].strip())}.ipynb", "r"
                )

                source = nb.read()
                nb_content = json.loads(source)

                _, last_update = get_metadata(nb_content["cells"])
                chapter = os.path.basename(chapter_dir)

                updated_row = [
                    f" {row['Title'].strip()} ",
                    f" {last_update} ",
                    f" {chapter} ",
                    f" {get_colab_link(row['Title'].strip(), chapter)} ",
                ]
                table.iloc[ind] = updated_row

            except Exception as e:
                print("\n")
                print(e)

        create_new_course_md(os.path.join(courses_dir, course), table)


def create_index_tables(scientisst_nb_dir):
    """Calls necessary fucntions to create a Master Index Table and an Index Table for each chapter.

    :param scientisst_nb_dir: Path to the root repository of the ScientISST Notebooks
    :type scientisst_nb_dir: string
    """

    create_master_table(scientisst_nb_dir)
    create_chapter_tables(scientisst_nb_dir)
    update_courses_tables(scientisst_nb_dir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "scientisst_nb_dir", help="Path to the local ScientISST Notebooks repository."
    )
    opt = parser.parse_args()

    scientisst_nb_dir = opt.scientisst_nb_dir
    create_index_tables(scientisst_nb_dir)
