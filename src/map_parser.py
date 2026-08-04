from typing import Any, Dict, List
import os


def Parse_Hub(text: List[str]) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "name": text[1],
        "position": [int(text[2]), int(text[3])],
        "settings": {}
    }
    for val in text[4:]:
        value = val.strip("[").strip("]").split("=")
        result["settings"][value[0]] = value[1]
    return result


def Parse_Connection(text: List[str]) -> Dict[str, Any]:
    connection = text[1].split("-")
    max_drones = 1
    if len(text) > 2:
        max_drones = int(text[2].split("=")[1].split("]")[0])
    return {"connection": connection, "max_drone": max_drones}


def Parse_File(filepath: str, name: str) -> Dict[str, Any] | None:
    result: Dict[str, Any] = {
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
                splittxt = text.split()
                if "hub" in splittxt[0]:
                    result["cells"].append(Parse_Hub(splittxt))
                elif "connection" in splittxt[0]:
                    result["connections"].append(Parse_Connection(splittxt))
                elif "nb_drones" in splittxt[0]:
                    result["nb_drones"] = int(splittxt[1])
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
                 final: Dict[str, Dict[str, Any] | None] = {}
                 ) -> Dict[str, Any]:
    if not os.path.isdir(dir) and os.path.isfile(dir):
        try:
            final[dir] = Parse_File(dir, filename)
        except (IndexError, ValueError):
            print(f"\033[38;2;255;255mFile: {dir} is invalid !\033[0m")
    elif os.path.isdir(dir):
        for _, file in enumerate(os.listdir(dir)):
            final = Loop_Through(dir + "/" + file, file)
    return final
