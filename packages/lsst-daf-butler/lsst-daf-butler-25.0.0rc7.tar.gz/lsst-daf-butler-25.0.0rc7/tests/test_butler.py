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

"""Tests for Butler.
"""

import gc
import logging
import os
import pathlib
import pickle
import posixpath
import random
import shutil
import socket
import string
import tempfile
import time
import unittest
from tempfile import gettempdir
from threading import Thread

try:
    import boto3
    import botocore
    from moto import mock_s3
except ImportError:
    boto3 = None

    def mock_s3(cls):
        """A no-op decorator in case moto mock_s3 can not be imported."""
        return cls


try:
    # It's possible but silly to have testing.postgresql installed without
    # having the postgresql server installed (because then nothing in
    # testing.postgresql would work), so we use the presence of that module
    # to test whether we can expect the server to be available.
    import testing.postgresql
except ImportError:
    testing = None


try:
    from cheroot import wsgi
    from wsgidav.wsgidav_app import WsgiDAVApp
except ImportError:
    WsgiDAVApp = None

import astropy.time
import sqlalchemy
from lsst.daf.butler import (
    Butler,
    ButlerConfig,
    CollectionType,
    Config,
    DatasetIdGenEnum,
    DatasetRef,
    DatasetType,
    FileDataset,
    FileTemplate,
    FileTemplateValidationError,
    StorageClassFactory,
    ValidationError,
    script,
)
from lsst.daf.butler.core.repoRelocation import BUTLER_ROOT_TAG
from lsst.daf.butler.registry import (
    CollectionError,
    CollectionTypeError,
    ConflictingDefinitionError,
    DataIdValueError,
    MissingCollectionError,
)
from lsst.daf.butler.tests import MetricsExample, MultiDetectorFormatter
from lsst.daf.butler.tests.utils import makeTestTempDir, removeTestTempDir, safeTestTempDir
from lsst.resources import ResourcePath
from lsst.resources.http import _is_webdav_endpoint
from lsst.resources.s3utils import setAwsEnvCredentials, unsetAwsEnvCredentials
from lsst.utils import doImport
from lsst.utils.introspection import get_full_type_name

TESTDIR = os.path.abspath(os.path.dirname(__file__))


def makeExampleMetrics():
    return MetricsExample(
        {"AM1": 5.2, "AM2": 30.6},
        {"a": [1, 2, 3], "b": {"blue": 5, "red": "green"}},
        [563, 234, 456.7, 752, 8, 9, 27],
    )


class TransactionTestError(Exception):
    """Specific error for testing transactions, to prevent misdiagnosing
    that might otherwise occur when a standard exception is used.
    """

    pass


class ButlerConfigTests(unittest.TestCase):
    """Simple tests for ButlerConfig that are not tested in any other test
    cases."""

    def testSearchPath(self):
        configFile = os.path.join(TESTDIR, "config", "basic", "butler.yaml")
        with self.assertLogs("lsst.daf.butler", level="DEBUG") as cm:
            config1 = ButlerConfig(configFile)
        self.assertNotIn("testConfigs", "\n".join(cm.output))

        overrideDirectory = os.path.join(TESTDIR, "config", "testConfigs")
        with self.assertLogs("lsst.daf.butler", level="DEBUG") as cm:
            config2 = ButlerConfig(configFile, searchPaths=[overrideDirectory])
        self.assertIn("testConfigs", "\n".join(cm.output))

        key = ("datastore", "records", "table")
        self.assertNotEqual(config1[key], config2[key])
        self.assertEqual(config2[key], "override_record")


class ButlerPutGetTests:
    """Helper method for running a suite of put/get tests from different
    butler configurations."""

    root = None
    default_run = "ingésτ😺"

    @staticmethod
    def addDatasetType(datasetTypeName, dimensions, storageClass, registry):
        """Create a DatasetType and register it"""
        datasetType = DatasetType(datasetTypeName, dimensions, storageClass)
        registry.registerDatasetType(datasetType)
        return datasetType

    @classmethod
    def setUpClass(cls):
        cls.storageClassFactory = StorageClassFactory()
        cls.storageClassFactory.addFromConfig(cls.configFile)

    def assertGetComponents(self, butler, datasetRef, components, reference, collections=None):
        datasetType = datasetRef.datasetType
        dataId = datasetRef.dataId
        deferred = butler.getDirectDeferred(datasetRef)

        for component in components:
            compTypeName = datasetType.componentTypeName(component)
            result = butler.get(compTypeName, dataId, collections=collections)
            self.assertEqual(result, getattr(reference, component))
            result_deferred = deferred.get(component=component)
            self.assertEqual(result_deferred, result)

    def tearDown(self):
        removeTestTempDir(self.root)

    def create_butler(self, run, storageClass, datasetTypeName):
        butler = Butler(self.tmpConfigFile, run=run)

        collections = set(butler.registry.queryCollections())
        self.assertEqual(collections, set([run]))

        # Create and register a DatasetType
        dimensions = butler.registry.dimensions.extract(["instrument", "visit"])

        datasetType = self.addDatasetType(datasetTypeName, dimensions, storageClass, butler.registry)

        # Add needed Dimensions
        butler.registry.insertDimensionData("instrument", {"name": "DummyCamComp"})
        butler.registry.insertDimensionData(
            "physical_filter", {"instrument": "DummyCamComp", "name": "d-r", "band": "R"}
        )
        butler.registry.insertDimensionData(
            "visit_system", {"instrument": "DummyCamComp", "id": 1, "name": "default"}
        )
        visit_start = astropy.time.Time("2020-01-01 08:00:00.123456789", scale="tai")
        visit_end = astropy.time.Time("2020-01-01 08:00:36.66", scale="tai")
        butler.registry.insertDimensionData(
            "visit",
            {
                "instrument": "DummyCamComp",
                "id": 423,
                "name": "fourtwentythree",
                "physical_filter": "d-r",
                "visit_system": 1,
                "datetime_begin": visit_start,
                "datetime_end": visit_end,
            },
        )

        # Add more visits for some later tests
        for visit_id in (424, 425):
            butler.registry.insertDimensionData(
                "visit",
                {
                    "instrument": "DummyCamComp",
                    "id": visit_id,
                    "name": f"fourtwentyfour_{visit_id}",
                    "physical_filter": "d-r",
                    "visit_system": 1,
                },
            )
        return butler, datasetType

    def runPutGetTest(self, storageClass, datasetTypeName):
        # New datasets will be added to run and tag, but we will only look in
        # tag when looking up datasets.
        run = self.default_run
        butler, datasetType = self.create_butler(run, storageClass, datasetTypeName)

        # Create and store a dataset
        metric = makeExampleMetrics()
        dataId = {"instrument": "DummyCamComp", "visit": 423}

        # Create a DatasetRef for put
        refIn = DatasetRef(datasetType, dataId, id=None)

        # Put with a preexisting id should fail
        with self.assertRaises(ValueError):
            butler.put(metric, DatasetRef(datasetType, dataId, id=100))

        # Put and remove the dataset once as a DatasetRef, once as a dataId,
        # and once with a DatasetType

        # Keep track of any collections we add and do not clean up
        expected_collections = {run}

        counter = 0
        for args in ((refIn,), (datasetTypeName, dataId), (datasetType, dataId)):
            # Since we are using subTest we can get cascading failures
            # here with the first attempt failing and the others failing
            # immediately because the dataset already exists. Work around
            # this by using a distinct run collection each time
            counter += 1
            this_run = f"put_run_{counter}"
            butler.registry.registerCollection(this_run, type=CollectionType.RUN)
            expected_collections.update({this_run})

            with self.subTest(args=args):
                ref = butler.put(metric, *args, run=this_run)
                self.assertIsInstance(ref, DatasetRef)

                # Test getDirect
                metricOut = butler.getDirect(ref)
                self.assertEqual(metric, metricOut)
                # Test get
                metricOut = butler.get(ref.datasetType.name, dataId, collections=this_run)
                self.assertEqual(metric, metricOut)
                # Test get with a datasetRef
                metricOut = butler.get(ref, collections=this_run)
                self.assertEqual(metric, metricOut)
                # Test getDeferred with dataId
                metricOut = butler.getDeferred(ref.datasetType.name, dataId, collections=this_run).get()
                self.assertEqual(metric, metricOut)
                # Test getDeferred with a datasetRef
                metricOut = butler.getDeferred(ref, collections=this_run).get()
                self.assertEqual(metric, metricOut)
                # and deferred direct with ref
                metricOut = butler.getDirectDeferred(ref).get()
                self.assertEqual(metric, metricOut)

                # Check we can get components
                if storageClass.isComposite():
                    self.assertGetComponents(
                        butler, ref, ("summary", "data", "output"), metric, collections=this_run
                    )

                # Can the artifacts themselves be retrieved?
                if not butler.datastore.isEphemeral:
                    root_uri = ResourcePath(self.root)

                    for preserve_path in (True, False):
                        destination = root_uri.join(f"artifacts/{preserve_path}_{counter}/")
                        # Use copy so that we can test that overwrite
                        # protection works (using "auto" for File URIs would
                        # use hard links and subsequent transfer would work
                        # because it knows they are the same file).
                        transferred = butler.retrieveArtifacts(
                            [ref], destination, preserve_path=preserve_path, transfer="copy"
                        )
                        self.assertGreater(len(transferred), 0)
                        artifacts = list(ResourcePath.findFileResources([destination]))
                        self.assertEqual(set(transferred), set(artifacts))

                        for artifact in transferred:
                            path_in_destination = artifact.relative_to(destination)
                            self.assertIsNotNone(path_in_destination)

                            # when path is not preserved there should not be
                            # any path separators.
                            num_seps = path_in_destination.count("/")
                            if preserve_path:
                                self.assertGreater(num_seps, 0)
                            else:
                                self.assertEqual(num_seps, 0)

                        primary_uri, secondary_uris = butler.datastore.getURIs(ref)
                        n_uris = len(secondary_uris)
                        if primary_uri:
                            n_uris += 1
                        self.assertEqual(
                            len(artifacts),
                            n_uris,
                            "Comparing expected artifacts vs actual:"
                            f" {artifacts} vs {primary_uri} and {secondary_uris}",
                        )

                        if preserve_path:
                            # No need to run these twice
                            with self.assertRaises(ValueError):
                                butler.retrieveArtifacts([ref], destination, transfer="move")

                            with self.assertRaises(FileExistsError):
                                butler.retrieveArtifacts([ref], destination)

                            transferred_again = butler.retrieveArtifacts(
                                [ref], destination, preserve_path=preserve_path, overwrite=True
                            )
                            self.assertEqual(set(transferred_again), set(transferred))

                # Now remove the dataset completely.
                butler.pruneDatasets([ref], purge=True, unstore=True)
                # Lookup with original args should still fail.
                with self.assertRaises(LookupError):
                    butler.datasetExists(*args, collections=this_run)
                # getDirect() should still fail.
                with self.assertRaises(FileNotFoundError):
                    butler.getDirect(ref)
                # Registry shouldn't be able to find it by dataset_id anymore.
                self.assertIsNone(butler.registry.getDataset(ref.id))

                # Do explicit registry removal since we know they are
                # empty
                butler.registry.removeCollection(this_run)
                expected_collections.remove(this_run)

        # Put the dataset again, since the last thing we did was remove it
        # and we want to use the default collection.
        ref = butler.put(metric, refIn)

        # Get with parameters
        stop = 4
        sliced = butler.get(ref, parameters={"slice": slice(stop)})
        self.assertNotEqual(metric, sliced)
        self.assertEqual(metric.summary, sliced.summary)
        self.assertEqual(metric.output, sliced.output)
        self.assertEqual(metric.data[:stop], sliced.data)
        # getDeferred with parameters
        sliced = butler.getDeferred(ref, parameters={"slice": slice(stop)}).get()
        self.assertNotEqual(metric, sliced)
        self.assertEqual(metric.summary, sliced.summary)
        self.assertEqual(metric.output, sliced.output)
        self.assertEqual(metric.data[:stop], sliced.data)
        # getDeferred with deferred parameters
        sliced = butler.getDeferred(ref).get(parameters={"slice": slice(stop)})
        self.assertNotEqual(metric, sliced)
        self.assertEqual(metric.summary, sliced.summary)
        self.assertEqual(metric.output, sliced.output)
        self.assertEqual(metric.data[:stop], sliced.data)

        if storageClass.isComposite():
            # Check that components can be retrieved
            metricOut = butler.get(ref.datasetType.name, dataId)
            compNameS = ref.datasetType.componentTypeName("summary")
            compNameD = ref.datasetType.componentTypeName("data")
            summary = butler.get(compNameS, dataId)
            self.assertEqual(summary, metric.summary)
            data = butler.get(compNameD, dataId)
            self.assertEqual(data, metric.data)

            if "counter" in storageClass.derivedComponents:
                count = butler.get(ref.datasetType.componentTypeName("counter"), dataId)
                self.assertEqual(count, len(data))

                count = butler.get(
                    ref.datasetType.componentTypeName("counter"), dataId, parameters={"slice": slice(stop)}
                )
                self.assertEqual(count, stop)

            compRef = butler.registry.findDataset(compNameS, dataId, collections=butler.collections)
            summary = butler.getDirect(compRef)
            self.assertEqual(summary, metric.summary)

        # Create a Dataset type that has the same name but is inconsistent.
        inconsistentDatasetType = DatasetType(
            datasetTypeName, datasetType.dimensions, self.storageClassFactory.getStorageClass("Config")
        )

        # Getting with a dataset type that does not match registry fails
        with self.assertRaises(ValueError):
            butler.get(inconsistentDatasetType, dataId)

        # Combining a DatasetRef with a dataId should fail
        with self.assertRaises(ValueError):
            butler.get(ref, dataId)
        # Getting with an explicit ref should fail if the id doesn't match
        with self.assertRaises(ValueError):
            butler.get(DatasetRef(ref.datasetType, ref.dataId, id=101))

        # Getting a dataset with unknown parameters should fail
        with self.assertRaises(KeyError):
            butler.get(ref, parameters={"unsupported": True})

        # Check we have a collection
        collections = set(butler.registry.queryCollections())
        self.assertEqual(collections, expected_collections)

        # Clean up to check that we can remove something that may have
        # already had a component removed
        butler.pruneDatasets([ref], unstore=True, purge=True)

        # Check that we can configure a butler to accept a put even
        # if it already has the dataset in registry.
        ref = butler.put(metric, refIn)

        # Repeat put will fail.
        with self.assertRaises(ConflictingDefinitionError):
            butler.put(metric, refIn)

        # Remove the datastore entry.
        butler.pruneDatasets([ref], unstore=True, purge=False, disassociate=False)

        # Put will still fail
        with self.assertRaises(ConflictingDefinitionError):
            butler.put(metric, refIn)

        # Allow the put to succeed
        butler._allow_put_of_predefined_dataset = True
        ref2 = butler.put(metric, refIn)
        self.assertEqual(ref2.id, ref.id)

        # A second put will still fail but with a different exception
        # than before.
        with self.assertRaises(ConflictingDefinitionError):
            butler.put(metric, refIn)

        # Reset the flag to avoid confusion
        butler._allow_put_of_predefined_dataset = False

        # Leave the dataset in place since some downstream tests require
        # something to be present

        return butler

    def testDeferredCollectionPassing(self):
        # Construct a butler with no run or collection, but make it writeable.
        butler = Butler(self.tmpConfigFile, writeable=True)
        # Create and register a DatasetType
        dimensions = butler.registry.dimensions.extract(["instrument", "visit"])
        datasetType = self.addDatasetType(
            "example", dimensions, self.storageClassFactory.getStorageClass("StructuredData"), butler.registry
        )
        # Add needed Dimensions
        butler.registry.insertDimensionData("instrument", {"name": "DummyCamComp"})
        butler.registry.insertDimensionData(
            "physical_filter", {"instrument": "DummyCamComp", "name": "d-r", "band": "R"}
        )
        butler.registry.insertDimensionData(
            "visit",
            {"instrument": "DummyCamComp", "id": 423, "name": "fourtwentythree", "physical_filter": "d-r"},
        )
        dataId = {"instrument": "DummyCamComp", "visit": 423}
        # Create dataset.
        metric = makeExampleMetrics()
        # Register a new run and put dataset.
        run = "deferred"
        self.assertTrue(butler.registry.registerRun(run))
        # Second time it will be allowed but indicate no-op
        self.assertFalse(butler.registry.registerRun(run))
        ref = butler.put(metric, datasetType, dataId, run=run)
        # Putting with no run should fail with TypeError.
        with self.assertRaises(CollectionError):
            butler.put(metric, datasetType, dataId)
        # Dataset should exist.
        self.assertTrue(butler.datasetExists(datasetType, dataId, collections=[run]))
        # We should be able to get the dataset back, but with and without
        # a deferred dataset handle.
        self.assertEqual(metric, butler.get(datasetType, dataId, collections=[run]))
        self.assertEqual(metric, butler.getDeferred(datasetType, dataId, collections=[run]).get())
        # Trying to find the dataset without any collection is a TypeError.
        with self.assertRaises(CollectionError):
            butler.datasetExists(datasetType, dataId)
        with self.assertRaises(CollectionError):
            butler.get(datasetType, dataId)
        # Associate the dataset with a different collection.
        butler.registry.registerCollection("tagged")
        butler.registry.associate("tagged", [ref])
        # Deleting the dataset from the new collection should make it findable
        # in the original collection.
        butler.pruneDatasets([ref], tags=["tagged"])
        self.assertTrue(butler.datasetExists(datasetType, dataId, collections=[run]))


