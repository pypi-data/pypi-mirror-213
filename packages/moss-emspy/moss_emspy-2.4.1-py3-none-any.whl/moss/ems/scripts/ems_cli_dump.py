#
# The MIT License (MIT)
# Copyright (c) 2022 M.O.S.S. Computer Grafik Systeme GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT,TORT OR OTHERWISE, ARISING FROM, OUT
# OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import copy
import json
import logging
from pathlib import Path
from typing import List, Optional

from moss.ems.emslayer import EmsLayer
from moss.ems.emsproject import EmsProject
from moss.ems.emsservice import EmsServiceException, Service

logger = logging.getLogger(__name__)


try:
    from osgeo import gdal
except ImportError:
    logger.error("This function needs GDAL Python bindings.")


class EmsCliDumpException(Exception):
    pass


class EmsCliDump:
    """ """

    def __init__(
        self,
        url: str,
        project: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ):

        if username and password:
            logger.debug("Logging in using username and password.")
            try:
                self.service = Service(url, username=username, password=password)
            except EmsServiceException:
                logger.error("Can not connect to service using username and password.")
                raise EmsCliDumpException
        elif token:
            logger.debug("Logging in using token.")
            try:
                self.service = Service(url, token=token)
            except EmsServiceException:
                logger.error("Can not connect to service using token.")
                raise EmsCliDumpException
        else:
            logger.debug("Using service without authentication.")
            try:
                self.service = Service(url)
            except EmsServiceException:
                logger.error("Can not access WEGA-EMS Service using no authentication.")

        logger.debug("Accessing project %s", project)
        try:
            selected_project = self.service.project(project)
            if selected_project is not None:
                self.project: EmsProject = selected_project
            else:
                logger.error("The selected project %s is not defined", project)
                raise EmsCliDumpException
        except EmsServiceException:
            logger.error("The project %s does not exists in %s", project, url)
            raise EmsCliDumpException

    def _project_has_variant(self):
        """
        Check if project has variants
        """
        return self.project.variants_tree()  # Empty dict are False

    def _save_layer_as_json(
        self,
        layer: EmsLayer,
        output_json_path: Path,
        query="1=1",
        variant: Optional[str] = None,
    ):
        """
        Save the layer as json.
        """

        logger.debug("Writing layer %s in %s", layer, output_json_path)
        query_params = {query: query, "returnGeometry": True}

        if variant:
            query_params["variants"] = [int(variant)]

        layer_query = layer.query(**query_params)
        logger.info("Queried %s features from %s", len(layer_query), layer)

        if layer_query:
            query_output = layer_query.resolve(with_catalog=True)

            total_features = []
            final_esri = {}

            for query_index, query_item in enumerate(query_output):
                if query_index == 0:
                    final_esri = copy.deepcopy(query_item)

                features = query_item.get("features")
                if features is not None:
                    total_features.extend(features)

            cleaned_features = list(
                filter(lambda item: "geometry" in item, total_features)
            )

            if cleaned_features:
                final_esri["features"] = cleaned_features
                final_esri["counts"] = len(cleaned_features)

                with open(output_json_path, "w+") as esri_json:
                    esri_json.write(json.dumps(final_esri))

        return output_json_path

    def _generate_output_file_name(self, output_path, objectclass, layer):
        """
        Full path to output json.
        """

        file_name = f"{objectclass}_{layer}.json"
        return output_path / file_name

    def ems_dump(
        self,
        output_path: str,
        objectclasses: Optional[str] = None,
        variants: Optional[str] = None,
        extension: str = "gpkg",
        output_filename: str = "export_ems",
        export_layers: List[str] = None,
    ):
        logger.info("Starting dump..")
        logger.debug("Checking if output %s exists", output_path)

        if not Path(output_path).exists():
            raise EmsCliDumpException("The output path %s not exists.", output_path)
        else:
            output_path = Path(output_path)

        export_objectclasses = []
        if objectclasses is not None:
            export_objectclasses = objectclasses.split(",")
            logger.info("Exporting only the provided objectclasses %s", objectclasses)
        else:
            export_objectclasses = self.project.objectclasses
            logger.info("Exporting ALL the objectclasses from project.")

        if variants is None and self._project_has_variant():
            raise EmsCliDumpException("Project has variant and no variant are provided")

        if variants is not None:
            for variant in variants.split(","):

                variant_output_path: Path = output_path / variant
                variant_output_path.mkdir(exist_ok=True)

                logger.info("Creating variant directory in %s", variant_output_path)

                for objectclass in export_objectclasses:
                    logger.info("Processing objectclass %s", objectclass)

                    if isinstance(objectclass, str):
                        objectclass = self.project.objectclass(objectclass)

                    if export_layers is None:
                        layers: Optional[List[EmsLayer]] = objectclass.layers
                    else:
                        layers = [
                            layer
                            for layer in objectclass.layers
                            if str(layer) in export_layers
                        ]
                    if layers is not None:
                        for layer in layers:
                            output_file_path = self._generate_output_file_name(
                                variant_output_path, objectclass, layer
                            )
                            self._save_layer_as_json(
                                layer, output_file_path, variant=variant
                            )

                logger.info("Generate GDAL file")
                output_gdal_file = (
                    variant_output_path / f"{output_filename}.{extension}"
                )
                for json_file in variant_output_path.glob("*.json"):

                    if extension in ["shp", "csv"]:
                        output_gdal_file = (
                            variant_output_path / f"{json_file.stem}.{extension}"
                        )

                    if not output_gdal_file.exists():
                        gdal.VectorTranslate(
                            str(output_gdal_file),
                            str(json_file),
                            layerName=json_file.stem,
                        )
                    else:
                        gdal.VectorTranslate(
                            str(output_gdal_file),
                            str(json_file),
                            layerName=json_file.stem,
                            accessMode="update",
                        )

                    json_file.unlink()

        else:
            for objectclass in export_objectclasses:
                logger.info("Processing objectclass %s", objectclass)

                if isinstance(objectclass, str):
                    objectclass = self.project.objectclass(objectclass)

                if export_layers is None:
                    layers: Optional[List[EmsLayer]] = objectclass.layers
                else:
                    layers = [
                        layer
                        for layer in objectclass.layers
                        if str(layer) in export_layers
                    ]
                if layers is not None:
                    for layer in layers:
                        output_file_path = self._generate_output_file_name(
                            output_path, objectclass, layer
                        )
                        self._save_layer_as_json(layer, output_file_path)

            logger.info("Generate GDAL file")
            output_gdal_file = output_path / f"{output_filename}_.{extension}"
            for json_file in output_path.glob("*.json"):

                if extension in ["shp", "csv"]:
                    output_gdal_file = output_path / f"{json_file.stem}.{extension}"

                if not output_gdal_file.exists():
                    gdal.VectorTranslate(
                        str(output_gdal_file),
                        str(json_file),
                        layerName=json_file.stem,
                    )
                else:
                    gdal.VectorTranslate(
                        str(output_gdal_file),
                        str(json_file),
                        layerName=json_file.stem,
                        accessMode="update",
                    )

                json_file.unlink()

        logger.info("Generate GDAL file")
        output_gdal_file = output_path / f"{output_filename}.{extension}"
        for json_file in output_path.glob("*.json"):

            if extension in ["shp", "csv"]:
                output_gdal_file = output_path / f"{json_file.stem}.{extension}"

            if not output_gdal_file.exists():
                gdal.VectorTranslate(
                    str(output_gdal_file),
                    str(json_file),
                    layerName=json_file.stem,
                )
            else:
                gdal.VectorTranslate(
                    str(output_gdal_file),
                    str(json_file),
                    layerName=json_file.stem,
                    accessMode="update",
                )

            json_file.unlink()

        logger.info("Closing the communication with WEGA-EMS")
        self.service.close()
