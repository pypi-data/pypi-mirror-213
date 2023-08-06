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


class DFIResponseError(Exception):
    "Raised when there's an error propagated back from the HTTP API"


class DFIResponseWarning(Warning):
    "Raised when there's an error propagated back from the HTTP API"


def raise_query_error_event(event: sseclient.Event) -> None:
    """helper to raise a QueryError response error"""
    msg = f"event returned QueryError: {event.data}"
    logger.error(msg)
    raise DFIResponseError(msg)


def raise_unexpected_event_found(event: sseclient.Event) -> None:
    """helper to raise a an unexpected event was found"""
    msg = f"Unexpected event in bagging area: {event}"
    logger.error(msg)
    raise DFIResponseError(msg)


def raise_message_event_not_reached() -> None:
    """helper to raise a warning if the "message" event was not reached."""
    msg = "No response from DFI API for the given query"
    logger.warning(msg)
    raise DFIResponseWarning(msg)


def receive_entities(response: requests.models.Response, progress_bar: bool = False) -> List[any]:
    """
    Helper function to parse clients events as entities and optionally show the progress bar.
    """
    client = sseclient.SSEClient(response)
    results = []
    result_received = False
    previous = 0

    for event in (pbar := tqdm(client.events(), disable=not progress_bar)):  # pylint: disable=no-member
        if event.event == "keepAlive":
            continue
        elif event.event == "finish":
            break
        elif event.event == "message":
            result_received = True
            results += [json.loads(event.data)]

            if progress_bar:
                len_results = len(results)
                if len_results != previous and len_results % 50 == 0:
                    previous = len(results)
                    pbar.set_description(f"Collecting {previous} records")
                    sleep(0.1)  # to avoid Google Colab being overwhelmed

            continue
        elif event.event == "queryError":
            raise_query_error_event(event)
        else:
            raise_unexpected_event_found(event)

    if not result_received:
        raise_message_event_not_reached()
    return results


def receive_history(response: requests.models.Response, progress_bar: bool = False) -> List[any]:
    """
    Helper function to parse clients events as history and optionally show the progress bar.
    """
    client = sseclient.SSEClient(response)
    results = []
    result_received = False
    previous = 0

    for event in (pbar := tqdm(client.events(), disable=progress_bar)):  # pylint: disable=no-member
        if event.event == "keepAlive":
            continue
        elif event.event == "finish":
            break
        elif event.event == "message":
            result_received = True
            results += json.loads(event.data)

            if progress_bar:
                len_results = len(results)
                if len_results != previous and len_results % 50 == 0:
                    previous = len(results)
                    pbar.set_description(f"Collecting {previous} records")
                    sleep(0.1)  # to avoid Google Colab being overwhelmed

            continue
        elif event.event == "queryError":
            raise_query_error_event(event)
        else:
            raise_unexpected_event_found(event)

    if not result_received:
        raise_message_event_not_reached()
    return results


def receive_count(response: requests.models.Response, progress_bar: bool = False) -> int:
    """
    Helper function to parse clients events as counts and optionally show the progress bar.
    """
    client = sseclient.SSEClient(response)
    results = None
    result_received = False
    previous = 0

    for event in (pbar := tqdm(client.events(), disable=not progress_bar)):  # pylint: disable=no-member
        if event.event == "keepAlive":
            continue
        elif event.event == "finish":
            break
        elif event.event == "message":
            result_received = True
            results = json.loads(event.data)

            if progress_bar:
                if results != previous and results % 50 == 0:
                    previous = results
                    pbar.set_description(f"Collecting {previous} records")
                    sleep(0.1)  # to avoid Google Colab being overwhelmed
            continue
        elif event.event == "queryError":
            raise_query_error_event(event)
        else:
            raise_unexpected_event_found(event)

    if not result_received:
        raise_message_event_not_reached()
    return results
