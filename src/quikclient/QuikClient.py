import json
import socket
from .ExceptionQuikClient import ExceptionQuikClient
import pandas as pd

# host = '127.0.0.1'
# port = 3587
# unicode = 'cp1251'
# # unicode = 'utf8'
# buff_size = 1024


class QuikClient:
    """
    Класс обеспечивающий связь с QUIK, передает команды и получает данные из QUIK,
    в случае ошибки генерит ExceptionQuikClient;
    """

    def __init__(self, host='127.0.0.1', port=3587, unicode='cp1251', buff_size=1024):
        self.host = host
        self.port = port
        self.unicode = unicode
        self.buf_size = buff_size
        if not self.is_conected():
            raise ExceptionQuikClient('Ошибка соединения с QUIK')

    @staticmethod
    def _check_cmd(cmd: str) -> None:
        """
        Проверка допустимой команды для сервера (должна быть строка и не должно быть \n)
        """
        if not isinstance(cmd, str):
            raise ExceptionQuikClient("Команда должна быть типа 'str'")
        if cmd.find('\n') != -1:
            raise ExceptionQuikClient("В строке команды не допускается символ LR(\\n)")

    def _get_cmd(self, cmd: str):
        """
        Получение результатов команды из QUiK
        """
        QuikClient._check_cmd(cmd)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            cmd_to_send = cmd + '\n'
            s.send(cmd_to_send.encode(self.unicode))
            number_chunk = json.loads(s.recv(32))
            res = b''
            for i in range(number_chunk):
                new_res = s.recv(self.buf_size)
                res += new_res
            result = json.loads(res.decode(self.unicode))
        except Exception as ex:
            raise ExceptionQuikClient('Ошибка соединения или передачи данных с QUIK') from ex
        return result

    def is_conected(self):
        try:
            connected_flag = self._get_cmd('is_connected()')
        except Exception:
            connected_flag = False
        return connected_flag

    def get_classes_list(self) -> list:
        """
        Получить список класcов интсрумента (акции, биржи, и т.д).

        Пример результата:
            ["SPBFUT","RTSIDX","SPBOPT","CROSSRATE","CETS","SMAL","INDX","TQBR","TQQI","TQDE"]
        """
        return self._get_cmd('get_classes_list()')

    def get_class_info(self, class_name: str) -> dict:
        """
        Вернуть информацию по классу.

        Пример результата:
            {'firmid': 'MC0139600000', 'name': 'МБ ФР: Т+ Акции и ДР', 'code': 'TQBR', 'npars': 64, 'nsecs': 260}
        """
        return self._get_cmd('get_class_info("' + class_name + '")')

    def get_class_codes(self, class_name: str) -> list:
        """
        Вернуть список кодов по классу.

        Пример результата:
            ['ABRD', 'AFKS', 'AFLT', 'AGRO', 'AKRN', 'ALBK', 'ALNU', 'ALRS', 'AMEZ', 'APTK', 'GAZP', 'SBER']
        """
        return self._get_cmd('get_class_codes("' + class_name + '")')

    def get_class_code_info(self, class_name: str, class_code: str) -> dict:
        """
        Информация по инсnрументу и коду:

        Пример результатов:

            {'isin_code': 'RU0007661625', 'bsid': '', 'cusip_code': '', 'stock_code': '', 'couponvalue': 0,
              'sell_leg_classcode': '', 'second_currcode': '', 'sell_leg_seccode': '', 'buy_leg_classcode': '',
              'base_active_classcode': '', 'class_code': 'TQBR', 'face_value': 5, 'buy_mat_date': 0,
              'option_strike': 0, 'name': '"Газпром" (ПАО) ао', 'qty_multiplier': 1, 'step_price_currency': '',
              'sedol_code': '', 'mat_date': 20210128, 'cfi_code': '', 'face_unit': 'SUR', 'code': 'GAZP',
              'ric_code': '', 'short_name': 'ГАЗПРОМ ао', 'buybackdate': 0, 'list_level': 1, 'qty_scale': 0,
              'yieldatprevwaprice': 0, 'buy_leg_seccode': '', 'regnumber': '1-02-00028-A',
              'min_price_step': 0.01, 'trade_currency': 'SUR', 'second_curr_qty_scale': 0,
              'first_curr_qty_scale': 0, 'base_active_seccode': '', 'sell_mat_date': 0, 'accruedint': 0,
              'stock_name': '', 'buybackprice': 0, 'lot_size': 10, 'nextcoupon': 0, 'couponperiod': 0,
              'scale': 2, 'sec_code': 'GAZP', 'class_name': 'МБ ФР: Т+ Акции и ДР', 'first_currcode': ''}
        """
        return self._get_cmd('get_class_code_info("' + class_name + '","' + class_code + '")')

    def get_candle_data(self, class_name: str, class_code: str, interval: str) -> pd.DataFrame:
        """
        Получение данные свечей.
            interval - одно из значений [INTERVAL_M1, INTERVAL_M2,...,INTERVAL_M6,INTERVAL_M10,
                INTERVAL_M15, INTERVAL_M20, INTERVAL_M30,INTERVAL_H1, INTERVAL_H2,INTERVAL_H4,
                INTERVAL_D1,  INTERVAL_W1, INTERVAL_MN1]

        Пример использования:
         get_candle_data('TQBR', 'GAZP', 'INTERVAL_M1')

        """
        data = self._get_cmd('get_candle_data("' + class_name + '","' + class_code + '",' + interval + ')')
        df = pd.DataFrame(data)
        if not df.empty:
            df['D'] = pd.to_datetime(df['D'])
            df = df[['D', 'H', 'L', 'O', 'C', 'V']]
        return df
