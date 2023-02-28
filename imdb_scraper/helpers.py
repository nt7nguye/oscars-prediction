""" Helper functions """
import json


def pretty_print(obj: any):
    """Prints data object with JSON format


    Args:
        obj (any):
    """
    print(json.dumps(obj), indent=4)


def dict_recur_get(
    dct: dict, keys: list[str], default: any = None, verbose: bool = True
) -> any:
    """Recursive version of dict.get() that returns value on KeyError"""
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            if verbose:
                print(f"Error retrieving field {key} from {dict}")
            return default
    return dct


def list_recur_get(
    lis: list[any], index: list[int], default: any = None, verbose: bool = True
) -> any:
    """Recursive version of lis[idx] that returns value on IndexError"""
    try:
        return lis[index]
    except IndexError:
        if verbose:
            print(f"Eror trieving index {index} in list {lis}")
        return default
