import unittest
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import nure.array
import nure.dataframe
import pandas as pd


def linear(array, slope, inception=0):
    return array * slope + inception


def sum(dataframe, column):
    return pd.Series({
        column: np.sum(dataframe[column])
    })


def numpy_accumulate(generator):
    return np.concatenate(list(generator))


class ParallelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.array = np.random.randint(0, 100, size=100000)
        self.df = pd.DataFrame(data={
            'col1': np.random.randint(0, 100, size=100000),
            'col2': np.random.randint(0, 100, size=100000),
        })

    def assert_result(self, a1, a2):
        self.assertEqual(a1.shape, a2.shape)
        self.assertTrue(np.all(a1 == a2))

    def test_array(self):
        slope = 2
        inception = 5
        groundtruth = linear(self.array, slope, inception)
        chunksize = 5000

        def _chunk_generator_():
            for i in range(0, len(self.array), chunksize):
                yield self.array[i: i + chunksize]

        # test with default thread executor
        result = numpy_accumulate(nure.array.parallelize_iterable(
            _chunk_generator_(), linear, slope, inception=inception,
            preserve_order=True, executor=None, use_process=False))

        self.assert_result(result, groundtruth)

        # test with default process executor
        result = numpy_accumulate(nure.array.parallelize_iterable(
            _chunk_generator_(), linear, slope=slope, inception=inception,
            preserve_order=True, executor=None, use_process=True))

        self.assert_result(result, groundtruth)

        # test with defined process executor, specific chunksize
        with ThreadPoolExecutor() as executor:
            result = numpy_accumulate(nure.array.parallelize_iterable(
                _chunk_generator_(), linear, slope, inception=inception,
                preserve_order=True, executor=executor))

        self.assert_result(result, groundtruth)

    def test_dataframe_apply(self):
        slope = 2
        inception = 5
        groundtruth = self.df.apply(linear, slope=slope, inception=inception)
        results = nure.dataframe.apply(
            self.df, linear, slope=slope, inception=inception,
            executor=None, chunksize=None, use_process=False)

        # it does not guarantee the order after groupby
        groundtruth = groundtruth.sort_index()
        results = results.sort_index()

        self.assert_result(results['col1'], groundtruth['col1'])
        self.assert_result(results['col2'], groundtruth['col2'])

    def test_dataframe_groupby_apply(self):
        slope = 2
        inception = 5
        groundtruth = self.df.groupby('col1').apply(linear, slope=slope, inception=inception)
        results = nure.dataframe.groupby_apply(
            self.df.groupby('col1'), linear, slope, inception=inception,
            executor=None, chunksize=None, use_process=False)

        # it does not guarantee the order after groupby
        groundtruth = groundtruth.sort_index()
        results = results.sort_index()

        self.assert_result(results['col1'], groundtruth['col1'])
        self.assert_result(results['col2'], groundtruth['col2'])

    def test_dataframe_groupby_apply_record(self):
        groundtruth = self.df.groupby('col1').apply(sum, 'col2')
        results = nure.dataframe.groupby_apply(
            self.df.groupby('col1'), sum, 'col2',
            executor=None, chunksize=None, use_process=False, retain_order=True)

        self.assert_result(results['col2'].values, groundtruth['col2'].values)
