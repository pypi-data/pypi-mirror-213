#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import re
import time
from collections import defaultdict
from typing import TYPE_CHECKING
from copy import deepcopy

if TYPE_CHECKING:
    from typing import (
        Any,
        Callable,
        DefaultDict,
        Generator,
        Iterable,
        List,
        Sequence,
        Union,
    )

    import dedupe.predicates
    from mobio.sdks.dedupe._typing import Data, Record, RecordID
    from mobio.sdks.dedupe.index import Index

    Docs = Union[Iterable[str], Iterable[Iterable[str]]]
    IndexList = DefaultDict[str, List[dedupe.predicates.IndexPredicate]]


logger = logging.getLogger(__name__)


def index_list() -> IndexList:
    return defaultdict(list)


class Fingerprinter(object):
    """Takes in a record and returns all blocks that record belongs to"""

    def __init__(self, predicates: Iterable[dedupe.predicates.Predicate]) -> None:
        self.predicates = predicates

        self.index_fields: dict[str, IndexList]
        self.index_fields = defaultdict(index_list)
        """
        A dictionary of all the fingerprinter methods that use an
        index of data field values. The keys are the field names,
        which can be useful to know for indexing the data.
        """

        self.index_predicates = []

        for full_predicate in predicates:
            for predicate in full_predicate:
                if hasattr(predicate, "index"):
                    self.index_fields[predicate.field][predicate.type].append(predicate)
                    self.index_predicates.append(predicate)

    def __call__(
        self, records: Iterable[Record], target: bool = False
    ) -> Generator[tuple[str, RecordID], None, None]:
        """
        Generate the predicates for records. Yields tuples of (predicate,
        record_id).

        Args:
            records: A sequence of tuples of (record_id,
                  record_dict). Can often be created by
                  `data_dict.items()`.
            target: Indicates whether the data should be treated as
                    the target data. This effects the behavior of
                    search predicates. If `target` is set to
                    `True`, an search predicate will return the
                    value itself. If `target` is set to `False` the
                    search predicate will return all possible
                    values within the specified search distance.

                    Let's say we have a
                    `LevenshteinSearchPredicate` with an associated
                    distance of `1` on a `"name"` field; and we
                    have a record like `{"name": "thomas"}`. If the
                    `target` is set to `True` then the predicate
                    will return `"thomas"`.  If `target` is set to
                    `False`, then the blocker could return
                    `"thomas"`, `"tomas"`, and `"thoms"`. By using
                    the `target` argument on one of your datasets,
                    you will dramatically reduce the total number
                    of comparisons without a loss of accuracy.

        .. code:: python

           > data = [(1, {'name' : 'bob'}), (2, {'name' : 'suzanne'})]
           > blocked_ids = deduper.fingerprinter(data)
           > print list(blocked_ids)
           [('foo:1', 1), ..., ('bar:1', 100)]

        """

        start_time = time.perf_counter()
        predicates = [
            (":" + predicate.__name__.split(", ")[-1].replace(")", ""), predicate) for i, predicate in
            enumerate(self.predicates)
        ]
        """And"""
        len_predicates = len(predicates)
        for i, record in enumerate(records):
            record_id, instance = record
            statics_key = []
            check_predicates = set([])
            block_key = ""
            for pred_id, predicate in predicates:
                if instance.get(predicate.field):
                    doc_norm = self.standardized_exclusion(predicate=predicate, doc=instance.get(predicate.field))
                    instance[predicate.field] = doc_norm
                    block_keys = predicate(instance, target=target)
                    for _block_key in block_keys:
                        if len_predicates > 1 and not predicate.is_approximate:
                            block_key += pred_id + ":" + _block_key + ":"
                            check_predicates.add(predicate.__name__)
                            continue
                        if len_predicates > 1 and predicate.is_approximate:
                            pre_fix_block_key = deepcopy(block_key)
                            pre_fix_block_key += pred_id + ":" + _block_key + ":"
                            statics_key.append(pre_fix_block_key)
                            check_predicates.add(predicate.__name__)
                            continue
                        elif len_predicates == 1:
                            yield pred_id + ":" + _block_key, record_id

            if statics_key and len(check_predicates) == len_predicates:
                for bk in statics_key:
                    yield bk, record_id
            elif not statics_key and len(check_predicates) == len_predicates:
                yield block_key, record_id

            if i and i % 10000 == 0:
                logger.info(
                    "%(iteration)d, %(elapsed)f2 seconds",
                    {"iteration": i, "elapsed": time.perf_counter() - start_time},
                )

        """Array"""
        # for i, record in enumerate(records):
        #     record_id, instance = record
        #     if int(instance["donor_id"]) == 5697:
        #         a = 1
        #     if int(instance["donor_id"]) == 1209:
        #         a = 1
        #     statics_key = []
        #     block_key = ""
        #     first = True
        #     for pred_id, predicate in predicates:
        #         if "address" in pred_id:
        #             for data in instance["address"]:
        #                 _instance = {"address": data}
        #                 block_keys = predicate(_instance, target=target)
        #                 for _block_key in block_keys:
        #                     if first:
        #                         block_key_id = _block_key + pred_id + ":"
        #                         statics_key.append(block_key_id)
        #                         first = False
        #                     else:
        #                         block_key_id = _block_key + pred_id + ":"
        #                         statics_key.append(block_key_id)
        #         else:
        #             block_keys = predicate(instance, target=target)
        #             for _block_key in block_keys:
        #                 if first:
        #                     block_key += _block_key + pred_id + ":"
        #                     statics_key.append(block_key)
        #                     first = False
        #                     continue
        #                 else:
        #                     from copy import deepcopy
        #                     clone_key = deepcopy(statics_key)
        #                     for static_key in clone_key:
        #                         static_key += _block_key + pred_id + ":"
        #                         statics_key.append(static_key)
        #                         yield static_key, record_id
        #
        #
        #     if i and i % 10000 == 0:
        #         logger.info(
        #             "%(iteration)d, %(elapsed)f2 seconds",
        #             {"iteration": i, "elapsed": time.perf_counter() - start_time},
        #         )

        # """Original"""
        # for i, record in enumerate(records):
        #     record_id, instance = record
        #
        #     for pred_id, predicate in predicates:
        #         block_keys = predicate(instance, target=target)
        #         for block_key in block_keys:
        #             yield block_key + pred_id, record_id
        #
        #     if i and i % 10000 == 0:
        #         logger.info(
        #             "%(iteration)d, %(elapsed)f2 seconds",
        #             {"iteration": i, "elapsed": time.perf_counter() - start_time},
        #         )

    @staticmethod
    def standardized_exclusion(predicate, doc):
        if predicate.exc_order_bword:
            doc = doc
        if predicate.exc_space:
            doc = doc
        if predicate.exc_spec_char:
            for char in ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", ",", "-", "+", "/"]:
                doc = doc.replace(char, "")
        if predicate.exc_without_accent:
            doc = re.sub("à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ", "a", doc)
            doc = re.sub("è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ", "e", doc)
            doc = re.sub("ì|í|ị|ỉ|ĩ", "i", doc)
            doc = re.sub("ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ", "o", doc)
            doc = re.sub("ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ", "u", doc)
            doc = re.sub("ỳ|ý|ỵ|ỷ|ỹ", "y", doc)
            doc = re.sub("đ", "d", doc)
            doc = re.sub("Đ", "D", doc)

            doc = re.sub("À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ", "A", doc)
            doc = re.sub("È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ", "E", doc)
            doc = re.sub("Ì|Í|Ị|Ỉ|Ĩ", "I", doc)
            doc = re.sub("Ò|Ó|Ọ|Ỏ|Õ|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ", "O", doc)
            doc = re.sub("Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ", "U", doc)
            doc = re.sub("Ỳ|Ý|Ỵ|Ỷ|Ỹ", "Y", doc)
        return doc

    def reset_indices(self) -> None:
        """
        Fingeprinter indicdes can take up a lot of memory. If you are
        done with blocking, the method will reset the indices to free up.
        If you need to block again, the data will need to be re-indexed.
        """
        for predicate in self.index_predicates:
            predicate.reset()

    def index(self, docs: Docs, field: str) -> None:
        """
        Add docs to the indices used by fingerprinters.

        Some fingerprinter methods depend upon having an index of
        values that a field may have in the data. This method adds
        those values to the index. If you don't have any fingerprinter
        methods that use an index, this method will do nothing.

        Args:
            docs: an iterator of values from your data to index. While
                  not required, it is recommended that docs be a unique
                  set of of those values. Indexing can be an expensive
                  operation.
            field: fieldname or key associated with the values you are
                   indexing

        """
        indices = extractIndices(self.index_fields[field])

        for doc in docs:
            if doc:
                for _, index, preprocess, predicate in indices:
                    doc = self.standardized_exclusion(predicate=predicate, doc=doc)
                    index.index(preprocess(doc))

        for index_type, index, _, _ in indices:
            index.initSearch()

            for predicate in self.index_fields[field][index_type]:
                logger.debug("Canopy: %s", str(predicate))
                predicate.index = index
                predicate.bust_cache()

    def unindex(self, docs: Docs, field: str) -> None:
        """Remove docs from indices used by fingerprinters

        Args:
            docs: an iterator of values from your data to remove. While
                  not required, it is recommended that docs be a unique
                  set of of those values. Indexing can be an expensive
                  operation.
            field: fieldname or key associated with the values you are
                   unindexing
        """

        indices = extractIndices(self.index_fields[field])

        for doc in docs:
            if doc:
                for _, index, preprocess, predicate in indices:
                    try:
                        index.unindex(preprocess(doc))
                    except KeyError:
                        pass

        for index_type, index, _, _ in indices:
            index.initSearch()

            for predicate in self.index_fields[field][index_type]:
                logger.debug("Canopy: %s", str(predicate))
                predicate.index = index
                predicate.bust_cache()

    def index_all(self, data: Data) -> None:
        for field in self.index_fields:
            unique_fields = {record[field] for record in data.values() if record[field]}
            self.index(unique_fields, field)


def extractIndices(
    index_fields: IndexList,
) -> Sequence[tuple[str, Index, Callable[[Any], Any]]]:
    indices = []
    for index_type, predicates in index_fields.items():
        predicate = predicates[0]
        index = predicate.index
        preprocess = predicate.preprocess
        if predicate.index is None:
            index = predicate.initIndex()
        assert index is not None
        indices.append((index_type, index, preprocess, predicate))

    return indices
