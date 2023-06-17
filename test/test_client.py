import pandas as pd

from src.quikclient import QuikClient
import pytest
from src.quikclient.ExceptionQuikClient import ExceptionQuikClient

classes = ['CROSSRATE', 'SMAL', 'INDX', 'TQBR', 'CETS', 'SPBFUT', 'RTSIDX', 'SPBOPT']

DICT_TO_CHECK_ORDERS = {'STOP_ORDERS': ['stopflags', 'condition_class_code', 'active_to_time', 'orderdate',
                                        'expiry', 'client_code', 'canceled_uid', 'co_order_num', 'spread',
                                        'price', 'activation_date_time', 'filled_qty', 'ordertime', 'ordernum',
                                        'sec_code', 'flags', 'class_code', 'stop_order_type', 'linkedorder',
                                        'seccode', 'firmid', 'order_num', 'condition', 'condition_sec_code',
                                        'account', 'qty', 'trans_id', 'withdraw_datetime', 'order_date_time',
                                        'condition_seccode', 'offset', 'condition_price2', 'co_order_price',
                                        'brokerref', 'withdraw_time', 'balance', 'active_from_time',
                                        'alltrade_num', 'uid', 'condition_price'],
                        'TRADES': ['broker_commission_currency', 'linked_trade', 'userid', 'client_code',
                                   'order_qty', 'bank_acc_id', 'client_qualifier', 'cpfirmid',
                                   'mleg_base_sid', 'value', 'settle_currency', 'trade_currency',
                                   'start_discount', 'kind', 'side_qualifier', 'seccode', 'firmid',
                                   'investment_decision_maker_short_code', 'lseccode', 'account',
                                   'waiver_flag', 'operation_type', 'settlecode', 'trading_session',
                                   'clearing_firmid', 'repoterm', 'ts_commission_currency', 'uid',
                                   'trade_num', 'accruedint', 'exec_market', 'order_price',
                                   'executing_trader_qualifier', 'otc_post_trade_indicator', 'yield',
                                   'clearing_comission', 'price', 'reporate', 'canceled_datetime',
                                   'datetime', 'capacity', 'ordernum', 'benchmark', 'spot_rate', 'flags',
                                   'exchange_comission', 'repovalue', 'class_code', 'ext_trade_flags',
                                   'start_date', 'cross_rate', 'order_revision_number', 'upper_discount',
                                   'executing_trader_short_code', 'period', 'price2', 'tradenum',
                                   'order_num', 'system_ref', 'lower_discount', 'block_securities',
                                   'clearing_bank_accid', 'repo2value', 'qty', 'tech_center_comission',
                                   'liquidity_indicator', 'fixing_date', 'trans_id', 'station_id',
                                   'sec_code', 'accrued2', 'settle_date', 'extref', 'broker_comission',
                                   'brokerref', 'exchange_code', 'investment_decision_maker_qualifier',
                                   'canceled_uid', 'order_exchange_code', 'on_behalf_of_uid',
                                   'client_short_code'],
                        'ORDERS': ['userid', 'client_code', 'bank_acc_id', 'passive_only_order', 'value2',
                                   'activation_time', 'client_qualifier', 'sec_code', 'value',
                                   'settle_currency', 'filled_value', 'start_discount', 'linkedorder',
                                   'seccode', 'firmid', 'investment_decision_maker_short_code',
                                   'settle_date', 'ext_order_status', 'start_date', 'min_qty',
                                   'operation_type', 'settlecode', 'trading_session', 'repoterm',
                                   'repo_value_balance', 'accruedint', 'visible',
                                   'executing_trader_qualifier', 'yield', 'value_entry_type', 'price',
                                   'price_currency', 'settle_date2', 'datetime', 'capacity', 'ordernum',
                                   'flags', 'repovalue', 'class_code', 'exec_type', 'benchmark',
                                   'lseccode', 'qty2', 'price_entry_type', 'visible_repo_value',
                                   'executing_trader_short_code', 'price2', 'acnt_type', 'order_num',
                                   'awg_price', 'accepted_uid', 'uid', 'expiry', 'on_behalf_of_uid', 'qty',
                                   'ext_order_flags', 'reject_reason', 'exchange_code', 'trans_id',
                                   'withdraw_datetime', 'balance', 'side_qualifier', 'canceled_uid',
                                   'extref', 'account', 'brokerref', 'repo2value',
                                   'investment_decision_maker_qualifier', 'visibility_factor',
                                   'revision_number', 'expiry_time', 'client_short_code']}


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


def test_get_orders():
    c = QuikClient()
    for order, fields in DICT_TO_CHECK_ORDERS.items():
        df = c.get_orders(order)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            for field in fields:
                assert field in df.columns


def test_get_class_codes():
    c = QuikClient()
    for cls in classes:
        codes = c.get_class_codes(cls)
        assert isinstance(codes, list)


def test_get_class_code_info():
    c = QuikClient()
    for cls in classes:
        codes = c.get_class_codes(cls)
        # restrict number request
        for code in codes[:10]:
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
