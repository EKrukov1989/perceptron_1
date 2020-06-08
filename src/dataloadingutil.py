"""Module, for utility functions for loading data from file."""

import json
import pathlib


def load_train_data(str_path):
    """Load train_data from file, give out checked object.

    This functions check path, file and data-object.
    Returns error-string and checked data-object.
    """
    load_err, loaded_obj = __load_object(str_path)
    if load_err:
        return load_err, []

    data_err, data = __check_data(loaded_obj)
    if data_err:
        return data_err, []
    return None, data


def load_configuration(str_path):
    """Load configuration_data from file, give out checked object.

    This functions check path, file and structure of object.
    Returns error-string and checked object.
    """
    load_err, loaded_obj = __load_object(str_path)
    if load_err:
        return load_err, {}

    config_err, config = __check_configuration(loaded_obj)
    if config_err:
        return config_err, {}
    return None, config


def __load_object(str_path):
    """Load data-object from file, give out data-object.

    This functions check path and decode json-file.
    Returns error-string and data-object.
    """
    pathlib_path = pathlib.Path(str_path)

    path_err = __check_path(pathlib_path)
    if path_err:
        return path_err, []

    load_err, loaded_obj = __load_data_from_json(pathlib_path)
    if load_err:
        return load_err, []
    return None, loaded_obj


def __check_path(pathlib_path):
    try:
        if not pathlib_path.is_absolute():
            pathlib_path = pathlib.Path.cwd() / pathlib_path

        if not pathlib_path.exists():
            return 'The file is not exists'
        if not pathlib_path.is_file():
            return 'This is not a file'
    except OSError:
        return 'Syntax error in filename'
    return None


def __load_data_from_json(pathlib_path):
    try:
        with open(pathlib_path) as f:
            loaded_obj_out = json.load(f)
        return None, loaded_obj_out
    except json.decoder.JSONDecodeError:
        return 'The file is corrupted', {}


def __check_data(loaded_obj):
    if 'Data' not in loaded_obj:
        return 'The file has no "Data"', []
    data = loaded_obj['Data']
    if type(data) is not list:
        return 'The file has no "Data"', []

    def valid(x): return (x >= -1.0 and x <= 1.0)

    for i, sample in enumerate(data):
        if (len(sample) != 2):
            return 'Wrong number of elements in sample ' + str(i), []
        if (type(sample[0]) != float) or (type(sample[1]) != float):
            return 'Wrong type of element in sample ' + str(i), []
        if not valid(sample[0]) or not sample[1]:
            return 'Wrong range of element in sample ' + str(i), []
        if not valid(sample[0]) or not sample[1]:
            return 'Wrong range of element in sample ' + str(i), []
    return None, data


def __check_configuration(loaded_obj):
    if 'Data' not in loaded_obj:
        return 'The file has no "Data"', []
    data = loaded_obj['Data']
    if type(data) is not list:
        return 'The file has no "Data"', []

    def valid(x): return (x >= -1.0 and x <= 1.0)

    for i, sample in enumerate(data):
        if (len(sample) != 2):
            return 'Wrong number of elements in sample ' + str(i), []
        if (type(sample[0]) != float) or (type(sample[1]) != float):
            return 'Wrong type of element in sample ' + str(i), []
        if not valid(sample[0]) or not sample[1]:
            return 'Wrong range of element in sample ' + str(i), []
        if not valid(sample[0]) or not sample[1]:
            return 'Wrong range of element in sample ' + str(i), []
    return None, data