class ButlerTests(ButlerPutGetTests):
    """Tests for Butler."""

    useTempRoot = True

    def setUp(self):
        """Create a new butler root for each test."""
        self.root = makeTestTempDir(TESTDIR)
        Butler.makeRepo(self.root, config=Config(self.configFile))
        self.tmpConfigFile = os.path.join(self.root, "butler.yaml")

    def testConstructor(self):
        """Independent test of constructor."""
        butler = Butler(self.tmpConfigFile, run=self.default_run)
        self.assertIsInstance(butler, Butler)

        # Check that butler.yaml is added automatically.
        if self.tmpConfigFile.endswith(end := "/butler.yaml"):
            config_dir = self.tmpConfigFile[: -len(end)]
            butler = Butler(config_dir, run=self.default_run)
            self.assertIsInstance(butler, Butler)

            # Even with a ResourcePath.
            butler = Butler(ResourcePath(config_dir, forceDirectory=True), run=self.default_run)
            self.assertIsInstance(butler, Butler)

        collections = set(butler.registry.queryCollections())
        self.assertEqual(collections, {self.default_run})

        # Check that some special characters can be included in run name.
        special_run = "u@b.c-A"
        butler_special = Butler(butler=butler, run=special_run)
        collections = set(butler_special.registry.queryCollections("*@*"))
        self.assertEqual(collections, {special_run})

        butler2 = Butler(butler=butler, collections=["other"])
        self.assertEqual(butler2.collections, ("other",))
        self.assertIsNone(butler2.run)
        self.assertIs(butler.datastore, butler2.datastore)

        # Test that we can use an environment variable to find this
        # repository.
        butler_index = Config()
        butler_index["label"] = self.tmpConfigFile
        for suffix in (".yaml", ".json"):
            # Ensure that the content differs so that we know that
            # we aren't reusing the cache.
            bad_label = f"s3://bucket/not_real{suffix}"
            butler_index["bad_label"] = bad_label
            with ResourcePath.temporary_uri(suffix=suffix) as temp_file:
                butler_index.dumpToUri(temp_file)
                with unittest.mock.patch.dict(os.environ, {"DAF_BUTLER_REPOSITORY_INDEX": str(temp_file)}):
                    self.assertEqual(Butler.get_known_repos(), set(("label", "bad_label")))
                    uri = Butler.get_repo_uri("bad_label")
                    self.assertEqual(uri, ResourcePath(bad_label))
                    uri = Butler.get_repo_uri("label")
                    butler = Butler(uri, writeable=False)
                    self.assertIsInstance(butler, Butler)
                    butler = Butler("label", writeable=False)
                    self.assertIsInstance(butler, Butler)
                    with self.assertRaisesRegex(FileNotFoundError, "aliases:.*bad_label"):
                        Butler("not_there", writeable=False)
                    with self.assertRaises(KeyError) as cm:
                        Butler.get_repo_uri("missing")
                    self.assertIn("not known to", str(cm.exception))
        with unittest.mock.patch.dict(os.environ, {"DAF_BUTLER_REPOSITORY_INDEX": "file://not_found/x.yaml"}):
            with self.assertRaises(FileNotFoundError):
                Butler.get_repo_uri("label")
            self.assertEqual(Butler.get_known_repos(), set())
        with self.assertRaises(KeyError) as cm:
            # No environment variable set.
            Butler.get_repo_uri("label")
        self.assertIn("No repository index defined", str(cm.exception))
        with self.assertRaisesRegex(FileNotFoundError, "no known aliases"):
            # No aliases registered.
            Butler("not_there")
        self.assertEqual(Butler.get_known_repos(), set())

    def testBasicPutGet(self):
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        self.runPutGetTest(storageClass, "test_metric")

    def testCompositePutGetConcrete(self):
        storageClass = self.storageClassFactory.getStorageClass("StructuredCompositeReadCompNoDisassembly")
        butler = self.runPutGetTest(storageClass, "test_metric")

        # Should *not* be disassembled
        datasets = list(butler.registry.queryDatasets(..., collections=self.default_run))
        self.assertEqual(len(datasets), 1)
        uri, components = butler.getURIs(datasets[0])
        self.assertIsInstance(uri, ResourcePath)
        self.assertFalse(components)
        self.assertEqual(uri.fragment, "", f"Checking absence of fragment in {uri}")
        self.assertIn("423", str(uri), f"Checking visit is in URI {uri}")

        # Predicted dataset
        dataId = {"instrument": "DummyCamComp", "visit": 424}
        uri, components = butler.getURIs(datasets[0].datasetType, dataId=dataId, predict=True)
        self.assertFalse(components)
        self.assertIsInstance(uri, ResourcePath)
        self.assertIn("424", str(uri), f"Checking visit is in URI {uri}")
        self.assertEqual(uri.fragment, "predicted", f"Checking for fragment in {uri}")

    def testCompositePutGetVirtual(self):
        storageClass = self.storageClassFactory.getStorageClass("StructuredCompositeReadComp")
        butler = self.runPutGetTest(storageClass, "test_metric_comp")

        # Should be disassembled
        datasets = list(butler.registry.queryDatasets(..., collections=self.default_run))
        self.assertEqual(len(datasets), 1)
        uri, components = butler.getURIs(datasets[0])

        if butler.datastore.isEphemeral:
            # Never disassemble in-memory datastore
            self.assertIsInstance(uri, ResourcePath)
            self.assertFalse(components)
            self.assertEqual(uri.fragment, "", f"Checking absence of fragment in {uri}")
            self.assertIn("423", str(uri), f"Checking visit is in URI {uri}")
        else:
            self.assertIsNone(uri)
            self.assertEqual(set(components), set(storageClass.components))
            for compuri in components.values():
                self.assertIsInstance(compuri, ResourcePath)
                self.assertIn("423", str(compuri), f"Checking visit is in URI {compuri}")
                self.assertEqual(compuri.fragment, "", f"Checking absence of fragment in {compuri}")

        # Predicted dataset
        dataId = {"instrument": "DummyCamComp", "visit": 424}
        uri, components = butler.getURIs(datasets[0].datasetType, dataId=dataId, predict=True)

        if butler.datastore.isEphemeral:
            # Never disassembled
            self.assertIsInstance(uri, ResourcePath)
            self.assertFalse(components)
            self.assertIn("424", str(uri), f"Checking visit is in URI {uri}")
            self.assertEqual(uri.fragment, "predicted", f"Checking for fragment in {uri}")
        else:
            self.assertIsNone(uri)
            self.assertEqual(set(components), set(storageClass.components))
            for compuri in components.values():
                self.assertIsInstance(compuri, ResourcePath)
                self.assertIn("424", str(compuri), f"Checking visit is in URI {compuri}")
                self.assertEqual(compuri.fragment, "predicted", f"Checking for fragment in {compuri}")

    def testStorageClassOverrideGet(self):
        """Test storage class conversion on get with override."""
        storageClass = self.storageClassFactory.getStorageClass("StructuredData")
        datasetTypeName = "anything"
        run = self.default_run

        butler, datasetType = self.create_butler(run, storageClass, datasetTypeName)

        # Create and store a dataset.
        metric = makeExampleMetrics()
        dataId = {"instrument": "DummyCamComp", "visit": 423}

        ref = butler.put(metric, datasetType, dataId)

        # Return native type.
        retrieved = butler.get(ref)
        self.assertEqual(retrieved, metric)

        # Specify an override.
        new_sc = self.storageClassFactory.getStorageClass("MetricsConversion")
        model = butler.getDirect(ref, storageClass=new_sc)
        self.assertNotEqual(type(model), type(retrieved))
        self.assertIs(type(model), new_sc.pytype)
        self.assertEqual(retrieved, model)

        # Defer but override later.
        deferred = butler.getDirectDeferred(ref)
        model = deferred.get(storageClass=new_sc)
        self.assertIs(type(model), new_sc.pytype)
        self.assertEqual(retrieved, model)

        # Defer but override up front.
        deferred = butler.getDirectDeferred(ref, storageClass=new_sc)
        model = deferred.get()
        self.assertIs(type(model), new_sc.pytype)
        self.assertEqual(retrieved, model)

        # Retrieve a component. Should be a tuple.
        data = butler.get("anything.data", dataId, storageClass="StructuredDataDataTestTuple")
        self.assertIs(type(data), tuple)
        self.assertEqual(data, tuple(retrieved.data))

        # Parameter on the write storage class should work regardless
        # of read storage class.
        data = butler.get(
            "anything.data",
            dataId,
            storageClass="StructuredDataDataTestTuple",
            parameters={"slice": slice(2, 4)},
        )
        self.assertEqual(len(data), 2)

        # Try a parameter that is known to the read storage class but not
        # the write storage class.
        with self.assertRaises(KeyError):
            butler.get(
                "anything.data",
                dataId,
                storageClass="StructuredDataDataTestTuple",
                parameters={"xslice": slice(2, 4)},
            )

    def testPytypePutCoercion(self):
        """Test python type coercion on Butler.get and put."""

        # Store some data with the normal example storage class.
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        datasetTypeName = "test_metric"
        butler, _ = self.create_butler(self.default_run, storageClass, datasetTypeName)

        dataId = {"instrument": "DummyCamComp", "visit": 423}

        # Put a dict and this should coerce to a MetricsExample
        test_dict = {"summary": {"a": 1}, "output": {"b": 2}}
        metric_ref = butler.put(test_dict, datasetTypeName, dataId=dataId, visit=424)
        test_metric = butler.getDirect(metric_ref)
        self.assertEqual(get_full_type_name(test_metric), "lsst.daf.butler.tests.MetricsExample")
        self.assertEqual(test_metric.summary, test_dict["summary"])
        self.assertEqual(test_metric.output, test_dict["output"])

        # Check that the put still works if a DatasetType is given with
        # a definition matching this python type.
        registry_type = butler.registry.getDatasetType(datasetTypeName)
        this_type = DatasetType(datasetTypeName, registry_type.dimensions, "StructuredDataDictJson")
        metric2_ref = butler.put(test_dict, this_type, dataId=dataId, visit=425)
        self.assertEqual(metric2_ref.datasetType, registry_type)

        # The get will return the type expected by registry.
        test_metric2 = butler.getDirect(metric2_ref)
        self.assertEqual(get_full_type_name(test_metric2), "lsst.daf.butler.tests.MetricsExample")

        # Make a new DatasetRef with the compatible but different DatasetType.
        # This should now return a dict.
        new_ref = DatasetRef(this_type, metric2_ref.dataId, id=metric2_ref.id, run=metric2_ref.run)
        test_dict2 = butler.getDirect(new_ref)
        self.assertEqual(get_full_type_name(test_dict2), "dict")

        # Get it again with the wrong dataset type definition using get()
        # rather than getDirect(). This should be consistent with getDirect()
        # behavior and return the type of the DatasetType.
        test_dict3 = butler.get(this_type, dataId=dataId, visit=425)
        self.assertEqual(get_full_type_name(test_dict3), "dict")

    def testIngest(self):
        butler = Butler(self.tmpConfigFile, run=self.default_run)

        # Create and register a DatasetType
        dimensions = butler.registry.dimensions.extract(["instrument", "visit", "detector"])

        storageClass = self.storageClassFactory.getStorageClass("StructuredDataDictYaml")
        datasetTypeName = "metric"

        datasetType = self.addDatasetType(datasetTypeName, dimensions, storageClass, butler.registry)

        # Add needed Dimensions
        butler.registry.insertDimensionData("instrument", {"name": "DummyCamComp"})
        butler.registry.insertDimensionData(
            "physical_filter", {"instrument": "DummyCamComp", "name": "d-r", "band": "R"}
        )
        for detector in (1, 2):
            butler.registry.insertDimensionData(
                "detector", {"instrument": "DummyCamComp", "id": detector, "full_name": f"detector{detector}"}
            )

        butler.registry.insertDimensionData(
            "visit",
            {"instrument": "DummyCamComp", "id": 423, "name": "fourtwentythree", "physical_filter": "d-r"},
            {"instrument": "DummyCamComp", "id": 424, "name": "fourtwentyfour", "physical_filter": "d-r"},
        )

        formatter = doImport("lsst.daf.butler.formatters.yaml.YamlFormatter")
        dataRoot = os.path.join(TESTDIR, "data", "basic")
        datasets = []
        for detector in (1, 2):
            detector_name = f"detector_{detector}"
            metricFile = os.path.join(dataRoot, f"{detector_name}.yaml")
            dataId = {"instrument": "DummyCamComp", "visit": 423, "detector": detector}
            # Create a DatasetRef for ingest
            refIn = DatasetRef(datasetType, dataId, id=None)

            datasets.append(FileDataset(path=metricFile, refs=[refIn], formatter=formatter))

        butler.ingest(*datasets, transfer="copy")

        dataId1 = {"instrument": "DummyCamComp", "detector": 1, "visit": 423}
        dataId2 = {"instrument": "DummyCamComp", "detector": 2, "visit": 423}

        metrics1 = butler.get(datasetTypeName, dataId1)
        metrics2 = butler.get(datasetTypeName, dataId2)
        self.assertNotEqual(metrics1, metrics2)

        # Compare URIs
        uri1 = butler.getURI(datasetTypeName, dataId1)
        uri2 = butler.getURI(datasetTypeName, dataId2)
        self.assertNotEqual(uri1, uri2)

        # Now do a multi-dataset but single file ingest
        metricFile = os.path.join(dataRoot, "detectors.yaml")
        refs = []
        for detector in (1, 2):
            detector_name = f"detector_{detector}"
            dataId = {"instrument": "DummyCamComp", "visit": 424, "detector": detector}
            # Create a DatasetRef for ingest
            refs.append(DatasetRef(datasetType, dataId, id=None))

        # Test "move" transfer to ensure that the files themselves
        # have disappeared following ingest.
        with ResourcePath.temporary_uri(suffix=".yaml") as tempFile:
            tempFile.transfer_from(ResourcePath(metricFile), transfer="copy")

            datasets = []
            datasets.append(FileDataset(path=tempFile, refs=refs, formatter=MultiDetectorFormatter))

            butler.ingest(*datasets, transfer="move", record_validation_info=False)
            self.assertFalse(tempFile.exists())

        # Check that the datastore recorded no file size.
        # Not all datastores can support this.
        try:
            infos = butler.datastore.getStoredItemsInfo(datasets[0].refs[0])
            self.assertEqual(infos[0].file_size, -1)
        except AttributeError:
            pass

        dataId1 = {"instrument": "DummyCamComp", "detector": 1, "visit": 424}
        dataId2 = {"instrument": "DummyCamComp", "detector": 2, "visit": 424}

        multi1 = butler.get(datasetTypeName, dataId1)
        multi2 = butler.get(datasetTypeName, dataId2)

        self.assertEqual(multi1, metrics1)
        self.assertEqual(multi2, metrics2)

        # Compare URIs
        uri1 = butler.getURI(datasetTypeName, dataId1)
        uri2 = butler.getURI(datasetTypeName, dataId2)
        self.assertEqual(uri1, uri2, f"Cf. {uri1} with {uri2}")

        # Test that removing one does not break the second
        # This line will issue a warning log message for a ChainedDatastore
        # that uses an InMemoryDatastore since in-memory can not ingest
        # files.
        butler.pruneDatasets([datasets[0].refs[0]], unstore=True, disassociate=False)
        self.assertFalse(butler.datasetExists(datasetTypeName, dataId1))
        self.assertTrue(butler.datasetExists(datasetTypeName, dataId2))
        multi2b = butler.get(datasetTypeName, dataId2)
        self.assertEqual(multi2, multi2b)

    def testPruneCollections(self):
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        butler = Butler(self.tmpConfigFile, writeable=True)
        # Load registry data with dimensions to hang datasets off of.
        registryDataDir = os.path.normpath(os.path.join(os.path.dirname(__file__), "data", "registry"))
        butler.import_(filename=os.path.join(registryDataDir, "base.yaml"))
        # Add some RUN-type collections.
        run1 = "run1"
        butler.registry.registerRun(run1)
        run2 = "run2"
        butler.registry.registerRun(run2)
        # put some datasets.  ref1 and ref2 have the same data ID, and are in
        # different runs.  ref3 has a different data ID.
        metric = makeExampleMetrics()
        dimensions = butler.registry.dimensions.extract(["instrument", "physical_filter"])
        datasetType = self.addDatasetType(
            "prune_collections_test_dataset", dimensions, storageClass, butler.registry
        )
        ref1 = butler.put(metric, datasetType, {"instrument": "Cam1", "physical_filter": "Cam1-G"}, run=run1)
        ref2 = butler.put(metric, datasetType, {"instrument": "Cam1", "physical_filter": "Cam1-G"}, run=run2)
        ref3 = butler.put(metric, datasetType, {"instrument": "Cam1", "physical_filter": "Cam1-R1"}, run=run1)

        # Try to delete a RUN collection without purge, or with purge and not
        # unstore.
        with self.assertRaises(TypeError):
            butler.pruneCollection(run1)
        with self.assertRaises(TypeError):
            butler.pruneCollection(run2, purge=True)
        # Add a TAGGED collection and associate ref3 only into it.
        tag1 = "tag1"
        registered = butler.registry.registerCollection(tag1, type=CollectionType.TAGGED)
        self.assertTrue(registered)
        # Registering a second time should be allowed.
        registered = butler.registry.registerCollection(tag1, type=CollectionType.TAGGED)
        self.assertFalse(registered)
        butler.registry.associate(tag1, [ref3])
        # Add a CHAINED collection that searches run1 and then run2.  It
        # logically contains only ref1, because ref2 is shadowed due to them
        # having the same data ID and dataset type.
        chain1 = "chain1"
        butler.registry.registerCollection(chain1, type=CollectionType.CHAINED)
        butler.registry.setCollectionChain(chain1, [run1, run2])
        # Try to delete RUN collections, which should fail with complete
        # rollback because they're still referenced by the CHAINED
        # collection.
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            butler.pruneCollection(run1, purge=True, unstore=True)
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            butler.pruneCollection(run2, purge=True, unstore=True)
        self.assertCountEqual(set(butler.registry.queryDatasets(..., collections=...)), [ref1, ref2, ref3])
        existence = butler.datastore.mexists([ref1, ref2, ref3])
        self.assertTrue(existence[ref1])
        self.assertTrue(existence[ref2])
        self.assertTrue(existence[ref3])
        # Try to delete CHAINED and TAGGED collections with purge; should not
        # work.
        with self.assertRaises(TypeError):
            butler.pruneCollection(tag1, purge=True, unstore=True)
        with self.assertRaises(TypeError):
            butler.pruneCollection(chain1, purge=True, unstore=True)
        # Remove the tagged collection with unstore=False.  This should not
        # affect the datasets.
        butler.pruneCollection(tag1)
        with self.assertRaises(MissingCollectionError):
            butler.registry.getCollectionType(tag1)
        self.assertCountEqual(set(butler.registry.queryDatasets(..., collections=...)), [ref1, ref2, ref3])
        existence = butler.datastore.mexists([ref1, ref2, ref3])
        self.assertTrue(existence[ref1])
        self.assertTrue(existence[ref2])
        self.assertTrue(existence[ref3])
        # Add the tagged collection back in, and remove it with unstore=True.
        # This should remove ref3 only from the datastore.
        butler.registry.registerCollection(tag1, type=CollectionType.TAGGED)
        butler.registry.associate(tag1, [ref3])
        butler.pruneCollection(tag1, unstore=True)
        with self.assertRaises(MissingCollectionError):
            butler.registry.getCollectionType(tag1)
        self.assertCountEqual(set(butler.registry.queryDatasets(..., collections=...)), [ref1, ref2, ref3])
        existence = butler.datastore.mexists([ref1, ref2, ref3])
        self.assertTrue(existence[ref1])
        self.assertTrue(existence[ref2])
        self.assertFalse(existence[ref3])
        # Delete the chain with unstore=False.  The datasets should not be
        # affected at all.
        butler.pruneCollection(chain1)
        with self.assertRaises(MissingCollectionError):
            butler.registry.getCollectionType(chain1)
        self.assertCountEqual(set(butler.registry.queryDatasets(..., collections=...)), [ref1, ref2, ref3])
        existence = butler.datastore.mexists([ref1, ref2, ref3])
        self.assertTrue(existence[ref1])
        self.assertTrue(existence[ref2])
        self.assertFalse(existence[ref3])
        existence = butler.datastore.knows_these([ref1, ref2, ref3])
        self.assertTrue(existence[ref1])
        self.assertTrue(existence[ref2])
        self.assertFalse(existence[ref3])
        # Redefine and then delete the chain with unstore=True.  Only ref1
        # should be unstored (ref3 has already been unstored, but otherwise
        # would be now).
        butler.registry.registerCollection(chain1, type=CollectionType.CHAINED)
        butler.registry.setCollectionChain(chain1, [run1, run2])
        butler.pruneCollection(chain1, unstore=True)
        with self.assertRaises(MissingCollectionError):
            butler.registry.getCollectionType(chain1)
        self.assertCountEqual(set(butler.registry.queryDatasets(..., collections=...)), [ref1, ref2, ref3])
        existence = butler.datastore.mexists([ref1, ref2, ref3])
        self.assertFalse(existence[ref1])
        self.assertTrue(existence[ref2])
        self.assertFalse(existence[ref3])
        # Remove run1.  This removes ref1 and ref3 from the registry (they're
        # already gone from the datastore, which is fine).
        butler.pruneCollection(run1, purge=True, unstore=True)
        with self.assertRaises(MissingCollectionError):
            butler.registry.getCollectionType(run1)
        self.assertCountEqual(set(butler.registry.queryDatasets(..., collections=...)), [ref2])
        self.assertTrue(butler.datastore.exists(ref2))
        self.assertTrue(butler.datastore.knows(ref2))
        # Remove run2.  This removes ref2 from the registry and the datastore.
        butler.pruneCollection(run2, purge=True, unstore=True)
        with self.assertRaises(MissingCollectionError):
            butler.registry.getCollectionType(run2)
        self.assertCountEqual(set(butler.registry.queryDatasets(..., collections=...)), [])

        # Now that the collections have been pruned we can remove the
        # dataset type
        butler.registry.removeDatasetType(datasetType.name)

    def testPickle(self):
        """Test pickle support."""
        butler = Butler(self.tmpConfigFile, run=self.default_run)
        butlerOut = pickle.loads(pickle.dumps(butler))
        self.assertIsInstance(butlerOut, Butler)
        self.assertEqual(butlerOut._config, butler._config)
        self.assertEqual(butlerOut.collections, butler.collections)
        self.assertEqual(butlerOut.run, butler.run)

    def testGetDatasetTypes(self):
        butler = Butler(self.tmpConfigFile, run=self.default_run)
        dimensions = butler.registry.dimensions.extract(["instrument", "visit", "physical_filter"])
        dimensionEntries = [
            (
                "instrument",
                {"instrument": "DummyCam"},
                {"instrument": "DummyHSC"},
                {"instrument": "DummyCamComp"},
            ),
            ("physical_filter", {"instrument": "DummyCam", "name": "d-r", "band": "R"}),
            ("visit", {"instrument": "DummyCam", "id": 42, "name": "fortytwo", "physical_filter": "d-r"}),
        ]
        storageClass = self.storageClassFactory.getStorageClass("StructuredData")
        # Add needed Dimensions
        for args in dimensionEntries:
            butler.registry.insertDimensionData(*args)

        # When a DatasetType is added to the registry entries are not created
        # for components but querying them can return the components.
        datasetTypeNames = {"metric", "metric2", "metric4", "metric33", "pvi", "paramtest"}
        components = set()
        for datasetTypeName in datasetTypeNames:
            # Create and register a DatasetType
            self.addDatasetType(datasetTypeName, dimensions, storageClass, butler.registry)

            for componentName in storageClass.components:
                components.add(DatasetType.nameWithComponent(datasetTypeName, componentName))

        fromRegistry: set[DatasetType] = set()
        for parent_dataset_type in butler.registry.queryDatasetTypes():
            fromRegistry.add(parent_dataset_type)
            fromRegistry.update(parent_dataset_type.makeAllComponentDatasetTypes())
        self.assertEqual({d.name for d in fromRegistry}, datasetTypeNames | components)

        # Now that we have some dataset types registered, validate them
        butler.validateConfiguration(
            ignore=[
                "test_metric_comp",
                "metric3",
                "metric5",
                "calexp",
                "DummySC",
                "datasetType.component",
                "random_data",
                "random_data_2",
            ]
        )

        # Add a new datasetType that will fail template validation
        self.addDatasetType("test_metric_comp", dimensions, storageClass, butler.registry)
        if self.validationCanFail:
            with self.assertRaises(ValidationError):
                butler.validateConfiguration()

        # Rerun validation but with a subset of dataset type names
        butler.validateConfiguration(datasetTypeNames=["metric4"])

        # Rerun validation but ignore the bad datasetType
        butler.validateConfiguration(
            ignore=[
                "test_metric_comp",
                "metric3",
                "metric5",
                "calexp",
                "DummySC",
                "datasetType.component",
                "random_data",
                "random_data_2",
            ]
        )

    def testTransaction(self):
        butler = Butler(self.tmpConfigFile, run=self.default_run)
        datasetTypeName = "test_metric"
        dimensions = butler.registry.dimensions.extract(["instrument", "visit"])
        dimensionEntries = (
            ("instrument", {"instrument": "DummyCam"}),
            ("physical_filter", {"instrument": "DummyCam", "name": "d-r", "band": "R"}),
            ("visit", {"instrument": "DummyCam", "id": 42, "name": "fortytwo", "physical_filter": "d-r"}),
        )
        storageClass = self.storageClassFactory.getStorageClass("StructuredData")
        metric = makeExampleMetrics()
        dataId = {"instrument": "DummyCam", "visit": 42}
        # Create and register a DatasetType
        datasetType = self.addDatasetType(datasetTypeName, dimensions, storageClass, butler.registry)
        with self.assertRaises(TransactionTestError):
            with butler.transaction():
                # Add needed Dimensions
                for args in dimensionEntries:
                    butler.registry.insertDimensionData(*args)
                # Store a dataset
                ref = butler.put(metric, datasetTypeName, dataId)
                self.assertIsInstance(ref, DatasetRef)
                # Test getDirect
                metricOut = butler.getDirect(ref)
                self.assertEqual(metric, metricOut)
                # Test get
                metricOut = butler.get(datasetTypeName, dataId)
                self.assertEqual(metric, metricOut)
                # Check we can get components
                self.assertGetComponents(butler, ref, ("summary", "data", "output"), metric)
                raise TransactionTestError("This should roll back the entire transaction")
        with self.assertRaises(DataIdValueError, msg=f"Check can't expand DataId {dataId}"):
            butler.registry.expandDataId(dataId)
        # Should raise LookupError for missing data ID value
        with self.assertRaises(LookupError, msg=f"Check can't get by {datasetTypeName} and {dataId}"):
            butler.get(datasetTypeName, dataId)
        # Also check explicitly if Dataset entry is missing
        self.assertIsNone(butler.registry.findDataset(datasetType, dataId, collections=butler.collections))
        # Direct retrieval should not find the file in the Datastore
        with self.assertRaises(FileNotFoundError, msg=f"Check {ref} can't be retrieved directly"):
            butler.getDirect(ref)

    def testMakeRepo(self):
        """Test that we can write butler configuration to a new repository via
        the Butler.makeRepo interface and then instantiate a butler from the
        repo root.
        """
        # Do not run the test if we know this datastore configuration does
        # not support a file system root
        if self.fullConfigKey is None:
            return

        # create two separate directories
        root1 = tempfile.mkdtemp(dir=self.root)
        root2 = tempfile.mkdtemp(dir=self.root)

        butlerConfig = Butler.makeRepo(root1, config=Config(self.configFile))
        limited = Config(self.configFile)
        butler1 = Butler(butlerConfig)
        butlerConfig = Butler.makeRepo(root2, standalone=True, config=Config(self.configFile))
        full = Config(self.tmpConfigFile)
        butler2 = Butler(butlerConfig)
        # Butlers should have the same configuration regardless of whether
        # defaults were expanded.
        self.assertEqual(butler1._config, butler2._config)
        # Config files loaded directly should not be the same.
        self.assertNotEqual(limited, full)
        # Make sure "limited" doesn't have a few keys we know it should be
        # inheriting from defaults.
        self.assertIn(self.fullConfigKey, full)
        self.assertNotIn(self.fullConfigKey, limited)

        # Collections don't appear until something is put in them
        collections1 = set(butler1.registry.queryCollections())
        self.assertEqual(collections1, set())
        self.assertEqual(set(butler2.registry.queryCollections()), collections1)

        # Check that a config with no associated file name will not
        # work properly with relocatable Butler repo
        butlerConfig.configFile = None
        with self.assertRaises(ValueError):
            Butler(butlerConfig)

        with self.assertRaises(FileExistsError):
            Butler.makeRepo(self.root, standalone=True, config=Config(self.configFile), overwrite=False)

    def testStringification(self):
        butler = Butler(self.tmpConfigFile, run=self.default_run)
        butlerStr = str(butler)

        if self.datastoreStr is not None:
            for testStr in self.datastoreStr:
                self.assertIn(testStr, butlerStr)
        if self.registryStr is not None:
            self.assertIn(self.registryStr, butlerStr)

        datastoreName = butler.datastore.name
        if self.datastoreName is not None:
            for testStr in self.datastoreName:
                self.assertIn(testStr, datastoreName)

    def testButlerRewriteDataId(self):
        """Test that dataIds can be rewritten based on dimension records."""

        butler = Butler(self.tmpConfigFile, run=self.default_run)

        storageClass = self.storageClassFactory.getStorageClass("StructuredDataDict")
        datasetTypeName = "random_data"

        # Create dimension records.
        butler.registry.insertDimensionData("instrument", {"name": "DummyCamComp"})
        butler.registry.insertDimensionData(
            "physical_filter", {"instrument": "DummyCamComp", "name": "d-r", "band": "R"}
        )
        butler.registry.insertDimensionData(
            "detector", {"instrument": "DummyCamComp", "id": 1, "full_name": "det1"}
        )

        dimensions = butler.registry.dimensions.extract(["instrument", "exposure"])
        datasetType = DatasetType(datasetTypeName, dimensions, storageClass)
        butler.registry.registerDatasetType(datasetType)

        n_exposures = 5
        dayobs = 20210530

        for i in range(n_exposures):
            butler.registry.insertDimensionData(
                "exposure",
                {
                    "instrument": "DummyCamComp",
                    "id": i,
                    "obs_id": f"exp{i}",
                    "seq_num": i,
                    "day_obs": dayobs,
                    "physical_filter": "d-r",
                },
            )

        # Write some data.
        for i in range(n_exposures):
            metric = {"something": i, "other": "metric", "list": [2 * x for x in range(i)]}

            # Use the seq_num for the put to test rewriting.
            dataId = {"seq_num": i, "day_obs": dayobs, "instrument": "DummyCamComp", "physical_filter": "d-r"}
            ref = butler.put(metric, datasetTypeName, dataId=dataId)

            # Check that the exposure is correct in the dataId
            self.assertEqual(ref.dataId["exposure"], i)

            # and check that we can get the dataset back with the same dataId
            new_metric = butler.get(datasetTypeName, dataId=dataId)
            self.assertEqual(new_metric, metric)


