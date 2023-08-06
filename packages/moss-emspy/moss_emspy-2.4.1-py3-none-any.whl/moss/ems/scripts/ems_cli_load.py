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

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

from moss.ems.emsproject import EmsProject
from moss.ems.emsservice import EmsServiceException, Service
from moss.ems.extra.geometry_converter import GeojsonConverter

logger = logging.getLogger("ems_cli_export")

try:
    from osgeo import gdal
except ImportError:
    logger.error("This function need GDAL Python bindings.")


class EmsCliLoadException(Exception):
    pass


class EmsCliLoad:
    def __init__(
        self,
        url: str,
        project: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):

        if username and password:
            logger.debug("Logging in using username and password.")
            try:
                self.service = Service(url, username=username, password=password)
            except EmsServiceException:
                logger.error("Can not connect to service using username and password.")
                raise EmsCliLoadException
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
                raise EmsCliLoadException
        except EmsServiceException:
            logger.error("The project %s does not exists in %s", project, url)
            raise EmsCliLoadException

    def ems_load(
        self,
        input_path: str,
        object_class: str,
        layer_name: str,
        variant_id: Optional[int] = 11,
    ):

        logger.info("Starting load...")
        self.objectclass = object_class
        self.layername = layer_name
        my_project = self.project
        logger.info("ObjectClass: {0}".format(object_class))
        logger.info("Input Path: {0}".format(input_path))
        logger.info("Layer Name: {0}".format(layer_name))
        logger.info("Variant ID: {0}".format(variant_id))

        if not isinstance(input_path, str):
            input_path = str(input_path)

        if not Path(input_path).exists():
            raise EmsCliLoadException("The output path %s not exists.", input_path)

        if input_path.endswith(".shp") or input_path.endswith(".gpkg"):
            logger.debug("Input is a file not a directory")

            with tempfile.TemporaryDirectory() as temp_directory:
                geojson_path = Path(temp_directory) / "output.json"

                gdal.VectorTranslate(
                    str(geojson_path),
                    str(input_path),
                    layerName="output",
                    format="GeoJSON",
                )

                with open(geojson_path, "r") as geo_js:
                    data_geojson = json.loads(geo_js.read())

                esri_geometries = []
                for feature in data_geojson["features"]:
                    esri_output = GeojsonConverter.to_esri(feature)

                    if esri_output:
                        esri_geometries.append(esri_output)

                my_layer = my_project.objectclass(self.objectclass).layer(
                    self.layername
                )

                # sending to ems
                output = my_layer.add_features(
                    features=esri_geometries,
                    variant_id=variant_id,
                )
        else:
            for file in os.listdir(input_path):
                if file.endswith(".gpkg") or file.endswith(".shp"):
                    shape_path = Path(input_path) / file
                    file_name = file.split(".")[0]
                    json_name = "{0}.{1}".format(file_name, "json")
                    geojson_path = Path(input_path) / str(json_name)

                    # shape to geojson
                    gdal.VectorTranslate(
                        str(geojson_path),
                        str(shape_path),
                        layerName=file_name,
                        format="GeoJSON",
                    )

                    # geojson to esri
                    with open(geojson_path, "r") as geo_js:
                        data_geojson = json.loads(geo_js.read())

                    esri_geometries = []
                    for feature in data_geojson["features"]:
                        esri_output = GeojsonConverter.to_esri(feature)

                        if esri_output:
                            esri_geometries.append(esri_output)

                    my_layer = my_project.objectclass(self.objectclass).layer(
                        self.layername
                    )

                    # sending to ems
                    output = my_layer.add_features(
                        features=esri_geometries,
                        variant_id=variant_id,
                    )
                    # response
                    logger.info("Respond from ems: %s", output)
                    geojson_path.unlink()

        logger.info("Closing the communication with WEGA-EMS")
        self.service.close()
