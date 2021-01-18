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
import tempfile
import unittest

from tensorflow.python.keras.backend import clear_session

from test.util.store_logs_callback import StoreLogsCallback
from tfaip.base import TrainerParams
from tfaip.scenario.tutorial.full.data.data_params import DataParams
from tfaip.scenario.tutorial.full.scenario import TutorialScenario


def get_default_data_params():
    params = DataParams()
    params.train.batch_size = 1
    params.train.limit = 50
    params.val.batch_size = 1
    params.val.limit = 50
    return params


def get_default_scenario_params():
    default_params = TutorialScenario.default_params()
    default_params.data_params = get_default_data_params()
    return default_params


class TestMultipleValLists(unittest.TestCase):
    def setUp(self) -> None:
        clear_session()

    def tearDown(self) -> None:
        clear_session()

    def test_lav_during_training(self):
        with tempfile.TemporaryDirectory() as d:
            # Train with ema and without ema with same seeds
            # train loss must be equals, but with ema the validation outcomes must be different
            store_logs_callback = StoreLogsCallback()
            scenario_params = get_default_scenario_params()
            trainer_params = TrainerParams(
                epochs=1,
                samples_per_epoch=1,
                scenario_params=scenario_params,
                skip_model_load_test=True,
                random_seed=1337,
                lav_every_n=1,
                checkpoint_dir=d,
            )
            trainer = TutorialScenario.create_trainer(trainer_params)
            trainer.train(callbacks=[store_logs_callback])
            train_logs = store_logs_callback.logs
            # Tutorial yields two LAV datasets (test and train)
            for i in range(2):
                self.assertAlmostEqual(train_logs[f'lav_l{i}_acc'], train_logs[f'lav_l{i}_simple_acc'])