class FileDatastoreButlerTests(ButlerTests):
    """Common tests and specialization of ButlerTests for butlers backed
    by datastores that inherit from FileDatastore.
    """

    def checkFileExists(self, root, relpath):
        """Checks if file exists at a given path (relative to root).

        Test testPutTemplates verifies actual physical existance of the files
        in the requested location.
        """
        uri = ResourcePath(root, forceDirectory=True)
        return uri.join(relpath).exists()

    def testPutTemplates(self):
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        butler = Butler(self.tmpConfigFile, run=self.default_run)

        # Add needed Dimensions
        butler.registry.insertDimensionData("instrument", {"name": "DummyCamComp"})
        butler.registry.insertDimensionData(
            "physical_filter", {"instrument": "DummyCamComp", "name": "d-r", "band": "R"}
        )
        butler.registry.insertDimensionData(
            "visit", {"instrument": "DummyCamComp", "id": 423, "name": "v423", "physical_filter": "d-r"}
        )
        butler.registry.insertDimensionData(
            "visit", {"instrument": "DummyCamComp", "id": 425, "name": "v425", "physical_filter": "d-r"}
        )

        # Create and store a dataset
        metric = makeExampleMetrics()

        # Create two almost-identical DatasetTypes (both will use default
        # template)
        dimensions = butler.registry.dimensions.extract(["instrument", "visit"])
        butler.registry.registerDatasetType(DatasetType("metric1", dimensions, storageClass))
        butler.registry.registerDatasetType(DatasetType("metric2", dimensions, storageClass))
        butler.registry.registerDatasetType(DatasetType("metric3", dimensions, storageClass))

        dataId1 = {"instrument": "DummyCamComp", "visit": 423}
        dataId2 = {"instrument": "DummyCamComp", "visit": 423, "physical_filter": "d-r"}

        # Put with exactly the data ID keys needed
        ref = butler.put(metric, "metric1", dataId1)
        uri = butler.getURI(ref)
        self.assertTrue(uri.exists())
        self.assertTrue(
            uri.unquoted_path.endswith(f"{self.default_run}/metric1/??#?/d-r/DummyCamComp_423.pickle")
        )

        # Check the template based on dimensions
        if hasattr(butler.datastore, "templates"):
            butler.datastore.templates.validateTemplates([ref])

        # Put with extra data ID keys (physical_filter is an optional
        # dependency); should not change template (at least the way we're
        # defining them  to behave now; the important thing is that they
        # must be consistent).
        ref = butler.put(metric, "metric2", dataId2)
        uri = butler.getURI(ref)
        self.assertTrue(uri.exists())
        self.assertTrue(
            uri.unquoted_path.endswith(f"{self.default_run}/metric2/d-r/DummyCamComp_v423.pickle")
        )

        # Check the template based on dimensions
        if hasattr(butler.datastore, "templates"):
            butler.datastore.templates.validateTemplates([ref])

        # Use a template that has a typo in dimension record metadata.
        # Easier to test with a butler that has a ref with records attached.
        template = FileTemplate("a/{visit.name}/{id}_{visit.namex:?}.fits")
        with self.assertLogs("lsst.daf.butler.core.fileTemplates", "INFO"):
            path = template.format(ref)
        self.assertEqual(path, f"a/v423/{ref.id}_fits")

        template = FileTemplate("a/{visit.name}/{id}_{visit.namex}.fits")
        with self.assertRaises(KeyError):
            with self.assertLogs("lsst.daf.butler.core.fileTemplates", "INFO"):
                template.format(ref)

        # Now use a file template that will not result in unique filenames
        with self.assertRaises(FileTemplateValidationError):
            butler.put(metric, "metric3", dataId1)

    def testImportExport(self):
        # Run put/get tests just to create and populate a repo.
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        self.runImportExportTest(storageClass)

    @unittest.expectedFailure
    def testImportExportVirtualComposite(self):
        # Run put/get tests just to create and populate a repo.
        storageClass = self.storageClassFactory.getStorageClass("StructuredComposite")
        self.runImportExportTest(storageClass)

    def runImportExportTest(self, storageClass):
        """This test does an export to a temp directory and an import back
        into a new temp directory repo. It does not assume a posix datastore"""
        exportButler = self.runPutGetTest(storageClass, "test_metric")
        # Test that the repo actually has at least one dataset.
        datasets = list(exportButler.registry.queryDatasets(..., collections=...))
        self.assertGreater(len(datasets), 0)
        # Add a DimensionRecord that's unused by those datasets.
        skymapRecord = {"name": "example_skymap", "hash": (50).to_bytes(8, byteorder="little")}
        exportButler.registry.insertDimensionData("skymap", skymapRecord)
        # Export and then import datasets.
        with safeTestTempDir(TESTDIR) as exportDir:
            exportFile = os.path.join(exportDir, "exports.yaml")
            with exportButler.export(filename=exportFile, directory=exportDir, transfer="auto") as export:
                export.saveDatasets(datasets)
                # Export the same datasets again. This should quietly do
                # nothing because of internal deduplication, and it shouldn't
                # complain about being asked to export the "htm7" elements even
                # though there aren't any in these datasets or in the database.
                export.saveDatasets(datasets, elements=["htm7"])
                # Save one of the data IDs again; this should be harmless
                # because of internal deduplication.
                export.saveDataIds([datasets[0].dataId])
                # Save some dimension records directly.
                export.saveDimensionData("skymap", [skymapRecord])
            self.assertTrue(os.path.exists(exportFile))
            with safeTestTempDir(TESTDIR) as importDir:
                # We always want this to be a local posix butler
                Butler.makeRepo(importDir, config=Config(os.path.join(TESTDIR, "config/basic/butler.yaml")))
                # Calling script.butlerImport tests the implementation of the
                # butler command line interface "import" subcommand. Functions
                # in the script folder are generally considered protected and
                # should not be used as public api.
                with open(exportFile, "r") as f:
                    script.butlerImport(
                        importDir,
                        export_file=f,
                        directory=exportDir,
                        transfer="auto",
                        skip_dimensions=None,
                        reuse_ids=False,
                    )
                importButler = Butler(importDir, run=self.default_run)
                for ref in datasets:
                    with self.subTest(ref=ref):
                        # Test for existence by passing in the DatasetType and
                        # data ID separately, to avoid lookup by dataset_id.
                        self.assertTrue(importButler.datasetExists(ref.datasetType, ref.dataId))
                self.assertEqual(
                    list(importButler.registry.queryDimensionRecords("skymap")),
                    [importButler.registry.dimensions["skymap"].RecordClass(**skymapRecord)],
                )

    def testRemoveRuns(self):
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        butler = Butler(self.tmpConfigFile, writeable=True)
        # Load registry data with dimensions to hang datasets off of.
        registryDataDir = os.path.normpath(os.path.join(os.path.dirname(__file__), "data", "registry"))
        butler.import_(filename=os.path.join(registryDataDir, "base.yaml"))
        # Add some RUN-type collection.
        run1 = "run1"
        butler.registry.registerRun(run1)
        run2 = "run2"
        butler.registry.registerRun(run2)
        # put a dataset in each
        metric = makeExampleMetrics()
        dimensions = butler.registry.dimensions.extract(["instrument", "physical_filter"])
        datasetType = self.addDatasetType(
            "prune_collections_test_dataset", dimensions, storageClass, butler.registry
        )
        ref1 = butler.put(metric, datasetType, {"instrument": "Cam1", "physical_filter": "Cam1-G"}, run=run1)
        ref2 = butler.put(metric, datasetType, {"instrument": "Cam1", "physical_filter": "Cam1-G"}, run=run2)
        uri1 = butler.getURI(ref1, collections=[run1])
        uri2 = butler.getURI(ref2, collections=[run2])
        # Remove from both runs with different values for unstore.
        butler.removeRuns([run1], unstore=True)
        butler.removeRuns([run2], unstore=False)
        # Should be nothing in registry for either one, and datastore should
        # not think either exists.
        with self.assertRaises(MissingCollectionError):
            butler.registry.getCollectionType(run1)
        with self.assertRaises(MissingCollectionError):
            butler.registry.getCollectionType(run2)
        self.assertFalse(butler.datastore.exists(ref1))
        self.assertFalse(butler.datastore.exists(ref2))
        # The ref we unstored should be gone according to the URI, but the
        # one we forgot should still be around.
        self.assertFalse(uri1.exists())
        self.assertTrue(uri2.exists())


