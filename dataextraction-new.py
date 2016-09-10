#!/usr/bin/env python

import logging
import json
import os
import sys

import numpy


def get_json(filepath, log):
    """
    Reads a JSON file, returns None on ValueError
    and if not a file.
    """
    parsed_json = None

    # See if it is a file and not a directory or something else
    if not os.path.isfile(file_path):
        log.warning("%s is not a file! Skipping", file_path)
        return parsed_json

    try:
        with open(filepath, "rb") as fp:
            parsed_json = json.loads(fp.read())

    except ValueError as e:
        log.error("Error reading JSON file %s. Error: %s",
                  filepath, e)

    return parsed_json


def setup_logger():
    """"
    Sets up the logger. You can pretty much ignore this method
    """
    logformat = "[%(asctime)s %(levelname)s] %(message)s"
    dateformat = "%d-%m-%y %H:%M:%S"
    logger = logging.getLogger("extraction")
    formatter = logging.Formatter(logformat)
    formatter.datefmt = dateformat
    fh = logging.FileHandler("dataextraction.log", mode="a")
    fh.setFormatter(formatter)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.propagate = False

if __name__ == "__main__":
    # Add path to reports here
    DATASET_DIR = "C:\\Users\\Kateryna\\testnow"

    # Add where you want to save the data here
    NUMPY_DATA_SAVE = "C:\\Users\\Kateryna\\data.npy"

    setup_logger()
    log = logging.getLogger("extraction")

    success_apis, fail_apis, return_codes = [], [], []
    sample_num = 0

    # Fill the lists with calls
    for sample in os.listdir(DATASET_DIR):

        file_path = os.path.join(DATASET_DIR, sample)

        try:
            # Load JSON file
            log.info("Reading file: %s", file_path)
            parsed_json = get_json(file_path, log)

            if parsed_json is None:
                log.warning("Parsed JSON was None. Skipping %s", file_path)
                continue

            # Successfully loaded, increment number
            sample_num += 1
            for n in parsed_json["behavior"]["processes"]:

                for k in n["calls"]:
                    call = k["api"]
                    if k["status"] == 1:
                        if call not in success_apis:
                            success_apis.append(call)

                    elif call not in fail_apis:
                        fail_apis.append(call)

                    if k["return_value"] not in return_codes:
                        return_codes.append(k["return_value"])

        except MemoryError as e:
            log.error("Error! %s", e)
            sys.exit(1)

    log.info("Success APIs: %s", len(success_apis))
    log.info("Fail APIs: %s", len(fail_apis))
    log.info("Return codes: %s", len(return_codes))

    data_length = len(success_apis) + len(fail_apis) + len(return_codes)

    # Create the matrix using the calculated length of all lists
    matrix = numpy.zeros((sample_num, data_length))

    log.info("Data length: %s", data_length)

    ids = 0

    try:
        for sample in os.listdir(DATASET_DIR):

            file_path = os.path.join(DATASET_DIR, sample)

            # Load JSON file again
            log.info("Reading file %s", file_path)
            parsed_json = get_json(file_path, log)

            if parsed_json is None:
                log.warning("Parsed JSON was None. Skipping %s", file_path)
                continue

            q = 0
            log.info("Adding successful APIs")
            for suc_api in success_apis:
                for n in parsed_json["behavior"]["processes"]:
                    for k in n["calls"]:
                        if suc_api in k["api"]:
                            matrix[ids][q] = matrix[ids][q] + 1
                q += 1

            log.info("Adding failed APIs")
            for fail_api in fail_apis:
                for n in parsed_json["behavior"]["processes"]:
                    for k in n["calls"]:
                        if fail_api in k["api"]:
                            matrix[ids][q] = matrix[ids][q] + 1
                q += 1

            log.info("Adding return codes")
            for code in return_codes:
                for n in parsed_json["behavior"]["processes"]:
                    for k in n["calls"]:
                        if code == k["return_value"]:
                            matrix[ids][q] = matrix[ids][q] + 1
                q += 1

            ids += 1
    finally:
        try:
            log.info("Storing numpy data in at %s", NUMPY_DATA_SAVE)
            numpy.save(NUMPY_DATA_SAVE, matrix)
        except Exception as e:
            log.error("Error writing numpy data! Trying script directory")
            numpy.save(NUMPY_DATA_SAVE, matrix)
