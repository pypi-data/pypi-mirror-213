import os
import shutil
import unittest

import numpy as np
import nure.archive


class ArchiveTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data = np.random.normal(size=100)
        self.archive_fn = 'tests/data/archive.zip'
        self.root_dir = os.path.splitext(self.archive_fn)[0]

    def tearDown(self) -> None:
        if os.path.isdir(self.root_dir):
            shutil.rmtree(self.root_dir)
        if os.path.isfile(self.archive_fn):
            os.remove(self.archive_fn)

    def test_archive(self):
        archive = nure.archive.Archive(self.archive_fn, self.root_dir)
        data_mod_fn = archive.get('data.npy', mode='m')
        np.save(data_mod_fn, self.data)
        archive.pack()
        self.assertTrue(os.path.isfile(self.archive_fn))

        archive.cleanup()
        archive.ensure_dirs()
        archive.unpack()
        data_org_fn = archive.get('data.npy', mode='o')
        data = np.load(data_org_fn)
        self.assertTrue(np.all(data == self.data))