class PosixDatastoreButlerTestCase(FileDatastoreButlerTests, unittest.TestCase):
    """PosixDatastore specialization of a butler"""

    configFile = os.path.join(TESTDIR, "config/basic/butler.yaml")
    fullConfigKey = ".datastore.formatters"
    validationCanFail = True
    datastoreStr = ["/tmp"]
    datastoreName = [f"FileDatastore@{BUTLER_ROOT_TAG}"]
    registryStr = "/gen3.sqlite3"

    def testPathConstructor(self):
        """Independent test of constructor using PathLike."""
        butler = Butler(self.tmpConfigFile, run=self.default_run)
        self.assertIsInstance(butler, Butler)

        # And again with a Path object with the butler yaml
        path = pathlib.Path(self.tmpConfigFile)
        butler = Butler(path, writeable=False)
        self.assertIsInstance(butler, Butler)

        # And again with a Path object without the butler yaml
        # (making sure we skip it if the tmp config doesn't end
        # in butler.yaml -- which is the case for a subclass)
        if self.tmpConfigFile.endswith("butler.yaml"):
            path = pathlib.Path(os.path.dirname(self.tmpConfigFile))
            butler = Butler(path, writeable=False)
            self.assertIsInstance(butler, Butler)

    def testExportTransferCopy(self):
        """Test local export using all transfer modes"""
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        exportButler = self.runPutGetTest(storageClass, "test_metric")
        # Test that the repo actually has at least one dataset.
        datasets = list(exportButler.registry.queryDatasets(..., collections=...))
        self.assertGreater(len(datasets), 0)
        uris = [exportButler.getURI(d) for d in datasets]
        datastoreRoot = exportButler.datastore.root

        pathsInStore = [uri.relative_to(datastoreRoot) for uri in uris]

        for path in pathsInStore:
            # Assume local file system
            self.assertTrue(self.checkFileExists(datastoreRoot, path), f"Checking path {path}")

        for transfer in ("copy", "link", "symlink", "relsymlink"):
            with safeTestTempDir(TESTDIR) as exportDir:
                with exportButler.export(directory=exportDir, format="yaml", transfer=transfer) as export:
                    export.saveDatasets(datasets)
                    for path in pathsInStore:
                        self.assertTrue(
                            self.checkFileExists(exportDir, path),
                            f"Check that mode {transfer} exported files",
                        )

    def testPruneDatasets(self):
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        butler = Butler(self.tmpConfigFile, writeable=True)
        # Load registry data with dimensions to hang datasets off of.
        registryDataDir = os.path.normpath(os.path.join(TESTDIR, "data", "registry"))
        butler.import_(filename=os.path.join(registryDataDir, "base.yaml"))
        # Add some RUN-type collections.
        run1 = "run1"
        butler.registry.registerRun(run1)
        run2 = "run2"
        butler.registry.registerRun(run2)
        # put some datasets.  ref1 and ref2 have the same data ID, and are in
        # different runs.  ref3 has a different data ID.
        metric = makeExampleMetrics()
        dimensions = butler.registry.dimensions.extract(["instrument", "physical_filter"])
        datasetType = self.addDatasetType(
            "prune_collections_test_dataset", dimensions, storageClass, butler.registry
        )
        ref1 = butler.put(metric, datasetType, {"instrument": "Cam1", "physical_filter": "Cam1-G"}, run=run1)
        ref2 = butler.put(metric, datasetType, {"instrument": "Cam1", "physical_filter": "Cam1-G"}, run=run2)
        ref3 = butler.put(metric, datasetType, {"instrument": "Cam1", "physical_filter": "Cam1-R1"}, run=run1)

        # Simple prune.
        butler.pruneDatasets([ref1, ref2, ref3], purge=True, unstore=True)
        with self.assertRaises(LookupError):
            butler.datasetExists(ref1.datasetType, ref1.dataId, collections=run1)

        # Put data back.
        ref1 = butler.put(metric, ref1.unresolved(), run=run1)
        ref2 = butler.put(metric, ref2.unresolved(), run=run2)
        ref3 = butler.put(metric, ref3.unresolved(), run=run1)

        # Check that in normal mode, deleting the record will lead to
        # trash not touching the file.
        uri1 = butler.datastore.getURI(ref1)
        butler.datastore.bridge.moveToTrash([ref1], transaction=None)  # Update the dataset_location table
        butler.datastore._table.delete(["dataset_id"], {"dataset_id": ref1.id})
        butler.datastore.trash(ref1)
        butler.datastore.emptyTrash()
        self.assertTrue(uri1.exists())
        uri1.remove()  # Clean it up.

        # Simulate execution butler setup by deleting the datastore
        # record but keeping the file around and trusting.
        butler.datastore.trustGetRequest = True
        uri2 = butler.datastore.getURI(ref2)
        uri3 = butler.datastore.getURI(ref3)
        self.assertTrue(uri2.exists())
        self.assertTrue(uri3.exists())

        # Remove the datastore record.
        butler.datastore.bridge.moveToTrash([ref2], transaction=None)  # Update the dataset_location table
        butler.datastore._table.delete(["dataset_id"], {"dataset_id": ref2.id})
        self.assertTrue(uri2.exists())
        butler.datastore.trash([ref2, ref3])
        # Immediate removal for ref2 file
        self.assertFalse(uri2.exists())
        # But ref3 has to wait for the empty.
        self.assertTrue(uri3.exists())
        butler.datastore.emptyTrash()
        self.assertFalse(uri3.exists())

        # Clear out the datasets from registry.
        butler.pruneDatasets([ref1, ref2, ref3], purge=True, unstore=True)

    def testPytypeCoercion(self):
        """Test python type coercion on Butler.get and put."""

        # Store some data with the normal example storage class.
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        datasetTypeName = "test_metric"
        butler = self.runPutGetTest(storageClass, datasetTypeName)

        dataId = {"instrument": "DummyCamComp", "visit": 423}
        metric = butler.get(datasetTypeName, dataId=dataId)
        self.assertEqual(get_full_type_name(metric), "lsst.daf.butler.tests.MetricsExample")

        datasetType_ori = butler.registry.getDatasetType(datasetTypeName)
        self.assertEqual(datasetType_ori.storageClass.name, "StructuredDataNoComponents")

        # Now need to hack the registry dataset type definition.
        # There is no API for this.
        manager = butler.registry._managers.datasets
        manager._db.update(
            manager._static.dataset_type,
            {"name": datasetTypeName},
            {datasetTypeName: datasetTypeName, "storage_class": "StructuredDataNoComponentsModel"},
        )

        # Force reset of dataset type cache
        butler.registry.refresh()

        datasetType_new = butler.registry.getDatasetType(datasetTypeName)
        self.assertEqual(datasetType_new.name, datasetType_ori.name)
        self.assertEqual(datasetType_new.storageClass.name, "StructuredDataNoComponentsModel")

        metric_model = butler.get(datasetTypeName, dataId=dataId)
        self.assertNotEqual(type(metric_model), type(metric))
        self.assertEqual(get_full_type_name(metric_model), "lsst.daf.butler.tests.MetricsExampleModel")

        # Put the model and read it back to show that everything now
        # works as normal.
        metric_ref = butler.put(metric_model, datasetTypeName, dataId=dataId, visit=424)
        metric_model_new = butler.get(metric_ref)
        self.assertEqual(metric_model_new, metric_model)

        # Hack the storage class again to something that will fail on the
        # get with no conversion class.
        manager._db.update(
            manager._static.dataset_type,
            {"name": datasetTypeName},
            {datasetTypeName: datasetTypeName, "storage_class": "StructuredDataListYaml"},
        )
        butler.registry.refresh()

        with self.assertRaises(ValueError):
            butler.get(datasetTypeName, dataId=dataId)


