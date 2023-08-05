"""
Auxiliary methods for streamed data.
"""

import json
import logging
from time import sleep
from typing import List

import requests
import sseclient  # pylint: disable=import-error
from tqdm import tqdm

logger = logging.getLogger(__name__)


# TODO: the need of split this function in 3 different ones shows some problem in the API.
# Refactor into one, possibly with one decorator with the progress bar on its own.
# TODO: the 0.1 second sleep is masking the "real" speed and should be avoided.

# TODO (Robert): stream.receive_entities() - the progress bar updates fairly infrequently due
# to if len_results % 50 == 0:.  this will only update if the len of results is exactly a
# multiple of 50.  Why not update on every event?


def receive_entities(response: requests.models.Response, progress_bar: bool = False) -> List[any]:
    """
    Helper function to parse clients events as entities and optionally show the progress bar.
    """
    client = sseclient.SSEClient(response)
    results = []
    if progress_bar:
        previous = 0
        for event in (pbar := tqdm(client.events())):  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results += [json.loads(event.data)]
                len_results = len(results)
                if len_results != previous and len_results % 50 == 0:
                    previous = len(results)
                    pbar.set_description(f"Collecting {previous} records")
                    sleep(0.1)  # to avoid Google Colab being overwhelmed
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    else:
        for event in client.events():  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results += [json.loads(event.data)]
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    return results


def receive_history(response: requests.models.Response, progress_bar: bool = False) -> List[any]:
    """
    Helper function to parse clients events as history and optionally show the progress bar.
    """
    client = sseclient.SSEClient(response)
    results = []
    if progress_bar:
        previous = 0
        for event in (pbar := tqdm(client.events())):  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results += json.loads(event.data)
                len_results = len(results)
                if len_results != previous and len_results % 50 == 0:
                    previous = len(results)
                    pbar.set_description(f"Collecting {previous} records")
                    sleep(0.1)
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    else:
        for event in client.events():  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results += json.loads(event.data)
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    return results


def receive_count(response: requests.models.Response, progress_bar: bool = False) -> List[any]:
    """
    Helper function to parse clients events as counts and optionally show the progress bar.
    """
    client = sseclient.SSEClient(response)
    if progress_bar:
        previous = 0
        for event in (pbar := tqdm(client.events())):  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results = json.loads(event.data)
                if results != previous and results % 50 == 0:
                    previous = results
                    # Comment from Robert:
                    # receive_count isn't collecting records, it's collecting a count of records.
                    # Each result is a cumulative sum, so each result is the number of records
                    # found up to that point.  I might suggest the description be changed to
                    # something like f"{previous} records"
                    pbar.set_description(f"Collecting {previous} records")

                    # Rob: something could possibly be done to switch to using from tqdm.notebook import tqdm
                    sleep(0.1)
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    else:
        for event in client.events():  # pylint: disable=no-member
            if event.event == "keepAlive":
                continue
            if event.event == "finish":
                break
            if event.event == "message":
                results = json.loads(event.data)
                continue
            logger.error("Unexpected event in bagging area: %s", str(event))
            return None
    return results
