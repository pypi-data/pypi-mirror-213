# Copyright 2023 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import zipfile
from tempfile import TemporaryDirectory
from urllib.parse import unquote

from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.helper import generate_identifier
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.records import Record


def import_eln(manager, file_path):
    """Import an RO-Crate file following the "ELN" file specification.

    :param file_path: The path of the file.
    :type file_path: str
    :raises KadiAPYInputError: If the structure of the RO-Crate is not valid.
    :raises KadiAPYRequestError: If any request was not successful while importing the
        data and metadata.
    """
    with zipfile.ZipFile(file_path) as ro_crate, TemporaryDirectory() as tmpdir:
        namelist = ro_crate.namelist()

        if not namelist:
            raise KadiAPYInputError("Archive is empty.")

        # We assume the first path contains the root directory of the crate.
        root_dir = namelist[0].split("/")[0]
        metadata_file_name = "ro-crate-metadata.json"

        if f"{root_dir}/{metadata_file_name}" not in namelist:
            raise KadiAPYInputError("Missing metadata file in RO-Crate.")

        ro_crate.extractall(tmpdir)

        root_path = os.path.join(tmpdir, root_dir)
        metadata_file_path = os.path.join(root_path, metadata_file_name)

        try:
            with open(metadata_file_path, mode="rb") as metadata_file:
                metadata = json.load(metadata_file)
        except Exception as e:
            raise KadiAPYInputError("Error opening or parsing metadata file.") from e

        # Collect all entities in the JSON-LD graph.
        graph = metadata.get("@graph", [])

        if not isinstance(graph, list):
            _raise_invalid_content("Graph is not an array.")

        entities = {}

        for entity in graph:
            if isinstance(entity, dict) and "@id" in entity:
                entities[entity["@id"]] = entity

        root_entity = entities.get("./")

        if root_entity is None:
            _raise_invalid_content("Root dataset missing in graph.")

        root_parts = root_entity.get("hasPart", [])

        if not isinstance(root_parts, list):
            _raise_invalid_content("Root parts are not an array.")

        collection_id = None

        # Create a collection if we have multiple entries in the root dataset.
        if len(root_parts) > 1:
            response = _create_resource(
                manager, Collection.base_path, {"title": root_dir}
            )
            collection_id = response.json()["id"]

        # Import all datasets as records.
        for root_part in root_parts:
            if not isinstance(root_part, dict) or "@id" not in root_part:
                _raise_invalid_content("Root part is not an object or missing an @id.")

            dataset_entity = entities.get(root_part["@id"])

            if dataset_entity is None:
                _raise_invalid_content(f"Entity {root_part['@id']} missing in graph.")

            if dataset_entity.get("@type") != "Dataset":
                continue

            record_metadata = {
                "title": dataset_entity.get("name", dataset_entity["@id"]),
                "tags": dataset_entity.get("keywords", []),
                "description": dataset_entity.get("text", ""),
            }

            response = _create_resource(manager, Record.base_path, record_metadata)
            record = manager.record(id=response.json()["id"])

            # Add the record to the collection, if applicable.
            if collection_id is not None:
                record.add_collection_link(collection_id)

            dataset_parts = dataset_entity.get("hasPart", [])

            if not isinstance(dataset_parts, list):
                _raise_invalid_content("Dataset parts are not an array.")

            # Import all files of the dataset.
            for dataset_part in dataset_parts:
                if not isinstance(dataset_part, dict) or "@id" not in dataset_part:
                    _raise_invalid_content(
                        "Dataset part is not an object or missing an @id."
                    )

                file_entity = entities.get(dataset_part["@id"])

                if file_entity is None:
                    _raise_invalid_content(
                        f"Entity {dataset_part['@id']} missing in graph."
                    )

                if file_entity.get("@type") != "File":
                    continue

                file_id = unquote(file_entity["@id"]).split("/", 1)[-1]
                file_path = os.path.realpath(os.path.join(root_path, file_id))

                # Ensure that the file path is contained within the root path in the
                # temporary directory.
                if os.path.commonpath([root_path, file_path]) != root_path:
                    _raise_invalid_content(f"Referenced file {file_path} is invalid.")

                file_name = file_entity.get("name", os.path.basename(file_path))
                file_description = file_entity.get("text", "")

                record.upload_file(file_path, file_name, file_description)


def _raise_invalid_content(msg):
    raise KadiAPYInputError(f"Invalid content in metadata file: {msg}")


def _create_resource(manager, base_path, metadata):
    base_identifier = generate_identifier(metadata["title"])
    metadata["identifier"] = base_identifier

    index = 1

    while True:
        response = manager._post(base_path, json=metadata)

        if response.status_code == 201:
            return response

        errors = response.json().get("errors", {})

        # Check if only the identifier was the problem and attempt to fix it.
        if "identifier" in errors and len(errors) == 1:
            suffix = f"-{str(index)}"
            metadata["identifier"] = f"{base_identifier[:50-len(suffix)]}{suffix}"

            index += 1
        else:
            raise KadiAPYRequestError(response.json())

        # Just in case, to make sure we never end up in an endless loop.
        if index > 100:
            break

    raise KadiAPYRequestError("Error attempting to create resource.")
