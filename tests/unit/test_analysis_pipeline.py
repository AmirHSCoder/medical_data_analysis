from unittest import mock

from apps.analysis import pipeline


class DummyCommand:
    def __init__(self):
        self.messages = []

    def write_suc(self, msg):
        self.messages.append(("success", msg))

    def write_warn(self, msg):
        self.messages.append(("warning", msg))

    def write_err(self, msg):
        self.messages.append(("error", msg))


class DummyCollection:
    def __init__(self):
        self.inserted = []
        self.deleted = False
        self.replaced = None

    def delete_many(self, *_args, **_kwargs):
        self.deleted = True

    def insert_many(self, records):
        self.inserted.extend(records)

    def find(self, *_args, **_kwargs):
        return self.inserted

    def replace_one(self, *args, **kwargs):
        if len(args) > 1:
            self.replaced = args[1]
        else:
            self.replaced = kwargs.get("replacement")


def test_load_data_success():
    cmd = DummyCommand()
    collection = DummyCollection()

    pipeline.load_data(cmd, "tests/fixtures", "cross.csv", collection)

    assert collection.deleted
    assert len(collection.inserted) > 0
    assert collection.inserted[0]["ID"]
    assert ("success", mock.ANY) in cmd.messages


def test_load_data_missing_file(tmp_path):
    cmd = DummyCommand()
    collection = DummyCollection()

    pipeline.load_data(cmd, str(tmp_path), "missing.csv", collection)

    assert ("error", mock.ANY) in cmd.messages


class DummyPipeline:
    def __init__(self, *args, **kwargs):
        pass

    def fit(self, X, y):
        return None

    def score(self, X, y):
        return 1.0

    def predict(self, X):
        return [0 for _ in range(len(X))]

    def predict_proba(self, X):
        return [[0.5, 0.5] for _ in range(len(X))]


class DummyLabelEncoder:
    def fit_transform(self, y):
        return [0 for _ in y]

    def transform(self, y):
        return [0 for _ in y]


def test_train_and_store(monkeypatch):
    cmd = DummyCommand()
    cross = DummyCollection()
    long = DummyCollection()
    merged = DummyCollection()
    rf = DummyCollection()
    ycol = DummyCollection()

    def get_collection(name, alias="default"):
        mapping = {
            pipeline.CROSS_DATA_COLLECTION: cross,
            pipeline.LONG_DATA_COLLECTION: long,
            pipeline.MERGED_DATA: merged,
            pipeline.RF_RESULT: rf,
            pipeline.Y_RESULT: ycol,
        }
        return mapping[name]

    monkeypatch.setattr(pipeline, "get_collection", get_collection)
    monkeypatch.setattr(pipeline, "Pipeline", DummyPipeline)
    monkeypatch.setattr(pipeline, "LabelEncoder", DummyLabelEncoder)
    monkeypatch.setattr(
        pipeline, "train_test_split", lambda X, y, test_size, random_state: (X, X, y, y)
    )

    pipeline.train_and_store(cmd, "tests/fixtures")

    assert cross.deleted and long.deleted
    assert len(cross.inserted) > 0
    assert len(long.inserted) > 0
    assert rf.replaced is not None
    assert ycol.replaced is not None
    assert len(merged.inserted) > 0
