import json
import os
import tarfile
import tempfile
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from itertools import groupby, islice
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Tuple, Union

from sqlalchemy import Float, Integer, String
from tqdm import tqdm

from dql.node import DirType

if TYPE_CHECKING:
    from dql.listing import Listing


PROCESSING_BATCH_SIZE = 1000  # Batch size for inserting entries.

INSERT_ITEMS = "insert"  # Indexing format adds new objects.
UPDATE_ITEMS = "update"  # Indexing format extends objects with new properties.


class IndexingFormat(ABC):
    """
    Indexing formats allow additional transformations on indexed
    objects, such as listing contents of archives.
    """

    # Default processor action - add new items to the index or update them,
    # e.g. by adding new signals.
    action_type: str = INSERT_ITEMS

    @abstractmethod
    def filter(self, listing: "Listing", paths: List[str]) -> Iterator[Tuple[Any, ...]]:
        """Create a list of entries to process"""

    @abstractmethod
    def process(self, listing, entries):
        """Process an entry and return additional entries to store."""


class TarFiles(IndexingFormat):
    """
    TarFiles indexes buckets containing uncompressed tar archives. The contents of
    the archives is indexed as well.
    """

    item_type = INSERT_ITEMS

    def filter(self, listing: "Listing", paths: List[str]) -> Iterator[Tuple[Any, ...]]:
        for path in paths:
            for node in listing.expand_path(path):
                found = listing.find(
                    node,
                    ["path_str", "id", "is_latest", "partial_id"],
                    names=["*.tar"],
                )
                yield from found

    def process(self, listing: "Listing", entries):
        for entry in entries:
            yield from self.process_entry(listing, entry)

    def process_entry(self, listing: "Listing", entry):
        pth, parent_id, is_latest, partial_id = entry
        local_path = tempfile.gettempdir() + f"/dql_cache_{parent_id}"
        client = listing.client
        # Download tarball to local storage first.
        client.fs.get_file(client.get_full_path(pth), local_path)
        with tarfile.open(name=local_path, mode="r:") as tar:
            for info in tar:
                if info.isdir():
                    yield self.tardir_from_info(
                        info, parent_id, pth, is_latest, partial_id
                    )
                elif info.isfile():
                    yield self.tarmember_from_info(
                        info, parent_id, pth, is_latest, partial_id
                    )
        os.remove(local_path)
        listing.data_storage.update_type(parent_id, DirType.TAR_ARCHIVE)

    def tarmember_from_info(self, info, parent_id, path_str, is_latest, partial_id):
        location = json.dumps(
            [
                {
                    "offset": info.offset_data,
                    "size": info.size,
                    "type": "tar",
                    "parent": path_str,
                },
            ]
        )
        return {
            "vtype": "tar",
            "dir_type": DirType.FILE,
            "parent_id": parent_id,
            "path_str": f"{path_str}/{info.name}",
            "name": info.name.rsplit("/", 1)[-1],
            "checksum": "",
            "etag": "",
            "version": "",
            "is_latest": is_latest,
            "last_modified": datetime.fromtimestamp(info.mtime, timezone.utc),
            "size": info.size,
            "owner_name": info.uname,
            "owner_id": str(info.uid),
            "location": location,
            "partial_id": partial_id,
        }

    def tardir_from_info(self, info, parent_id, path_str, is_latest, partial_id):
        return {
            "vtype": "tar",
            "dir_type": DirType.DIR,
            "parent_id": parent_id,
            "path_str": f"{path_str}/{info.name.rstrip('/')}",
            "name": info.name.rsplit("/", 1)[-1],
            "checksum": "",
            "etag": "",
            "version": "",
            "is_latest": is_latest,
            "last_modified": datetime.fromtimestamp(info.mtime, timezone.utc),
            "size": info.size,
            "owner_name": info.uname,
            "owner_id": str(info.uid),
            "partial_id": partial_id,
        }


class LaionJSONPair(IndexingFormat):
    """
    Load signals from .json files and attach them to objects with the same base name.
    """

    action_type = UPDATE_ITEMS

    IGNORED_EXTS = [".json", ".txt"]  # File extensions not to attach loaded signals to.

    def filter(self, listing: "Listing", paths: List[str]) -> Iterator[Tuple[Any, ...]]:
        for path in paths:
            for node in listing.expand_path(path):
                found = listing.find(
                    node,
                    ["path_str", "id", "vtype", "name", "size", "location"],
                    order_by="path_str",
                )
                yield from found

    def process(self, listing: "Listing", entries):
        self._create_columns(listing)
        for _, group in groupby(entries, self._group):
            yield from self._process_group(listing, group)

    def _process_group(self, listing: "Listing", group):
        # Create a map of extension to object info.
        nodes = {
            os.path.splitext(entry[0])[1]: {
                "path_str": entry[0],
                "id": entry[1],
                "vtype": entry[2],
                "name": entry[3],
                "size": entry[4],
                "location": entry[5],
            }
            for entry in group
        }
        json_obj = nodes.get(".json")
        if not json_obj:
            # No .json file in group. Ignore.
            return
        with listing.client.open_object(
            json_obj["path_str"],
            json_obj["vtype"],
            **{arg: json_obj[arg] for arg in ("name", "size", "location")},
        ) as f:
            data = json.load(f)
            if not isinstance(data, dict):
                # .json file contains something other than a json object. Ignore.
                return
            update = {
                col[0]: data.get(col[0]) for col in laionJSONColumns if data.get(col[0])
            }

        for ext, node in nodes.items():
            if ext in self.IGNORED_EXTS:
                continue
            yield (node["id"], update)

    def _group(self, entry):
        """
        Group entries by paths sans the extension.
        This way 'path/000.jpg' and 'path/000.json' will be grouped
        together.
        """
        return os.path.splitext(entry[0])[0]

    def _create_columns(self, listing: "Listing"):
        for col_name, col_type in laionJSONColumns:
            listing.data_storage.add_bucket_signal_column(
                listing.client.uri, col_name, col_type
            )


# Signal columns for storing laion json data.
laionJSONColumns = (
    ("punsafe", Float()),
    ("pwatermark", Float()),
    ("similarity", Float()),
    ("hash", Integer()),
    ("caption", String()),
    ("url", String()),
    ("key", String()),
    ("status", String()),
    ("error_message", String()),
    ("width", Integer()),
    ("height", Integer()),
    ("original_width", Integer()),
    ("original_height", Integer()),
    ("md5", String()),
)


async def apply_processors(
    listing: "Listing", path: str, processors: List[IndexingFormat]
):
    async def insert_items(items):
        await listing.data_storage.insert_entries(items)

    async def update_items(items):
        for item in items:
            (node_id, values) = item
            listing.data_storage.update_node(node_id, values)

    for processor in processors:
        if processor.action_type == INSERT_ITEMS:
            func = insert_items
        elif processor.action_type == UPDATE_ITEMS:
            func = update_items

        listing = listing.clone()
        with tqdm(desc="Processing", unit=" objects") as pbar:
            entries = processor.filter(listing, [path])
            results = processor.process(listing, entries)
            for batch in _batch(results, PROCESSING_BATCH_SIZE):
                pbar.update(len(batch))
                await func(batch)
        if processor.action_type == INSERT_ITEMS:
            listing.data_storage.inserts_done()


def _batch(it, size):
    while batch := list(islice(it, size)):
        yield batch


indexer_formats: Dict[str, Union[List[IndexingFormat], IndexingFormat]] = {
    "tar-files": TarFiles(),
    "json-pair": LaionJSONPair(),
    "webdataset": [TarFiles(), LaionJSONPair()],
}
