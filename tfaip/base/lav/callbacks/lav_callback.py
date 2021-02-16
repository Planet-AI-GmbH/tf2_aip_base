# Copyright 2020 The tfaip authors. All Rights Reserved.
#
# This file is part of tfaip.
#
# tfaip is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# tfaip is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# tfaip. If not, see http://www.gnu.org/licenses/.
# ==============================================================================
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tfaip.base.lav.lav import LAV
    from tfaip.base.model.modelbase import ModelBase
    from tfaip.base.data.data import DataBase


class LAVCallback(ABC):
    def __init__(self):
        self.lav: 'LAV' = None  # Set from lav
        self.data: 'DataBase' = None  # Set from lav
        self.model: 'ModelBase' = None  # set from lav

    @abstractmethod
    def on_sample_end(self, inputs, targets, outputs):
        pass

    @abstractmethod
    def on_step_end(self, inputs, targets, outputs, metrics):
        pass

    @abstractmethod
    def on_lav_end(self, result):
        pass