@unittest.skipUnless(testing is not None, "testing.postgresql module not found")
class PostgresPosixDatastoreButlerTestCase(FileDatastoreButlerTests, unittest.TestCase):
    """PosixDatastore specialization of a butler using Postgres"""

    configFile = os.path.join(TESTDIR, "config/basic/butler.yaml")
    fullConfigKey = ".datastore.formatters"
    validationCanFail = True
    datastoreStr = ["/tmp"]
    datastoreName = [f"FileDatastore@{BUTLER_ROOT_TAG}"]
    registryStr = "PostgreSQL@test"

    @staticmethod
    def _handler(postgresql):
        engine = sqlalchemy.engine.create_engine(postgresql.url())
        with engine.begin() as connection:
            connection.execute(sqlalchemy.text("CREATE EXTENSION btree_gist;"))

    @classmethod
    def setUpClass(cls):
        # Create the postgres test server.
        cls.postgresql = testing.postgresql.PostgresqlFactory(
            cache_initialized_db=True, on_initialized=cls._handler
        )
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        # Clean up any lingering SQLAlchemy engines/connections
        # so they're closed before we shut down the server.
        gc.collect()
        cls.postgresql.clear_cache()
        super().tearDownClass()

    def setUp(self):
        self.server = self.postgresql()

        # Need to add a registry section to the config.
        self._temp_config = False
        config = Config(self.configFile)
        config["registry", "db"] = self.server.url()
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as fh:
            config.dump(fh)
            self.configFile = fh.name
            self._temp_config = True
        super().setUp()

    def tearDown(self):
        self.server.stop()
        if self._temp_config and os.path.exists(self.configFile):
            os.remove(self.configFile)
        super().tearDown()

    def testMakeRepo(self):
        # The base class test assumes that it's using sqlite and assumes
        # the config file is acceptable to sqlite.
        raise unittest.SkipTest("Postgres config is not compatible with this test.")


