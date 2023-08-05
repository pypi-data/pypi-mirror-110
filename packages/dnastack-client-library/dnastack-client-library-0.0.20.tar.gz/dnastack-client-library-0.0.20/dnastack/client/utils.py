import sys

import click
import requests
from requests.exceptions import SSLError, HTTPError
from search_python_client.search import SearchClient, DrsClient
from typing import Optional
import json
import io
import csv


def handle_client_results(results, dataconnect_url):
    try:
        yield from results
    except SSLError:
        click.secho(
            f"There was an error retrieving the SSL certificate from {dataconnect_url}",
            fg="red",
        )
        sys.exit(1)
    except HTTPError as e:
        error_res = requests.get(e.response.url)
        error_json = json.loads(error_res.text)
        error_msg = error_json["errors"][0]["title"]
        click.secho(
            f"There was an error querying from {dataconnect_url}: {error_msg}", fg="red"
        )
        sys.exit(1)


def get_dataconnect_client(dataconnect_url):
    return SearchClient(dataconnect_url)


def get_drs_client(drs_url):
    return DrsClient(drs_url)


def format_query_result_as_csv(query_results, include_headers=True):
    output = io.StringIO()
    writer = csv.writer(output)

    # if we have at least one result, add the headers
    if len(query_results) > 0 and include_headers:
        writer.writerow(query_results[0].keys())

    for res in query_results:
        data_row = list(map(lambda x: str(x).replace(",", "\,"), res.values()))
        writer.writerow(data_row)

    return output.getvalue()
