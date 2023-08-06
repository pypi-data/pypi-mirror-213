#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# ErrorsArtifact -- Store errors and generate errors.json file
# By: Bruno Duyé <bruno.duye@cepremap.org>
#
# Copyright (C) 2017 Cepremap
# https://git.nomics.world/dbnomics-fetchers/ecb-fetcher
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pathlib import Path

import toolz
import ujson as json


__all__ = ['ErrorsArtifact']


class ErrorsArtifact:
    datasets_errors = None          # list of dicts that contains errors on datasets
    general_errors = None           # list that contains general errors
    nb_expected_datasets = None     # Total number of datasets

    def __init__(self):
        self.datasets_errors = []
        self.general_errors = []

    def add_general_error(self, message):
        """ Add a general error; ie an error that prevented datasets processing
        """
        assert message is not None
        self.general_errors.append(message)

    def add_dataset_error(self, dataset_code, message=''):
        """ Add a dataset in datasets errors list
        """
        assert dataset_code is not None
        assert isinstance(dataset_code, str)
        assert isinstance(message, str), message
        self.datasets_errors.append(toolz.valfilter(lambda e: e, {  # filter None values
            "dataset_code": dataset_code,
            "message": message,
        }))

    def get_nb_errors(self):
        """ Return the current number of errors
        """
        return len(self.datasets_errors)

    def write_json_file(self, target_path, nb_expected_datasets=None):
        """ Write "errors.json" file in given path
        """
        target_path = Path(target_path)
        if self.general_errors:
            errors_json = {
                "general_errors": self.general_errors
            }
        else:
            nb_datasets = nb_expected_datasets if nb_expected_datasets is not None else self.nb_expected_datasets
            assert nb_datasets is not None, "Total number of datasets is required"
            errors_json = {
                'errors': self.datasets_errors,
                'nb_expected_datasets': nb_datasets,
            }
        with (target_path / 'errors.json').open('w', encoding='utf-8') as file_:
            json.dump(errors_json, file_, ensure_ascii=False, indent=2, sort_keys=True)
