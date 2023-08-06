import array
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Iterable, Iterator, Mapping, Optional, Set

import numpy as np
import scipy
from penelope.co_occurrence.interface import ContextOpts
from penelope.corpus import Token2Id
from penelope.type_alias import Token


class VectorizeType(IntEnum):
    Normal = 1
    Concept = 2


@dataclass
class VectorizedTTM:
    vectorize_type: VectorizeType
    term_term_matrix: scipy.sparse.spmatrix
    term_window_counts: Mapping[int, int]
    document_id: int


class DocumentWindowsVectorizer:
    """Creates a term-term-matrix from a sequence of windows (tokens)"""

    def __init__(self, vocabulary: Token2Id, dtype: Any = np.int32):

        self.total_term_window_counts: Mapping[VectorizeType, Counter] = defaultdict(Counter)
        self.vocabulary: Token2Id = vocabulary
        self.dtype = dtype

    def fit_transform(
        self, *, document_id: int, windows: Iterator[Iterator[str]], context_opts: ContextOpts
    ) -> Mapping[VectorizeType, VectorizedTTM]:
        """Fits windows generated from a __single__ document"""

        ignore_ids: Set[int] = set()

        if context_opts.ignore_padding:
            ignore_ids.add(self.vocabulary[context_opts.pad])

        if context_opts.concept:
            if context_opts.ignore_concept:
                ignore_ids.update(context_opts.get_concepts())

        data: Mapping[VectorizeType, VectorizedTTM] = self.vectorize(
            document_id=document_id,
            windows=windows,
            concept=context_opts.concept,
            ignore_ids=ignore_ids,
        )

        for item in data.values():
            self.total_term_window_counts[item.vectorize_type].update(item.term_window_counts)

        return data

    def vectorize(
        self,
        *,
        document_id: int,
        windows: Iterator[Iterable[Token]],
        concept: Set[str],
        ignore_ids: Set[int],
    ) -> Mapping[VectorizeType, VectorizedTTM]:

        if len(concept) > 1:
            raise NotImplementedError("Multiple concepts disabled (performance")

        concept_word: Optional[str] = list(concept)[0] if concept else None

        counters: Mapping[VectorizeType, WindowsTermsCounter] = defaultdict(WindowsTermsCounter)

        fg = self.vocabulary.get
        ewu = counters[VectorizeType.Normal].update

        def _count_tokens_without_ignores(windows: Iterable[str]) -> dict:
            token_counter: dict = {}
            tg = token_counter.get
            for t in windows:
                token_counter[t] = tg(t, 0) + 1
            return token_counter

        def _count_tokens_with_ignores(windows: Iterable[str]) -> dict:
            token_counter: dict = {}
            tg = token_counter.get
            for t in windows:
                if t in ignore_ids:
                    continue
                token_counter[t] = tg(t, 0) + 1
            return token_counter

        count_tokens = _count_tokens_with_ignores if ignore_ids else _count_tokens_without_ignores

        if concept_word:
            cwu = counters[VectorizeType.Concept].update
            for window in windows:
                token_counts: dict = count_tokens(fg(t) for t in window)
                if concept_word in window:  # any(x in window for x in concept):
                    cwu(token_counts)
                ewu(token_counts)
        else:
            for window in windows:
                ewu(count_tokens(fg(t) for t in window))

        data: Mapping[VectorizeType, VectorizedTTM] = {
            key: counter.compile(vectorize_type=key, document_id=document_id, vocab_size=len(self.vocabulary))
            for key, counter in counters.items()
        }

        return data


class WindowsTermsCounter:
    def __init__(self, dtype: Any = np.int32):
        self.dtype = dtype
        self.indptr = []
        self.jj = []
        self.values = array.array(str("i"))
        self.indptr.append(0)
        self._jj_extend = self.jj.extend
        self._values_extend = self.values.extend
        self._indptr_append = self.indptr.append

    def update(self, token_counter: Counter):
        if None in token_counter.keys():
            raise ValueError("BugCheck: None in TokenCounter not allowed!")
        self._jj_extend(token_counter.keys())
        self._values_extend(token_counter.values())
        self._indptr_append(len(self.jj))

    def compile(self, *, document_id: int, vectorize_type: VectorizeType, vocab_size: int) -> VectorizedTTM:
        self.jj = np.asarray(self.jj, dtype=np.int64)
        self.indptr = np.asarray(self.indptr, dtype=np.int32)
        self.values = np.frombuffer(self.values, dtype=np.intc)

        window_term_matrix: scipy.sparse.spmatrix = scipy.sparse.csr_matrix(
            (self.values, self.jj, self.indptr), shape=(len(self.indptr) - 1, vocab_size), dtype=self.dtype
        )
        window_term_matrix.sort_indices()

        term_term_matrix: scipy.sparse.spmatrix = scipy.sparse.triu(
            np.dot(window_term_matrix.T, window_term_matrix),
            1,
        )
        term_window_counts: Mapping[int, int] = self.to_term_window_counter(window_term_matrix)
        return VectorizedTTM(
            vectorize_type=vectorize_type,
            document_id=document_id,
            term_term_matrix=term_term_matrix,
            term_window_counts=term_window_counts,
        )

    def to_term_window_counter(self, window_term_matrix: scipy.sparse.spmatrix) -> Mapping[int, int]:
        """Returns tuples (token_id, window count) for non-zero tokens in window_term_matrix"""

        window_counts: np.ndarray = (window_term_matrix != 0).sum(axis=0).A1
        window_counter: Mapping[int, int] = {i: window_counts[i] for i in window_counts.nonzero()[0]}
        return window_counter
