# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for fedjax."""

import unittest

import fedjax


class FedjaxTest(unittest.TestCase):
  """Test fedjax can be imported correctly."""

  def test_import(self):
    self.assertTrue(hasattr(fedjax, 'FederatedAlgorithm'))
    self.assertTrue(hasattr(fedjax.aggregators, 'Aggregator'))
    self.assertTrue(hasattr(fedjax.algorithms, 'fed_avg'))
    self.assertTrue(hasattr(fedjax.datasets, 'emnist'))
    self.assertTrue(hasattr(fedjax.models, 'emnist'))
    self.assertTrue(hasattr(fedjax.training, 'save_checkpoint'))

  def test_no_core(self):
    self.assertFalse(hasattr(fedjax, 'core'))


if __name__ == '__main__':
  unittest.main()
