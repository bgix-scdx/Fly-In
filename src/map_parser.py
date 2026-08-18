from typing import Any, Dict, List
import os


def Parse_Hub(text: List[str], RawMap: Dict[str, Any]) -> Dict[str, Any]:
    '''Get all valid info from a hub'''
    result: Dict[str, Any] = {
        "name": text[1],
        "position": [int(text[2]), int(text[3])],
        "settings": {}
    }
    for val in text[4:]:
        if '#' in val:
            continue
        value = val.strip("[").strip("]").split("=")
        result["settings"][value[0]] = value[1]
    if "start_hub" in text[0] and not RawMap.get("StartingCell"):
        RawMap["StartingCell"] = text[1]
    elif "end_hub" in text[0] and not RawMap.get("EndingCell"):
        RawMap["EndingCell"] = text[1]
    return result


def Parse_Connection(text: List[str]) -> Dict[str, Any]:
    '''Get all valid info from a connection'''
    connection = text[1].split("-")
    max_drones = 1
    if len(text) > 2:
        max_drones = int(text[2].split("=")[1].split("]")[0])
    return {"connection": connection, "max_drone": max_drones}


def Parse_File(filepath: str, name: str) -> Dict[str, Any] | None:
    '''Parse the file to store all info like droneshubs'''
    ''' and handle errors related to json'''
    result: Dict[str, Any] = {
        "map": name,
        "connections": [],
        "cells": [],
        "StartingCell": None,
        "EndingCell": None
    }
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            for text in lines:
                if text[0] == '#':
                    continue
                if text == "\n" or text == "":
                    continue
                splittxt = text.split()
                if "hub" in splittxt[0]:
                    result["cells"].append(Parse_Hub(splittxt, result))
                elif "connection" in splittxt[0]:
                    result["connections"].append(Parse_Connection(splittxt))
                elif "nb_drones" in splittxt[0]:
                    if int(splittxt[1]) >= 100:
                        print("\033[38;2;255mDrone numbers must "
                              "be inferior to 100.\033[0m")
                        return None
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
    if not result.get("StartingCell") or not result.get("EndingCell"):
        print(f"\033[38;2;255mMap {name} need a start and an "
              "end (start_hub | end_hub)\033[0m")
        return None
    return result


def Loop_Through(dir: str = "maps", filename: str = "",
                 final: Dict[str, Dict[str, Any] | None] = {}
                 ) -> Dict[str, Any]:
    '''Loop through all map in the files to store and return them as a dict'''
    if not os.path.isdir(dir) and os.path.isfile(dir):
        try:
            if ".txt" not in filename:
                return final
            final[dir] = Parse_File(dir, filename)
        except (IndexError, ValueError):
            print(f"\033[38;2;255;255mFile: {dir} is invalid !\033[0m")
    elif os.path.isdir(dir):
        for _, file in enumerate(os.listdir(dir)):
            final = Loop_Through(dir + "/" + file, file)
    return final