class InMemoryDatastoreButlerTestCase(ButlerTests, unittest.TestCase):
    """InMemoryDatastore specialization of a butler"""

    configFile = os.path.join(TESTDIR, "config/basic/butler-inmemory.yaml")
    fullConfigKey = None
    useTempRoot = False
    validationCanFail = False
    datastoreStr = ["datastore='InMemory"]
    datastoreName = ["InMemoryDatastore@"]
    registryStr = "/gen3.sqlite3"

    def testIngest(self):
        pass


class ChainedDatastoreButlerTestCase(FileDatastoreButlerTests, unittest.TestCase):
    """PosixDatastore specialization"""

    configFile = os.path.join(TESTDIR, "config/basic/butler-chained.yaml")
    fullConfigKey = ".datastore.datastores.1.formatters"
    validationCanFail = True
    datastoreStr = ["datastore='InMemory", "/FileDatastore_1/,", "/FileDatastore_2/'"]
    datastoreName = [
        "InMemoryDatastore@",
        f"FileDatastore@{BUTLER_ROOT_TAG}/FileDatastore_1",
        "SecondDatastore",
    ]
    registryStr = "/gen3.sqlite3"


class ButlerExplicitRootTestCase(PosixDatastoreButlerTestCase):
    """Test that a yaml file in one location can refer to a root in another."""

    datastoreStr = ["dir1"]
    # Disable the makeRepo test since we are deliberately not using
    # butler.yaml as the config name.
    fullConfigKey = None

    def setUp(self):
        self.root = makeTestTempDir(TESTDIR)

        # Make a new repository in one place
        self.dir1 = os.path.join(self.root, "dir1")
        Butler.makeRepo(self.dir1, config=Config(self.configFile))

        # Move the yaml file to a different place and add a "root"
        self.dir2 = os.path.join(self.root, "dir2")
        os.makedirs(self.dir2, exist_ok=True)
        configFile1 = os.path.join(self.dir1, "butler.yaml")
        config = Config(configFile1)
        config["root"] = self.dir1
        configFile2 = os.path.join(self.dir2, "butler2.yaml")
        config.dumpToUri(configFile2)
        os.remove(configFile1)
        self.tmpConfigFile = configFile2

    def testFileLocations(self):
        self.assertNotEqual(self.dir1, self.dir2)
        self.assertTrue(os.path.exists(os.path.join(self.dir2, "butler2.yaml")))
        self.assertFalse(os.path.exists(os.path.join(self.dir1, "butler.yaml")))
        self.assertTrue(os.path.exists(os.path.join(self.dir1, "gen3.sqlite3")))


