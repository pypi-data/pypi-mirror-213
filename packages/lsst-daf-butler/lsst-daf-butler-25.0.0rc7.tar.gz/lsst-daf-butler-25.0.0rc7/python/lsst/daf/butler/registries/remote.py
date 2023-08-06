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

__all__ = ("RemoteRegistry",)

import contextlib
import functools
from typing import TYPE_CHECKING, Any, Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Set, Union

import httpx
from lsst.daf.butler import __version__
from lsst.resources import ResourcePath, ResourcePathExpression
from lsst.utils.introspection import get_full_type_name
from lsst.utils.iteration import ensure_iterable

from ..core import (
    Config,
    DataCoordinate,
    DataCoordinateSequence,
    DataId,
    DatasetAssociation,
    DatasetId,
    DatasetRef,
    DatasetType,
    Dimension,
    DimensionConfig,
    DimensionElement,
    DimensionGraph,
    DimensionRecord,
    DimensionUniverse,
    NameLookupMapping,
    SerializedDataCoordinate,
    SerializedDatasetRef,
    SerializedDatasetType,
    SerializedDimensionRecord,
    StorageClassFactory,
    Timespan,
)
from ..core.serverModels import (
    DatasetsQueryParameter,
    ExpressionQueryParameter,
    QueryDataIdsModel,
    QueryDatasetsModel,
    QueryDimensionRecordsModel,
)
from ..registry import (
    CollectionSearch,
    CollectionSummary,
    CollectionType,
    Registry,
    RegistryConfig,
    RegistryDefaults,
)
from ..registry.interfaces import DatasetIdFactory, DatasetIdGenEnum

if TYPE_CHECKING:
    from .._butlerConfig import ButlerConfig
    from ..registry.interfaces import CollectionRecord, DatastoreRegistryBridgeManager


