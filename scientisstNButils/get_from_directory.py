import os


def get_chapters_list(scientisst_nb_dir):
    """Returns the list of Notebook Chapters present in the root repository.

    :param scientisst_nb_dir: Path to the root repository of the ScientISST Notebooks
    :type scientisst_nb_dir: string

    :return: List with names of Notebook Chapters (i.e. folder names).
    :rtype: list
    """

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

    return chapters_list


def get_nb_folders_list(path_chapter):
    """Returns the list of Notebook folders present in the specified chapter directory.

    :param path_chapter: Path to a chapter directory in ScientISST Notebooks
    :type path_chapter: string

    :return: [ReturnDescription]
    :rtype: list
    """

    nb_folders_list = sorted(
        [
            f
            for f in os.listdir(path_chapter)
            if (os.path.isdir(os.path.join(path_chapter, f)) and f[0] != "_")
        ]
    )

    return nb_folders_list
