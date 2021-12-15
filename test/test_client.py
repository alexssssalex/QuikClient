from src.quikclient import QuikClient
import pytest
from src.quikclient.ExceptionQuikClient import ExceptionQuikClient

classes = ['CROSSRATE', 'SMAL', 'INDX', 'TQBR', 'CETS', 'SPBFUT', 'RTSIDX', 'SPBOPT']


def test_error_no_connection_with_init():
    with pytest.raises(ExceptionQuikClient):
        QuikClient(port=1111)


def test_init():
    c = QuikClient()
    assert c is not None


def test_get_classes_list():
    c = QuikClient()
    classes = set(c.get_classes_list())
    assert set(classes) == set(classes)


def test_get_classes_info():
    c = QuikClient()
    for cls in classes:
        assert set(c.get_class_info(cls).keys()) == {'nsecs', 'name', 'code', 'firmid', 'npars'}


def test_get_class_codes():
    c = QuikClient()
    for cls in classes:
        cls = 'CROSSRATE'
        codes = c.get_class_codes(cls)
        assert isinstance(codes, list)


def test_get_class_code_info():
    c = QuikClient()
    for cls in classes:
        for code in c.get_class_codes(cls):
            info = c.get_class_code_info(cls, code)
            assert info is None or isinstance(info, dict)


def test_get_candle_data():
    c = QuikClient()
    intervals = ['INTERVAL_M1', 'INTERVAL_M2', 'INTERVAL_M6', 'INTERVAL_M10', 'INTERVAL_M15', 'INTERVAL_M20',
                 'INTERVAL_M30',
                 'INTERVAL_H1', 'INTERVAL_H2', 'INTERVAL_H4', 'INTERVAL_D1', 'INTERVAL_W1', 'INTERVAL_MN1']
    for interval in intervals:
        df = c.get_candle_data('TQBR', 'GAZP', interval)
        assert all(df.columns.isin(['D', 'H', 'L', 'O', 'C', 'V']))
