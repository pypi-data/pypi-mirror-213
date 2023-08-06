# This file is part of daf_butler.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

"""Support for reading and writing files to a POSIX file system."""

__all__ = ("FileFormatter",)

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Optional, Type

from lsst.daf.butler import Formatter
from lsst.utils.introspection import get_full_type_name

if TYPE_CHECKING:
    from lsst.daf.butler import StorageClass


class FileFormatter(Formatter):
    """Interface for reading and writing files on a POSIX file system."""

    extension: Optional[str] = None
    """Default file extension to use for writing files. None means that no
    modifications will be made to the supplied file extension. (`str`)"""

    @abstractmethod
    def _readFile(self, path: str, pytype: Optional[Type[Any]] = None) -> Any:
        """Read a file from the path in the correct format.

        Parameters
        ----------
        path : `str`
            Path to use to open the file.
        pytype : `class`, optional
            Class to use to read the file.

        Returns
        -------
        data : `object`
            Data read from file. Returns `None` if the file can not be
            found at the given path.

        Raises
        ------
        Exception
            Some problem reading the file.
        """
        pass

    @abstractmethod
    def _writeFile(self, inMemoryDataset: Any) -> None:
        """Write the in memory dataset to file on disk.

        Parameters
        ----------
        inMemoryDataset : `object`
            Object to serialize.

        Raises
        ------
        Exception
            The file could not be written.
        """
        pass

    def _assembleDataset(self, data: Any, component: Optional[str] = None) -> Any:
        """Assembles and coerces the dataset, or one of its components,
        into an appropriate python type and returns it.

        Parameters
        ----------
        data : `dict` or `object`
            Composite or a dict that, or which component, needs to be
            coerced to the python type specified in "fileDescriptor"
        component : `str`, optional
            Component to read from the file. Only used if the `StorageClass`
            for reading differed from the `StorageClass` used to write the
            file.

        Returns
        -------
        inMemoryDataset : `object`
            The requested data as a Python object. The type of object
            is controlled by the specific formatter.
        """
        fileDescriptor = self.fileDescriptor

        # if read and write storage classes differ, more work is required
        readStorageClass = fileDescriptor.readStorageClass
        if readStorageClass != fileDescriptor.storageClass:
            if component is None:
                # This likely means that type conversion is required but
                # it will be an error if no valid converter is available
                # for this pytype.
                if not readStorageClass.can_convert(fileDescriptor.storageClass):
                    raise ValueError(
                        f"Storage class inconsistency ({readStorageClass.name} vs"
                        f" {fileDescriptor.storageClass.name}) but no"
                        " component requested or converter registered for"
                        f" converting type {get_full_type_name(fileDescriptor.storageClass.pytype)}"
                        f" to {get_full_type_name(readStorageClass.pytype)}."
                    )
            else:
                # Concrete composite written as a single file (we hope)
                try:
                    data = fileDescriptor.storageClass.delegate().getComponent(data, component)
                except AttributeError:
                    # Defer the complaint
                    data = None

        # Coerce to the requested type (not necessarily the type that was
        # written)
        data = self._coerceType(data, fileDescriptor.storageClass, readStorageClass)

        return data

    def _coerceType(
        self, inMemoryDataset: Any, writeStorageClass: StorageClass, readStorageClass: StorageClass
    ) -> Any:
        """Coerce the supplied inMemoryDataset to the correct python type.

        Parameters
        ----------
        inMemoryDataset : `object`
            Object to coerce to expected type.
        writeStorageClass : `StorageClass`
            Storage class used to serialize this data.
        readStorageClass : `StorageClass`
            Storage class requested as the outcome.

        Returns
        -------
        inMemoryDataset : `object`
            Object of expected type ``readStorageClass.pytype``.
        """
        return readStorageClass.coerce_type(inMemoryDataset)

    def read(self, component: Optional[str] = None) -> Any:
        """Read data from a file.

        Parameters
        ----------
        fileDescriptor : `FileDescriptor`
            Identifies the file to read, type to read it into and parameters
            to be used for reading.
        component : `str`, optional
            Component to read from the file. Only used if the `StorageClass`
            for reading differed from the `StorageClass` used to write the
            file.

        Returns
        -------
        inMemoryDataset : `object`
            The requested data as a Python object. The type of object
            is controlled by the specific formatter.

        Raises
        ------
        ValueError
            Component requested but this file does not seem to be a concrete
            composite.
        NotImplementedError
            Formatter does not implement a method to read from files.
        """

        # Read the file naively
        path = self.fileDescriptor.location.path
        data = self._readFile(path, self.fileDescriptor.storageClass.pytype)

        # Assemble the requested dataset and potentially return only its
        # component coercing it to its appropriate pytype
        data = self._assembleDataset(data, component)

        # Special case components by allowing a formatter to return None
        # to indicate that the component was understood but is missing
        if data is None and component is None:
            raise ValueError(f"Unable to read data with URI {self.fileDescriptor.location.uri}")

        return data

    def fromBytes(self, serializedDataset: bytes, component: Optional[str] = None) -> Any:
        """Reads serialized data into a Dataset or its component.

        Parameters
        ----------
        serializedDataset : `bytes`
            Bytes object to unserialize.
        component : `str`, optional
            Component to read from the Dataset. Only used if the `StorageClass`
            for reading differed from the `StorageClass` used to write the
            file.

        Returns
        -------
        inMemoryDataset : `object`
            The requested data as a Python object. The type of object
            is controlled by the specific formatter.

        Raises
        ------
        NotImplementedError
            Formatter does not support reading from bytes.
        """
        if not hasattr(self, "_fromBytes"):
            raise NotImplementedError("Type does not support reading from bytes.")

        data = self._fromBytes(serializedDataset, self.fileDescriptor.storageClass.pytype)

        # Assemble the requested dataset and potentially return only its
        # component coercing it to its appropriate pytype
        data = self._assembleDataset(data, component)

        # Special case components by allowing a formatter to return None
        # to indicate that the component was understood but is missing
        if data is None and component is None:
            nbytes = len(serializedDataset)
            s = "s" if nbytes != 1 else ""
            raise ValueError(
                f"Unable to unpersist {nbytes} byte{s} from URI {self.fileDescriptor.location.uri}"
            )

        return data

    def write(self, inMemoryDataset: Any) -> None:
        """Write a Python object to a file.

        Parameters
        ----------
        inMemoryDataset : `object`
            The Python object to store.

        Returns
        -------
        path : `str`
            The path where the primary file is stored within the datastore.
        """
        fileDescriptor = self.fileDescriptor
        # Update the location with the formatter-preferred file extension
        fileDescriptor.location.updateExtension(self.extension)

        self._writeFile(inMemoryDataset)

    def toBytes(self, inMemoryDataset: Any) -> bytes:
        """Serialize the Dataset to bytes based on formatter.

        Parameters
        ----------
        inMemoryDataset : `object`
            Object to serialize.

        Returns
        -------
        serializedDataset : `bytes`
            Bytes representing the serialized dataset.

        Raises
        ------
        NotImplementedError
            Formatter does not support reading from bytes.
        """
        if not hasattr(self, "_toBytes"):
            raise NotImplementedError("Type does not support reading from bytes.")

        return self._toBytes(inMemoryDataset)
