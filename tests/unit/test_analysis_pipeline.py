import os
import builtins
import csv
import types
from unittest import mock

import pandas as pd
import pytest

from apps.analysis import pipeline

class DummyCommand:
    def __init__(self):
        self.messages = []
    def write_suc(self, msg):
        self.messages.append(('success', msg))
    def write_warn(self, msg):
        self.messages.append(('warning', msg))
    def write_err(self, msg):
        self.messages.append(('error', msg))

class DummyCollection:
    def __init__(self):
        self.inserted = []
        self.deleted = False
    def delete_many(self, *_args, **_kwargs):
        self.deleted = True
    def insert_many(self, records):
        self.inserted.extend(records)


def test_load_data_success(tmp_path):
    csv_content = "ID,M/F,Hand,Age,Educ,SES,MMSE,CDR,eTIV,nWBV,ASF,Delay\n" \
                  "OAS1_0001_MR1,F,R,74,2,3,29,0,1344,0.743,1.306,N/A\n"
    csv_file = tmp_path / "cross.csv"
    csv_file.write_text(csv_content)

    cmd = DummyCommand()
    collection = DummyCollection()

    pipeline.load_data(cmd, str(tmp_path), "cross.csv", collection)

    assert collection.deleted
    assert len(collection.inserted) == 1
    assert collection.inserted[0]['ID'] == 'OAS1_0001_MR1'
    assert ('success', mock.ANY) in cmd.messages


def test_load_data_missing_file(tmp_path):
    cmd = DummyCommand()
    collection = DummyCollection()

    pipeline.load_data(cmd, str(tmp_path), "missing.csv", collection)

    assert ('error', mock.ANY) in cmd.messages