class RemoteRegistry(Registry):
    """Registry that can talk to a remote Butler server.

    Parameters
    ----------
    server_uri : `lsst.resources.ResourcePath`
        URL of the remote Butler server.
    defaults : `RegistryDefaults`
        Default collection search path and/or output `~CollectionType.RUN`
        collection.
    """

    @classmethod
    def createFromConfig(
        cls,
        config: Optional[Union[RegistryConfig, str]] = None,
        dimensionConfig: Optional[Union[DimensionConfig, str]] = None,
        butlerRoot: Optional[ResourcePathExpression] = None,
    ) -> Registry:
        """Create registry database and return `Registry` instance.

        A remote registry can not create a registry database. Calling this
        method will raise an exception.
        """
        raise NotImplementedError("A remote registry can not create a registry.")

    @classmethod
    def fromConfig(
        cls,
        config: Union[ButlerConfig, RegistryConfig, Config, str],
        butlerRoot: Optional[ResourcePathExpression] = None,
        writeable: bool = True,
        defaults: Optional[RegistryDefaults] = None,
    ) -> Registry:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        config = cls.forceRegistryConfig(config)
        config.replaceRoot(butlerRoot)

        if defaults is None:
            defaults = RegistryDefaults()

        server_uri = ResourcePath(config["db"])
        return cls(server_uri, defaults, writeable)

    def __init__(self, server_uri: ResourcePath, defaults: RegistryDefaults, writeable: bool):
        self._db = server_uri
        self._defaults = defaults

        # In the future DatasetIdFactory may become configurable and this
        # instance will need to be shared with datasets manager.
        self.datasetIdFactory = DatasetIdFactory()

        # All PUT calls should be short-circuited if not writeable.
        self._writeable = writeable

        self._dimensions: Optional[DimensionUniverse] = None

        headers = {"user-agent": f"{get_full_type_name(self)}/{__version__}"}
        self._client = httpx.Client(headers=headers)

        # Does each API need to be sent the defaults so that the server
        # can use specific defaults each time?

        # Storage class information should be pulled from server.
        # Dimensions should be pulled from server.

    def __str__(self) -> str:
        return str(self._db)

    def __repr__(self) -> str:
        return f"RemoteRegistry({self._db!r}, {self.dimensions!r})"

    def isWriteable(self) -> bool:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        # Can be used to prevent any PUTs to server
        return self._writeable

    def copy(self, defaults: Optional[RegistryDefaults] = None) -> Registry:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        if defaults is None:
            # No need to copy, because `RegistryDefaults` is immutable; we
            # effectively copy on write.
            defaults = self.defaults
        return type(self)(self._db, defaults, self.isWriteable())

    @property
    def dimensions(self) -> DimensionUniverse:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        if self._dimensions is not None:
            return self._dimensions

        # Access /dimensions.json on server and cache it locally.
        response = self._client.get(str(self._db.join("universe")))
        response.raise_for_status()

        config = DimensionConfig.fromString(response.text, format="json")
        self._dimensions = DimensionUniverse(config)
        return self._dimensions

    def refresh(self) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry

        # Need to determine what to refresh.
        # Might need a server method to return all the DatasetTypes up front.
        pass

    @contextlib.contextmanager
    def transaction(self, *, savepoint: bool = False) -> Iterator[None]:
        # Transaction handling for client server is hard and will require
        # some support in the server to store registry changes and defer
        # committing them. This will likely require a change in transaction
        # interface. For now raise.
        raise NotImplementedError()

    # insertOpaqueData + fetchOpaqueData + deleteOpaqueData
    #    There are no managers for opaque data in client. This implies
    #    that the server would have to have specific implementations for
    #    use by Datastore. DatastoreBridgeManager also is not needed.

    def registerCollection(
        self, name: str, type: CollectionType = CollectionType.TAGGED, doc: Optional[str] = None
    ) -> bool:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    @functools.lru_cache
    def getCollectionType(self, name: str) -> CollectionType:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        # This could use a local cache since collection types won't
        # change.
        path = f"v1/registry/collection/type/{name}"
        response = self._client.get(str(self._db.join(path)))
        response.raise_for_status()
        typeName = response.json()
        return CollectionType.from_name(typeName)

    def _get_collection_record(self, name: str) -> CollectionRecord:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError

    def registerRun(self, name: str, doc: Optional[str] = None) -> bool:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def removeCollection(self, name: str) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def getCollectionChain(self, parent: str) -> CollectionSearch:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        path = f"v1/registry/collection/chain/{parent}"
        response = self._client.get(str(self._db.join(path)))
        response.raise_for_status()
        chain = response.json()
        return CollectionSearch.parse_obj(chain)

    def setCollectionChain(self, parent: str, children: Any, *, flatten: bool = False) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def getCollectionParentChains(self, collection: str) -> Set[str]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def getCollectionDocumentation(self, collection: str) -> Optional[str]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def setCollectionDocumentation(self, collection: str, doc: Optional[str]) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def getCollectionSummary(self, collection: str) -> CollectionSummary:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def registerDatasetType(self, datasetType: DatasetType) -> bool:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def removeDatasetType(self, name: str) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def getDatasetType(self, name: str) -> DatasetType:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def supportsIdGenerationMode(self, mode: DatasetIdGenEnum) -> bool:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def findDataset(
        self,
        datasetType: Union[DatasetType, str],
        dataId: Optional[DataId] = None,
        *,
        collections: Any = None,
        timespan: Optional[Timespan] = None,
        **kwargs: Any,
    ) -> Optional[DatasetRef]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def insertDatasets(
        self,
        datasetType: Union[DatasetType, str],
        dataIds: Iterable[DataId],
        run: Optional[str] = None,
        expand: bool = True,
        idGenerationMode: DatasetIdGenEnum = DatasetIdGenEnum.UNIQUE,
    ) -> List[DatasetRef]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def _importDatasets(
        self,
        datasets: Iterable[DatasetRef],
        expand: bool = True,
        idGenerationMode: DatasetIdGenEnum = DatasetIdGenEnum.UNIQUE,
        reuseIds: bool = False,
    ) -> List[DatasetRef]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def getDataset(self, id: DatasetId) -> Optional[DatasetRef]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def removeDatasets(self, refs: Iterable[DatasetRef]) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def associate(self, collection: str, refs: Iterable[DatasetRef]) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def disassociate(self, collection: str, refs: Iterable[DatasetRef]) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def certify(self, collection: str, refs: Iterable[DatasetRef], timespan: Timespan) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def decertify(
        self,
        collection: str,
        datasetType: Union[str, DatasetType],
        timespan: Timespan,
        *,
        dataIds: Optional[Iterable[DataId]] = None,
    ) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def getDatastoreBridgeManager(self) -> DatastoreRegistryBridgeManager:
        """Return an object that allows a new `Datastore` instance to
        communicate with this `Registry`.

        Returns
        -------
        manager : `DatastoreRegistryBridgeManager`
            Object that mediates communication between this `Registry` and its
            associated datastores.
        """
        from ..tests._dummyRegistry import DummyDatastoreRegistryBridgeManager, DummyOpaqueTableStorageManager

        return DummyDatastoreRegistryBridgeManager(DummyOpaqueTableStorageManager(), self.dimensions, int)

    def getDatasetLocations(self, ref: DatasetRef) -> Iterable[str]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def expandDataId(
        self,
        dataId: Optional[DataId] = None,
        *,
        graph: Optional[DimensionGraph] = None,
        records: Optional[NameLookupMapping[DimensionElement, Optional[DimensionRecord]]] = None,
        withDefaults: bool = True,
        **kwargs: Any,
    ) -> DataCoordinate:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def insertDimensionData(
        self,
        element: Union[DimensionElement, str],
        *data: Union[Mapping[str, Any], DimensionRecord],
        conform: bool = True,
        replace: bool = False,
        skip_existing: bool = False,
    ) -> None:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def syncDimensionData(
        self,
        element: Union[DimensionElement, str],
        row: Union[Mapping[str, Any], DimensionRecord],
        conform: bool = True,
        update: bool = False,
    ) -> Union[bool, Dict[str, Any]]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    def queryDatasetTypes(
        self,
        expression: Any = ...,
        *,
        components: Optional[bool] = None,
        missing: Optional[List[str]] = None,
    ) -> Iterable[DatasetType]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        if missing is not None:
            raise NotImplementedError("RemoteRegistry does not support the 'missing' parameter.")

        params: Dict[str, Any] = {}

        expression = ExpressionQueryParameter.from_expression(expression)
        if expression.regex is not None:
            params["regex"] = expression.regex
        if expression.glob is not None:
            params["glob"] = expression.glob

        path = "v1/registry/datasetTypes"
        if params:
            path += "/re"

        if components is not None:
            params = {"components": components}

        response = self._client.get(str(self._db.join(path)), params=params)
        response.raise_for_status()

        # Really could do with a ListSerializedDatasetType model but for
        # now do it explicitly.
        datasetTypes = response.json()
        return [
            DatasetType.from_simple(SerializedDatasetType(**d), universe=self.dimensions)
            for d in datasetTypes
        ]

    def queryCollections(
        self,
        expression: Any = ...,
        datasetType: Optional[DatasetType] = None,
        collectionTypes: Union[Iterable[CollectionType], CollectionType] = CollectionType.all(),
        flattenChains: bool = False,
        includeChains: Optional[bool] = None,
    ) -> Sequence[str]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        params: Dict[str, Any] = {"flattenChains": flattenChains}

        expression = ExpressionQueryParameter.from_expression(expression)
        if expression.regex is not None:
            params["regex"] = expression.regex
        if expression.glob is not None:
            params["glob"] = expression.glob
        if datasetType is not None:
            params["datasetType"] = datasetType.name
        if includeChains is not None:
            params["includeChains"] = includeChains

        collection_types = [collectionType.name for collectionType in ensure_iterable(collectionTypes)]
        params["collectionType"] = collection_types

        path = "v1/registry/collections"
        response = self._client.get(str(self._db.join(path)), params=params)
        response.raise_for_status()

        collections = response.json()
        return list(collections)

    def queryDatasets(  # type: ignore
        self,
        datasetType: Any,
        *,
        collections: Any = None,
        dimensions: Optional[Iterable[Union[Dimension, str]]] = None,
        dataId: Optional[DataId] = None,
        where: Optional[str] = None,
        findFirst: bool = False,
        components: Optional[bool] = None,
        bind: Optional[Mapping[str, Any]] = None,
        check: bool = True,
        **kwargs: Any,
    ) -> Iterable[DatasetRef]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        if dimensions is not None:
            dimensions = [str(d) for d in ensure_iterable(dimensions)]

        if collections is not None:
            collections = ExpressionQueryParameter.from_expression(collections)

        parameters = QueryDatasetsModel(
            datasetType=ExpressionQueryParameter.from_expression(datasetType),
            collections=collections,
            dimensions=dimensions,
            dataId=dataId,
            where=where,
            findFirst=findFirst,
            components=components,
            bind=bind,
            check=check,
            keyword_args=kwargs,
        )

        response = self._client.post(
            str(self._db.join("v1/registry/datasets")),
            json=parameters.dict(exclude_unset=True, exclude_defaults=True),
            timeout=20,
        )
        response.raise_for_status()

        simple_refs = response.json()
        return (
            DatasetRef.from_simple(SerializedDatasetRef(**r), universe=self.dimensions) for r in simple_refs
        )

    def queryDataIds(  # type: ignore
        self,
        dimensions: Union[Iterable[Union[Dimension, str]], Dimension, str],
        *,
        dataId: Optional[DataId] = None,
        datasets: Any = None,
        collections: Any = None,
        where: Optional[str] = None,
        components: Optional[bool] = None,
        bind: Optional[Mapping[str, Any]] = None,
        check: bool = True,
        **kwargs: Any,
    ) -> DataCoordinateSequence:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        cleaned_dimensions = [str(d) for d in ensure_iterable(dimensions)]

        if collections is not None:
            collections = ExpressionQueryParameter.from_expression(collections)
        if datasets is not None:
            datasets = DatasetsQueryParameter.from_expression(datasets)

        parameters = QueryDataIdsModel(
            dimensions=cleaned_dimensions,
            dataId=dataId,
            collections=collections,
            datasets=datasets,
            where=where,
            components=components,
            bind=bind,
            check=check,
            keyword_args=kwargs,
        )

        response = self._client.post(
            str(self._db.join("v1/registry/dataIds")),
            json=parameters.dict(exclude_unset=True, exclude_defaults=True),
            timeout=20,
        )
        response.raise_for_status()

        simple = response.json()
        dataIds = [
            DataCoordinate.from_simple(SerializedDataCoordinate(**d), universe=self.dimensions)
            for d in simple
        ]
        return DataCoordinateSequence(
            dataIds=dataIds, graph=DimensionGraph(self.dimensions, names=cleaned_dimensions)
        )

    def queryDimensionRecords(  # type: ignore
        self,
        element: Union[DimensionElement, str],
        *,
        dataId: Optional[DataId] = None,
        datasets: Any = None,
        collections: Any = None,
        where: Optional[str] = None,
        components: Optional[bool] = None,
        bind: Optional[Mapping[str, Any]] = None,
        check: bool = True,
        **kwargs: Any,
    ) -> Iterator[DimensionRecord]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        if collections is not None:
            collections = ExpressionQueryParameter.from_expression(collections)
        if datasets is not None:
            datasets = DatasetsQueryParameter.from_expression(datasets)

        parameters = QueryDimensionRecordsModel(
            dataId=dataId,
            datasets=datasets,
            collections=collections,
            where=where,
            components=components,
            bind=bind,
            check=check,
            keyword_args=kwargs,
        )
        response = self._client.post(
            str(self._db.join(f"v1/registry/dimensionRecords/{element}")),
            json=parameters.dict(exclude_unset=True, exclude_defaults=True),
            timeout=20,
        )
        response.raise_for_status()

        simple_records = response.json()

        return (
            DimensionRecord.from_simple(SerializedDimensionRecord(**r), universe=self.dimensions)
            for r in simple_records
        )

    def queryDatasetAssociations(
        self,
        datasetType: Union[str, DatasetType],
        collections: Any = ...,
        *,
        collectionTypes: Iterable[CollectionType] = CollectionType.all(),
        flattenChains: bool = False,
    ) -> Iterator[DatasetAssociation]:
        # Docstring inherited from lsst.daf.butler.registry.Registry
        raise NotImplementedError()

    storageClasses: StorageClassFactory
    """All storage classes known to the registry (`StorageClassFactory`).
    """
