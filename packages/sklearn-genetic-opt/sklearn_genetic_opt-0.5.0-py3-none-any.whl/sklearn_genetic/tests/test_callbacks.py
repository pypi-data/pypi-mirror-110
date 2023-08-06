import pytest
import os
import logging

from deap.tools import Logbook
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from .. import GASearchCV
from ..space import Integer, Continuous
from ..callbacks import (
    ThresholdStopping,
    ConsecutiveStopping,
    DeltaThreshold,
    LogbookSaver,
)
from ..callbacks.validations import check_stats, check_callback
from ..callbacks.base import BaseCallback

data = load_digits()
label_names = data["target_names"]
y = data["target"]
X = data["data"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)


def test_check_metrics():
    assert check_stats("fitness") is None

    with pytest.raises(Exception) as excinfo:
        check_stats("accuracy")
    assert (
        str(excinfo.value)
        == "metric must be one of ['fitness', 'fitness_std', 'fitness_max', 'fitness_min'], "
        "but got accuracy instead"
    )


def test_check_callback():
    callback_threshold = ThresholdStopping(threshold=0.8)
    callback_consecutive = ConsecutiveStopping(generations=3)
    assert check_callback(callback_threshold) == [callback_threshold]
    assert check_callback(None) == []
    assert check_callback([callback_threshold, callback_consecutive]) == [
        callback_threshold,
        callback_consecutive,
    ]

    with pytest.raises(Exception) as excinfo:
        check_callback(1)
    assert (
        str(excinfo.value)
        == "callback should be either a class or a list of classes with inheritance from "
        "callbacks.base.BaseCallback"
    )


def test_wrong_base_callback():
    class MyDummyCallback(BaseCallback):
        def __init__(self, metric):
            self.metric = metric

        def validate(self):
            print(self.metric)

    with pytest.raises(Exception) as excinfo:
        callback = MyDummyCallback()
    assert (
        str(excinfo.value)
        == "Can't instantiate abstract class MyDummyCallback with abstract methods __call__, on_step"
    )


def test_base_callback_call():
    possible_messages = [
        "Can't instantiate abstract class MyDummyCallback with abstract methods __call__",
        "Can't instantiate abstract class MyDummyCallback with abstract method __call__",
    ]

    class MyDummyCallback(BaseCallback):
        def __init__(self, metric):
            self.metric = metric

        def on_step(self, record=None, logbook=None, estimator=None):
            print(record)

    with pytest.raises(Exception) as excinfo:
        callback = MyDummyCallback(metric="fitness")

    assert any([str(excinfo.value) == i for i in possible_messages])


def test_threshold_callback():
    callback = ThresholdStopping(threshold=0.8)
    assert check_callback(callback) == [callback]
    assert not callback(record={"fitness": 0.5})
    assert callback(record={"fitness": 0.9})

    # test callback using LogBook instead of a record
    logbook = Logbook()
    logbook.record(fitness=0.93)
    logbook.record(fitness=0.4)

    assert not callback(logbook=logbook)

    logbook.record(fitness=0.95)

    assert callback(logbook=logbook)

    with pytest.raises(Exception) as excinfo:
        callback()
    assert (
        str(excinfo.value)
        == "At least one of record or logbook parameters must be provided"
    )


def test_consecutive_callback():
    callback = ConsecutiveStopping(generations=3)
    assert check_callback(callback) == [callback]

    logbook = Logbook()

    logbook.record(fitness=0.9)
    logbook.record(fitness=0.8)
    logbook.record(fitness=0.83)

    # Not enough records to decide
    assert not callback(logbook=logbook)

    logbook.record(fitness=0.85)
    logbook.record(fitness=0.81)

    # Current record is better that at least of of the previous 3 records
    assert not callback(logbook=logbook)

    logbook.record(fitness=0.8)

    # Current record is worst that the 3 previous ones
    assert callback(logbook=logbook)
    assert callback(logbook=logbook, record={"fitness": 0.8})

    with pytest.raises(Exception) as excinfo:
        callback()
    assert str(excinfo.value) == "logbook parameter must be provided"


def test_delta_callback():
    callback = DeltaThreshold(0.001)
    assert check_callback(callback) == [callback]

    logbook = Logbook()

    logbook.record(fitness=0.9)

    # Not enough records to decide
    assert not callback(logbook=logbook)

    logbook.record(fitness=0.923)
    logbook.record(fitness=0.914)

    # Abs difference is not bigger than the threshold
    assert not callback(logbook=logbook)

    logbook.record(fitness=0.9141)

    # Abs difference is bigger than the threshold
    assert callback(logbook=logbook)
    assert callback(logbook=logbook, record={"fitness": 0.9141})

    with pytest.raises(Exception) as excinfo:
        callback()
    assert str(excinfo.value) == "logbook parameter must be provided"


def test_logbook_saver_callback(caplog):
    callback = LogbookSaver("./logbook.pkl")
    assert check_callback(callback) == [callback]

    clf = DecisionTreeClassifier()
    evolved_estimator = GASearchCV(
        clf,
        cv=3,
        scoring="accuracy",
        generations=2,
        param_grid={
            "min_weight_fraction_leaf": Continuous(0, 0.5),
            "max_depth": Integer(2, 20),
            "max_leaf_nodes": Integer(2, 30),
        },
        verbose=False,
    )

    evolved_estimator.fit(X_train, y_train, callbacks=callback)

    assert os.path.exists("./logbook.pkl")

    os.remove("./logbook.pkl")

    with caplog.at_level(logging.ERROR):
        callback = LogbookSaver(checkpoint_path="./no_folder/logbook.pkl", estimator=4)
        callback()
    assert "Could not save the Logbook in the checkpoint" in caplog.text
