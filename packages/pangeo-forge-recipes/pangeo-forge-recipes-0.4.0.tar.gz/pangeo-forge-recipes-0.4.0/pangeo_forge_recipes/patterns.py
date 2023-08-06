"""
Filename / URL patterns.
"""

from dataclasses import dataclass, field, replace
from itertools import product
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Tuple, Union

import numpy as np
import xarray as xr


@dataclass
class ConcatDim:
    """Represents a concatenation operation across a dimension of a FilePattern.

    :param name: The name of the dimension we are concatenating over. For
      files with labeled dimensions, this should match the dimension name
      within the file. The most common value is ``"time"``.
    :param keys: The keys used to represent each individual item along this
      dimension. This will be used by a ``FilePattern`` object to evaluate
      the file name.
    :param nitems_per_file: If each file contains the exact same known number of
      items in each file along the concat dimension, this can be set to
      provide a fast path for recipes.
    """

    name: str  # should match the actual dimension name
    keys: Sequence[Any] = field(repr=False)
    nitems_per_file: Optional[int] = None


@dataclass
class MergeDim:
    """Represents a merge operation across a dimension of a FilePattern.

    :param name: The name of the dimension we are are merging over. The actual
       value is not used by most recipes. The most common value is
       ``"variable"``.
    :param keys: The keys used to represent each individual item along this
      dimension. This will be used by a ``FilePattern`` object to evaluate
      the file name.
    """

    name: str
    keys: Sequence[Any] = field(repr=False)


Index = Tuple[int, ...]
CombineDim = Union[MergeDim, ConcatDim]


class FilePattern:
    """Represents an n-dimensional matrix of individual files to be combined
    through a combination of merge and concat operations. Each operation generates
    a new dimension to the matrix.

    :param format_function: A function that takes one argument for each
      combine_op and returns a string representing the filename / url paths.
      Each argument name should correspond to a ``name`` in the ``combine_dims``
      list.
    :param combine_dims: A sequence of either concat or merge dimensions. The outer
      product of the keys is used to generate the full list of file paths.
    """

    @staticmethod
    def _make_da(format_function, combine_dims) -> xr.DataArray:
        dim_names = [cdim.name for cdim in combine_dims]
        fnames = []
        for keys in product(*[cdim.keys for cdim in combine_dims]):
            kwargs = dict(zip(dim_names, keys))
            fnames.append(format_function(**kwargs))
        shape = [len(cdim.keys) for cdim in combine_dims]
        fnames_np = np.array(fnames)
        fnames_np.shape = tuple(shape)
        # This way of defining coords is incompatible with xarray type annotations.
        # I don't understand why.
        coords = {cdim.name: (cdim.name, cdim.keys) for cdim in combine_dims}
        return xr.DataArray(fnames_np, dims=list(coords), coords=coords)  # type: ignore

    def __init__(self, format_function: Callable, *combine_dims: CombineDim):
        self.__setstate__((format_function, combine_dims))

    def __getstate__(self):
        return self.format_function, self.combine_dims

    def __setstate__(self, state):
        self.format_function, self.combine_dims = state
        self._da = self._make_da(self.format_function, self.combine_dims)

    def __repr__(self):
        return f"<FilePattern {self.dims}>"

    @property
    def dims(self) -> Dict[str, int]:
        """Dictionary representing the dimensions of the FilePattern. Keys are
        dimension names, values are the number of items along each dimension."""
        return {op.name: len(op.keys) for op in self.combine_dims}

    @property
    def shape(self) -> Tuple[int, ...]:
        """Shape of the filename matrix."""
        return self._da.shape

    @property
    def merge_dims(self) -> List[str]:
        """List of dims that are merge operations"""
        return [op.name for op in self.combine_dims if isinstance(op, MergeDim)]

    @property
    def concat_dims(self) -> List[str]:
        """List of dims that are concat operations"""
        return [op.name for op in self.combine_dims if isinstance(op, ConcatDim)]

    @property
    def nitems_per_input(self) -> Dict[str, Union[int, None]]:
        """Dictionary mapping concat dims to number of items per file."""
        nitems = {}  # type: Dict[str, Union[int, None]]
        for op in self.combine_dims:
            if isinstance(op, ConcatDim):
                if op.nitems_per_file:
                    nitems[op.name] = op.nitems_per_file
                else:
                    nitems[op.name] = None
        return nitems

    @property
    def concat_sequence_lens(self) -> Dict[str, Optional[int]]:
        """Dictionary mapping concat dims to sequence lengths.
        Only available if ``nitems_per_input`` is set on the dimension."""
        return {
            dim_name: (nitems * self.dims[dim_name] if nitems is not None else None)
            for dim_name, nitems in self.nitems_per_input.items()
        }

    def __getitem__(self, indexer) -> str:
        """Get a filename path for a particular key. """
        return self._da[indexer].values.item()

    def __iter__(self) -> Iterator[Index]:
        """Iterate over all keys in the pattern. """
        for val in product(*[range(n) for n in self.shape]):
            yield val

    def items(self):
        """Iterate over key, filename pairs."""
        for key in self:
            yield key, self[key]


def pattern_from_file_sequence(file_list, concat_dim, nitems_per_file=None):
    """Convenience function for creating a FilePattern from a list of files."""

    keys = list(range(len(file_list)))
    concat = ConcatDim(name=concat_dim, keys=keys, nitems_per_file=nitems_per_file)

    def format_function(**kwargs):
        return file_list[kwargs[concat_dim]]

    return FilePattern(format_function, concat)


def prune_pattern(fp: FilePattern, nkeep: int = 2) -> FilePattern:
    """
    Create a smaller pattern from a full pattern.
    Keeps all MergeDims but only the first `nkeep` items from each ConcatDim

    :param fp: The original pattern.
    :param nkeep: The number of items to keep from each ConcatDim sequence.
    """

    new_combine_dims = []  # type: List[CombineDim]
    for cdim in fp.combine_dims:
        if isinstance(cdim, MergeDim):
            new_combine_dims.append(cdim)
        elif isinstance(cdim, ConcatDim):
            new_keys = cdim.keys[:nkeep]
            new_cdim = replace(cdim, keys=new_keys)
            new_combine_dims.append(new_cdim)
        else:  # pragma: no cover
            assert "Should never happen"

    return FilePattern(fp.format_function, *new_combine_dims)
