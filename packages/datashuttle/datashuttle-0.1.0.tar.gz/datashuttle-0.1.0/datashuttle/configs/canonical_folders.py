from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config_class import Configs

from datashuttle.utils.folder_class import Folder


def get_data_type_folders(cfg: Configs) -> dict:
    """
    This function holds the canonical folders
    managed by datashuttle.

    Parameters
    ----------

    cfg : datashuttle configs dict

    Other Parameters
    ----------------

    When adding a new folder, the
    key should be the canonical key used to refer
    to the data_type in datashuttle and SWC-BIDs.

    The value is a Folder() class instance with
    the required fields

    name : The display name for the data_type, that will
        be used for making and transferring files in practice.
        This should always match the canonical name, but left as
        an option for rare cases in which advanced users want to change it.

    used : whether the folder is used or not (see make_config_file)
        if False, the folder will not be made in make_sub_folders
        even if selected.

    level : "sub" or "ses", level to make the folder at.

    Notes
    ------

    In theory, adding a new  folder should only require
    adding an entry to this dictionary. However, this will not
    update configs e.g. use_xxx. This has not been
    directly tested yet, but if it does not work when attempted
    it should be configured to from then on.
    """
    return {
        "ephys": Folder(
            name="ephys",
            used=cfg["use_ephys"],
            level="ses",
        ),
        "behav": Folder(
            name="behav",
            used=cfg["use_behav"],
            level="ses",
        ),
        "funcimg": Folder(
            name="funcimg",
            used=cfg["use_funcimg"],
            level="ses",
        ),
        "histology": Folder(
            name="histology",
            used=cfg["use_histology"],
            level="sub",
        ),
    }


def get_non_sub_names():
    """
    Get all arguments that are not allowed at the
    subject level for data transfer, i.e. as sub_names
    """
    return [
        "all_ses",
        "all_non_ses",
        "all_data_type",
        "all_ses_level_non_data_type",
    ]


def get_non_ses_names():
    """
    Get all arguments that are not allowed at the
    session level for data transfer, i.e. as ses_names
    """
    return [
        "all_sub",
        "all_non_sub",
        "all_data_type",
        "all_ses_level_non_data_type",
    ]


def get_top_level_folders():
    return ["rawdata", "derivatives"]
