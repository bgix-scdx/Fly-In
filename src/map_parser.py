from typing import Any, Dict, List
import os


def Parse_Hub(text: List[str]) -> Dict[str, Any]:
    result = {
        "name": text[1],
        "position": [int(text[2]), int(text[3])],
        "settings": {}
    }
    for val in text[4:]:
        val = val.strip("[").strip("]").split("=")
        result["settings"][val[0]] = val[1]
    return result


def Parse_File(filepath: str, name: str) -> Dict[str, Any]:
    result = {
        "map": name,
        "connections": [],
        "cells": []
    }
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            for text in lines:
                if text == "\n" or text == "":
                    continue
                split = text.split()
                if "hub" in split[0]:
                    result["cells"].append(Parse_Hub(split))
                elif "connection" in split[0]:
                    result["connections"].append(split[1].split("-"))
                elif "nb_drones" in split[0]:
                    result["nb_drones"] = int(split[1])
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
        return None
    except IsADirectoryError as e:
        print(f"Is a directory: {e.filename}")
        return None
    except NotADirectoryError as e:
        print(f"Is a not directory: {e.filename}")
        return None
    except PermissionError as e:
        print(f"No permission to open {e.filename}.")
        return None
    return result


def Loop_Through(dir: str = "maps", filename: str = "",
                 final: Dict[str, Dict[str, Any]] = {}) -> Dict[str, Any]:
    if not os.path.isdir(dir) and os.path.isfile(dir):
        try:
            final[dir] = Parse_File(dir, filename)
        except (IndexError, ValueError):
            print(f"File: {dir} is invalid !")
    elif os.path.isdir(dir):
        for _, file in enumerate(os.listdir(dir)):
            final = Loop_Through(dir + "/" + file, file)
    return final
