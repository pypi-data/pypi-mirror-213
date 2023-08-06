import os
import tempfile
import unittest

import numpy as np
import nure.code
import nure.dataframe
import pandas as pd


class CoderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.np_chars = np.array([chr(c) for c in range(ord('A'), ord('Z'))])
        self.df = pd.DataFrame(data={
            'col1': np.random.choice(self.np_chars, size=10000, replace=True),
            'col2': np.random.choice(self.np_chars, size=10000, replace=True)
        })

        self.df.to_csv('tests/data/coder.csv', index=False)

    def test_coder(self):
        coder = nure.code.LabelCoder()
        # check return_value False
        encoded = coder.encode(['A', 'B', 'C'], return_value=False, expand=True)
        self.assertIsNone(encoded)
        self.assertEqual(
            set(coder._code_dict),
            set([None, 'A', 'B', 'C'])
        )

        # check expand False
        encoded = coder.encode(['A', 'B', 'C', 'D', 1, None], return_value=True, expand=False)
        self.assertEqual(
            set(coder._code_dict),
            set([None, 'A', 'B', 'C'])
        )

        # check encoded function
        decoded = coder.decode(encoded)
        self.assertTrue(np.all(decoded == ['A', 'B', 'C', None, None, None]))

        # check expand True
        encoded = coder.encode(['E'], return_value=True, expand=True)
        self.assertEqual(
            set(coder._code_dict),
            set([None, 'A', 'B', 'C', 'E'])
        )

    def test_dataframe(self):
        df1, coders1 = nure.dataframe.read_csv_and_encode('tests/data/coder.csv', encode_columns=['col1', 'col2'], chunksize=None)
        df2, coders2 = nure.dataframe.read_csv_and_encode('tests/data/coder.csv', encode_columns=['col1', 'col2'], chunksize=100)
        # check has encoders
        self.assertTrue('col1' in coders1 and 'col2' in coders1)
        # check encoding correctly
        self.assertEqual(
            set(coders1['col1']._code_dict),
            set(coders2['col1']._code_dict)
        )

        # check shapes
        self.assertEqual(self.df.shape, df1.shape)
        self.assertEqual(self.df.shape, df2.shape)

        # check save function
        with tempfile.TemporaryDirectory() as tmpdir:
            out1_fn = os.path.join(tmpdir, 'out1.csv')
            nure.dataframe.decode_and_write_csv(out1_fn, df1, coders1, chunksize=None, index=False)
            self.assertTrue(os.path.exists(out1_fn))

            out2_fn = os.path.join(tmpdir, 'out2.csv')
            nure.dataframe.decode_and_write_csv(out2_fn, df2, coders2, chunksize=100, index=False)
            self.assertTrue(os.path.exists(out2_fn))

            df1 = pd.read_csv(out1_fn)
            df2 = pd.read_csv(out2_fn)
            for col in df1.columns:
                self.assertTrue(np.all(df1[col] == df2[col]))

    def tearDown(self) -> None:
        os.remove('tests/data/coder.csv')