class ButlerMakeRepoOutfileTestCase(ButlerPutGetTests, unittest.TestCase):
    """Test that a config file created by makeRepo outside of repo works."""

    configFile = os.path.join(TESTDIR, "config/basic/butler.yaml")

    def setUp(self):
        self.root = makeTestTempDir(TESTDIR)
        self.root2 = makeTestTempDir(TESTDIR)

        self.tmpConfigFile = os.path.join(self.root2, "different.yaml")
        Butler.makeRepo(self.root, config=Config(self.configFile), outfile=self.tmpConfigFile)

    def tearDown(self):
        if os.path.exists(self.root2):
            shutil.rmtree(self.root2, ignore_errors=True)
        super().tearDown()

    def testConfigExistence(self):
        c = Config(self.tmpConfigFile)
        uri_config = ResourcePath(c["root"])
        uri_expected = ResourcePath(self.root, forceDirectory=True)
        self.assertEqual(uri_config.geturl(), uri_expected.geturl())
        self.assertNotIn(":", uri_config.path, "Check for URI concatenated with normal path")

    def testPutGet(self):
        storageClass = self.storageClassFactory.getStorageClass("StructuredDataNoComponents")
        self.runPutGetTest(storageClass, "test_metric")


class ButlerMakeRepoOutfileDirTestCase(ButlerMakeRepoOutfileTestCase):
    """Test that a config file created by makeRepo outside of repo works."""

    configFile = os.path.join(TESTDIR, "config/basic/butler.yaml")

    def setUp(self):
        self.root = makeTestTempDir(TESTDIR)
        self.root2 = makeTestTempDir(TESTDIR)

        self.tmpConfigFile = self.root2
        Butler.makeRepo(self.root, config=Config(self.configFile), outfile=self.tmpConfigFile)

    def testConfigExistence(self):
        # Append the yaml file else Config constructor does not know the file
        # type.
        self.tmpConfigFile = os.path.join(self.tmpConfigFile, "butler.yaml")
        super().testConfigExistence()


class ButlerMakeRepoOutfileUriTestCase(ButlerMakeRepoOutfileTestCase):
    """Test that a config file created by makeRepo outside of repo works."""

    configFile = os.path.join(TESTDIR, "config/basic/butler.yaml")

    def setUp(self):
        self.root = makeTestTempDir(TESTDIR)
        self.root2 = makeTestTempDir(TESTDIR)

        self.tmpConfigFile = ResourcePath(os.path.join(self.root2, "something.yaml")).geturl()
        Butler.makeRepo(self.root, config=Config(self.configFile), outfile=self.tmpConfigFile)


@unittest.skipIf(not boto3, "Warning: boto3 AWS SDK not found!")
class S3DatastoreButlerTestCase(FileDatastoreButlerTests, unittest.TestCase):
    """S3Datastore specialization of a butler; an S3 storage Datastore +
    a local in-memory SqlRegistry.
    """

    configFile = os.path.join(TESTDIR, "config/basic/butler-s3store.yaml")
    fullConfigKey = None
    validationCanFail = True

    bucketName = "anybucketname"
    """Name of the Bucket that will be used in the tests. The name is read from
    the config file used with the tests during set-up.
    """

    root = "butlerRoot/"
    """Root repository directory expected to be used in case useTempRoot=False.
    Otherwise the root is set to a 20 characters long randomly generated string
    during set-up.
    """

    datastoreStr = [f"datastore={root}"]
    """Contains all expected root locations in a format expected to be
    returned by Butler stringification.
    """

    datastoreName = ["FileDatastore@s3://{bucketName}/{root}"]
    """The expected format of the S3 Datastore string."""

    registryStr = "/gen3.sqlite3"
    """Expected format of the Registry string."""

    mock_s3 = mock_s3()
    """The mocked s3 interface from moto."""

    def genRoot(self):
        """Returns a random string of len 20 to serve as a root
        name for the temporary bucket repo.

        This is equivalent to tempfile.mkdtemp as this is what self.root
        becomes when useTempRoot is True.
        """
        rndstr = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        return rndstr + "/"

    def setUp(self):
        config = Config(self.configFile)
        uri = ResourcePath(config[".datastore.datastore.root"])
        self.bucketName = uri.netloc

        # Enable S3 mocking of tests.
        self.mock_s3.start()

        # set up some fake credentials if they do not exist
        self.usingDummyCredentials = setAwsEnvCredentials()

        if self.useTempRoot:
            self.root = self.genRoot()
        rooturi = f"s3://{self.bucketName}/{self.root}"
        config.update({"datastore": {"datastore": {"root": rooturi}}})

        # need local folder to store registry database
        self.reg_dir = makeTestTempDir(TESTDIR)
        config["registry", "db"] = f"sqlite:///{self.reg_dir}/gen3.sqlite3"

        # MOTO needs to know that we expect Bucket bucketname to exist
        # (this used to be the class attribute bucketName)
        s3 = boto3.resource("s3")
        s3.create_bucket(Bucket=self.bucketName)

        self.datastoreStr = f"datastore={self.root}"
        self.datastoreName = [f"FileDatastore@{rooturi}"]
        Butler.makeRepo(rooturi, config=config, forceConfigRoot=False)
        self.tmpConfigFile = posixpath.join(rooturi, "butler.yaml")

    def tearDown(self):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(self.bucketName)
        try:
            bucket.objects.all().delete()
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                # the key was not reachable - pass
                pass
            else:
                raise

        bucket = s3.Bucket(self.bucketName)
        bucket.delete()

        # Stop the S3 mock.
        self.mock_s3.stop()

        # unset any potentially set dummy credentials
        if self.usingDummyCredentials:
            unsetAwsEnvCredentials()

        if self.reg_dir is not None and os.path.exists(self.reg_dir):
            shutil.rmtree(self.reg_dir, ignore_errors=True)

        if self.useTempRoot and os.path.exists(self.root):
            shutil.rmtree(self.root, ignore_errors=True)

        super().tearDown()


@unittest.skipIf(WsgiDAVApp is None, "Warning: wsgidav/cheroot not found!")
class WebdavDatastoreButlerTestCase(FileDatastoreButlerTests, unittest.TestCase):
    """WebdavDatastore specialization of a butler; a Webdav storage Datastore +
    a local in-memory SqlRegistry.
    """

    configFile = os.path.join(TESTDIR, "config/basic/butler-webdavstore.yaml")
    fullConfigKey = None
    validationCanFail = True

    serverName = "localhost"
    """Name of the server that will be used in the tests.
    """

    portNumber = 8080
    """Port on which the webdav server listens. Automatically chosen
    at setUpClass via the _getfreeport() method
    """

    root = "butlerRoot/"
    """Root repository directory expected to be used in case useTempRoot=False.
    Otherwise the root is set to a 20 characters long randomly generated string
    during set-up.
    """

    datastoreStr = [f"datastore={root}"]
    """Contains all expected root locations in a format expected to be
    returned by Butler stringification.
    """

    datastoreName = ["FileDatastore@https://{serverName}/{root}"]
    """The expected format of the WebdavDatastore string."""

    registryStr = "/gen3.sqlite3"
    """Expected format of the Registry string."""

    serverThread = None
    """Thread in which the local webdav server will run"""

    stopWebdavServer = False
    """This flag will cause the webdav server to
    gracefully shut down when True
    """

    def genRoot(self):
        """Returns a random string of len 20 to serve as a root
        name for the temporary bucket repo.

        This is equivalent to tempfile.mkdtemp as this is what self.root
        becomes when useTempRoot is True.
        """
        rndstr = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        return rndstr + "/"

    @classmethod
    def setUpClass(cls):
        # Do the same as inherited class
        cls.storageClassFactory = StorageClassFactory()
        cls.storageClassFactory.addFromConfig(cls.configFile)

        cls.portNumber = cls._getfreeport()
        # Run a local webdav server on which tests will be run
        cls.serverThread = Thread(
            target=cls._serveWebdav, args=(cls, cls.portNumber, lambda: cls.stopWebdavServer), daemon=True
        )
        cls.serverThread.start()
        # Wait for it to start
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        # Ask for graceful shut down of the webdav server
        cls.stopWebdavServer = True
        # Wait for the thread to exit
        cls.serverThread.join()
        super().tearDownClass()

    def setUp(self):
        config = Config(self.configFile)

        if self.useTempRoot:
            self.root = self.genRoot()
        self.rooturi = f"http://{self.serverName}:{self.portNumber}/{self.root}"
        config.update({"datastore": {"datastore": {"root": self.rooturi}}})

        # need local folder to store registry database
        self.reg_dir = makeTestTempDir(TESTDIR)
        config["registry", "db"] = f"sqlite:///{self.reg_dir}/gen3.sqlite3"

        self.datastoreStr = f"datastore={self.root}"
        self.datastoreName = [f"FileDatastore@{self.rooturi}"]

        if not _is_webdav_endpoint(self.rooturi):
            raise OSError("Webdav server not running properly: cannot run tests.")

        Butler.makeRepo(self.rooturi, config=config, forceConfigRoot=False)
        self.tmpConfigFile = posixpath.join(self.rooturi, "butler.yaml")

    def tearDown(self):
        # Clear temporary directory
        ResourcePath(self.rooturi).remove()
        ResourcePath(self.rooturi).session.close()

        if self.reg_dir is not None and os.path.exists(self.reg_dir):
            shutil.rmtree(self.reg_dir, ignore_errors=True)

        if self.useTempRoot and os.path.exists(self.root):
            shutil.rmtree(self.root, ignore_errors=True)

        super().tearDown()

    def _serveWebdav(self, port: int, stopWebdavServer):
        """Starts a local webdav-compatible HTTP server,
        Listening on http://localhost:port
        This server only runs when this test class is instantiated,
        and then shuts down. Must be started is a separate thread.

        Parameters
        ----------
        port : `int`
           The port number on which the server should listen
        """
        root_path = gettempdir()

        config = {
            "host": "0.0.0.0",
            "port": port,
            "provider_mapping": {"/": root_path},
            "http_authenticator": {"domain_controller": None},
            "simple_dc": {"user_mapping": {"*": True}},
            "verbose": 0,
        }
        app = WsgiDAVApp(config)

        server_args = {
            "bind_addr": (config["host"], config["port"]),
            "wsgi_app": app,
        }
        server = wsgi.Server(**server_args)
        server.prepare()

        try:
            # Start the actual server in a separate thread
            t = Thread(target=server.serve, daemon=True)
            t.start()
            # watch stopWebdavServer, and gracefully
            # shut down the server when True
            while True:
                if stopWebdavServer():
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print("Caught Ctrl-C, shutting down...")
        finally:
            server.stop()
            t.join()

    def _getfreeport():
        """
        Determines a free port using sockets.
        """
        free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        free_socket.bind(("127.0.0.1", 0))
        free_socket.listen()
        port = free_socket.getsockname()[1]
        free_socket.close()
        return port


