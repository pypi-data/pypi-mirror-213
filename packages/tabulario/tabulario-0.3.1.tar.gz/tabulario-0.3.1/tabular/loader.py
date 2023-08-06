# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import os
import shutil
from typing import (
    Dict,
    Literal,
    Optional,
    Union,
)

from pyiceberg.catalog import Catalog, load_catalog
from pyiceberg.catalog.rest import Endpoints
from pyiceberg.table import Identifier, Table
from requests import HTTPError

from tab.exceptions import InvalidInputError


def enable_loading(
    identifier: Union[Identifier, str],
    file_type: Literal["csv", "json", "parquet"],
    mode: Literal["append", "replace"],
    delim: str = ",",
    catalog: Optional[Catalog] = None,
    override: bool = False,
):
    """
    Enable data loader for a given table. See https://docs.tabular.io/tables

    :param identifier: table identifier string or tuple
    :param file_type: csv, json, parquet
    :param mode: append or replace
    :param delim: delimiter for csv files
    :param catalog: optional catalog ('default' if not provided in table identifier)
    :param override: override the loader configuration if already enabled on the target table
    """
    catalog = _resolve_catalog(identifier, catalog)
    identifier = _normalize_table_identifier(identifier)

    table: Table = catalog.load_table(identifier)
    properties = table.metadata.properties

    if properties.get("fileloader.enabled") == "true" and not override:
        raise ValueError(f"Table '{identifier}' already has file loading enabled")

    payload: Dict[str, str] = {"format": file_type, "mode": mode}

    if file_type == "csv" and delim:
        payload["delim"] = delim

    url = catalog.url(
        f"{Endpoints.load_table}/loader",
        prefixed=True,
        **catalog._split_identifier_for_path(identifier),  # pylint: disable=[W0212]
    )
    # Remove the redirection for ice controller
    url = url.replace("/ice/", "/")

    response = catalog.session.post(url, json=payload)

    try:
        response.raise_for_status()
    except HTTPError as exc:
        catalog._handle_non_200_response(exc, {})  # pylint: disable=[W0212]


def ingest(identifier: Union[Identifier, str], file: str, catalog: Optional[Catalog] = None):
    """
    Ingest data into the provided Iceberg table by copying the provided file
    into the configured loader path in S3.

    :param identifier: target table for loading data
    :param file: path to the file to be loaded
    :param catalog: optional catalog ('default' if not provided in table identifier)
    """
    catalog = _resolve_catalog(identifier, catalog)
    identifier = _normalize_table_identifier(identifier)

    table: Table = catalog.load_table(identifier)
    properties = table.metadata.properties

    if properties.get("fileloader.enabled", "false") != "true":
        raise ValueError(f"File loader is not enabled for '{catalog.name}.{identifier}'")

    loader_path = properties.get("fileloader.path")
    loader_path += "/" + os.path.basename(file)
    io = table.io

    with io.new_input(file).open() as fin, io.new_output(loader_path).create(overwrite=True) as fout:
        shutil.copyfileobj(fin, fout)


def _resolve_catalog(identifier: Union[Identifier, str], catalog: Optional[Catalog] = None) -> Catalog:
    identifier_tuple: Identifier = Catalog.identifier_to_tuple(identifier)

    # Check if the catalog was provided in the identifier
    if len(identifier_tuple) == 3:
        if catalog:
            if catalog.name != identifier_tuple[0]:
                raise ValueError(f"Catalog identifier '{identifier_tuple[0]}' does not match catalog f'{catalog.name}'")
            return catalog
        else:
            return load_catalog(identifier_tuple[0])

    assert len(identifier_tuple) == 2, "Identifier must include database and table"
    return catalog or load_catalog("default")


def _normalize_table_identifier(identifier: Union[Identifier, str]) -> Identifier:
    identifier_tuple: Identifier = Catalog.identifier_to_tuple(identifier)

    if len(identifier_tuple) == 3:
        return identifier_tuple[1:]
    elif len(identifier_tuple) == 2:
        return identifier_tuple
    else:
        raise InvalidInputError(
            f"Table identifier '{identifier}' must be qualified as '<catalog>.<db>.<table>' or '<db>.<table>'"
        )