class PosixDatastoreTransfers(unittest.TestCase):
    """Test data transfers between butlers.

    Test for different managers. UUID to UUID and integer to integer are
    tested. UUID to integer is not supported since we do not currently
    want to allow that.  Integer to UUID is supported with the caveat
    that UUID4 will be generated and this will be incorrect for raw
    dataset types. The test ignores that.
    """

    configFile = os.path.join(TESTDIR, "config/basic/butler.yaml")

    @classmethod
    def setUpClass(cls):
        cls.storageClassFactory = StorageClassFactory()
        cls.storageClassFactory.addFromConfig(cls.configFile)

    def setUp(self):
        self.root = makeTestTempDir(TESTDIR)
        self.config = Config(self.configFile)

    def tearDown(self):
        removeTestTempDir(self.root)

    def create_butler(self, manager, label):
        config = Config(self.configFile)
        config["registry", "managers", "datasets"] = manager
        return Butler(Butler.makeRepo(f"{self.root}/butler{label}", config=config), writeable=True)

    def create_butlers(self, manager1, manager2):
        self.source_butler = self.create_butler(manager1, "1")
        self.target_butler = self.create_butler(manager2, "2")

    def testTransferUuidToUuid(self):
        self.create_butlers(
            "lsst.daf.butler.registry.datasets.byDimensions.ByDimensionsDatasetRecordStorageManagerUUID",
            "lsst.daf.butler.registry.datasets.byDimensions.ByDimensionsDatasetRecordStorageManagerUUID",
        )
        # Setting id_gen_map should have no effect here
        self.assertButlerTransfers(id_gen_map={"random_data_2": DatasetIdGenEnum.DATAID_TYPE})

    def testTransferMissing(self):
        """Test transfers where datastore records are missing.

        This is how execution butler works.
        """
        self.create_butlers(
            "lsst.daf.butler.registry.datasets.byDimensions.ByDimensionsDatasetRecordStorageManagerUUID",
            "lsst.daf.butler.registry.datasets.byDimensions.ByDimensionsDatasetRecordStorageManagerUUID",
        )

        # Configure the source butler to allow trust.
        self.source_butler.datastore.trustGetRequest = True

        self.assertButlerTransfers(purge=True)

    def testTransferMissingDisassembly(self):
        """Test transfers where datastore records are missing.

        This is how execution butler works.
        """
        self.create_butlers(
            "lsst.daf.butler.registry.datasets.byDimensions.ByDimensionsDatasetRecordStorageManagerUUID",
            "lsst.daf.butler.registry.datasets.byDimensions.ByDimensionsDatasetRecordStorageManagerUUID",
        )

        # Configure the source butler to allow trust.
        self.source_butler.datastore.trustGetRequest = True

        # Test disassembly.
        self.assertButlerTransfers(purge=True, storageClassName="StructuredComposite")

    def assertButlerTransfers(self, id_gen_map=None, purge=False, storageClassName="StructuredData"):
        """Test that a run can be transferred to another butler."""

        storageClass = self.storageClassFactory.getStorageClass(storageClassName)
        datasetTypeName = "random_data"

        # Test will create 3 collections and we will want to transfer
        # two of those three.
        runs = ["run1", "run2", "other"]

        # Also want to use two different dataset types to ensure that
        # grouping works.
        datasetTypeNames = ["random_data", "random_data_2"]

        # Create the run collections in the source butler.
        for run in runs:
            self.source_butler.registry.registerCollection(run, CollectionType.RUN)

        # Create dimensions in source butler.
        n_exposures = 30
        self.source_butler.registry.insertDimensionData("instrument", {"name": "DummyCamComp"})
        self.source_butler.registry.insertDimensionData(
            "physical_filter", {"instrument": "DummyCamComp", "name": "d-r", "band": "R"}
        )
        self.source_butler.registry.insertDimensionData(
            "detector", {"instrument": "DummyCamComp", "id": 1, "full_name": "det1"}
        )

        for i in range(n_exposures):
            self.source_butler.registry.insertDimensionData(
                "exposure",
                {"instrument": "DummyCamComp", "id": i, "obs_id": f"exp{i}", "physical_filter": "d-r"},
            )

        # Create dataset types in the source butler.
        dimensions = self.source_butler.registry.dimensions.extract(["instrument", "exposure"])
        for datasetTypeName in datasetTypeNames:
            datasetType = DatasetType(datasetTypeName, dimensions, storageClass)
            self.source_butler.registry.registerDatasetType(datasetType)

        # Write a dataset to an unrelated run -- this will ensure that
        # we are rewriting integer dataset ids in the target if necessary.
        # Will not be relevant for UUID.
        run = "distraction"
        butler = Butler(butler=self.source_butler, run=run)
        butler.put(
            makeExampleMetrics(),
            datasetTypeName,
            exposure=1,
            instrument="DummyCamComp",
            physical_filter="d-r",
        )

        # Write some example metrics to the source
        butler = Butler(butler=self.source_butler)

        # Set of DatasetRefs that should be in the list of refs to transfer
        # but which will not be transferred.
        deleted = set()

        n_expected = 20  # Number of datasets expected to be transferred
        source_refs = []
        for i in range(n_exposures):
            # Put a third of datasets into each collection, only retain
            # two thirds.
            index = i % 3
            run = runs[index]
            datasetTypeName = datasetTypeNames[i % 2]

            metric_data = {
                "summary": {"counter": i},
                "output": {"text": "metric"},
                "data": [2 * x for x in range(i)],
            }
            metric = MetricsExample(**metric_data)
            dataId = {"exposure": i, "instrument": "DummyCamComp", "physical_filter": "d-r"}
            ref = butler.put(metric, datasetTypeName, dataId=dataId, run=run)

            # Remove the datastore record using low-level API
            if purge:
                # Remove records for a fraction.
                if index == 1:
                    # For one of these delete the file as well.
                    # This allows the "missing" code to filter the
                    # file out.
                    if not deleted:
                        primary, uris = butler.datastore.getURIs(ref)
                        if primary:
                            primary.remove()
                        for uri in uris.values():
                            uri.remove()
                        n_expected -= 1
                        deleted.add(ref)

                    # Remove the datastore record.
                    butler.datastore._table.delete(["dataset_id"], {"dataset_id": ref.id})

            if index < 2:
                source_refs.append(ref)
            if ref not in deleted:
                new_metric = butler.get(ref.unresolved(), collections=run)
                self.assertEqual(new_metric, metric)

        # Create some bad dataset types to ensure we check for inconsistent
        # definitions.
        badStorageClass = self.storageClassFactory.getStorageClass("StructuredDataList")
        for datasetTypeName in datasetTypeNames:
            datasetType = DatasetType(datasetTypeName, dimensions, badStorageClass)
            self.target_butler.registry.registerDatasetType(datasetType)
        with self.assertRaises(ConflictingDefinitionError) as cm:
            self.target_butler.transfer_from(self.source_butler, source_refs, id_gen_map=id_gen_map)
        self.assertIn("dataset type differs", str(cm.exception))

        # And remove the bad definitions.
        for datasetTypeName in datasetTypeNames:
            self.target_butler.registry.removeDatasetType(datasetTypeName)

        # Transfer without creating dataset types should fail.
        with self.assertRaises(KeyError):
            self.target_butler.transfer_from(self.source_butler, source_refs, id_gen_map=id_gen_map)

        # Transfer without creating dimensions should fail.
        with self.assertRaises(ConflictingDefinitionError) as cm:
            self.target_butler.transfer_from(
                self.source_butler, source_refs, id_gen_map=id_gen_map, register_dataset_types=True
            )
        self.assertIn("dimension", str(cm.exception))

        # The failed transfer above leaves registry in an inconsistent
        # state because the run is created but then rolled back without
        # the collection cache being cleared. For now force a refresh.
        # Can remove with DM-35498.
        self.target_butler.registry.refresh()

        # Now transfer them to the second butler, including dimensions.
        with self.assertLogs(level=logging.DEBUG) as cm:
            transferred = self.target_butler.transfer_from(
                self.source_butler,
                source_refs,
                id_gen_map=id_gen_map,
                register_dataset_types=True,
                transfer_dimensions=True,
            )
        self.assertEqual(len(transferred), n_expected)
        log_output = ";".join(cm.output)
        self.assertIn("found in datastore for chunk", log_output)
        self.assertIn("Creating output run", log_output)

        # Do the transfer twice to ensure that it will do nothing extra.
        # Only do this if purge=True because it does not work for int
        # dataset_id.
        if purge:
            # This should not need to register dataset types.
            transferred = self.target_butler.transfer_from(
                self.source_butler, source_refs, id_gen_map=id_gen_map
            )
            self.assertEqual(len(transferred), n_expected)

            # Also do an explicit low-level transfer to trigger some
            # edge cases.
            with self.assertLogs(level=logging.DEBUG) as cm:
                self.target_butler.datastore.transfer_from(self.source_butler.datastore, source_refs)
            log_output = ";".join(cm.output)
            self.assertIn("no file artifacts exist", log_output)

            with self.assertRaises(TypeError):
                self.target_butler.datastore.transfer_from(self.source_butler, source_refs)

            with self.assertRaises(ValueError):
                self.target_butler.datastore.transfer_from(
                    self.source_butler.datastore, source_refs, transfer="split"
                )

        # Now try to get the same refs from the new butler.
        for ref in source_refs:
            if ref not in deleted:
                unresolved_ref = ref.unresolved()
                new_metric = self.target_butler.get(unresolved_ref, collections=ref.run)
                old_metric = self.source_butler.get(unresolved_ref, collections=ref.run)
                self.assertEqual(new_metric, old_metric)

        # Now prune run2 collection and create instead a CHAINED collection.
        # This should block the transfer.
        self.target_butler.pruneCollection("run2", purge=True, unstore=True)
        self.target_butler.registry.registerCollection("run2", CollectionType.CHAINED)
        with self.assertRaises(CollectionTypeError):
            # Re-importing the run1 datasets can be problematic if they
            # use integer IDs so filter those out.
            to_transfer = [ref for ref in source_refs if ref.run == "run2"]
            self.target_butler.transfer_from(self.source_butler, to_transfer, id_gen_map=id_gen_map)


if __name__ == "__main__":
    unittest.main()
