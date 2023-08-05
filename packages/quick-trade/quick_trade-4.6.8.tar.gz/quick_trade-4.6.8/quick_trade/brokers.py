import ccxt
import pandas as pd
from quick_trade import utils


class TradingClient(object):
    ordered: bool = False
    __side__: str
    ticker: str
    cls_open_orders: int = 0

    def __init__(self, client: ccxt.Exchange):
        self.client = client

    def order_create(self,
                     side: str,
                     ticker: str = 'None',
                     quantity: float = 0.0):
        utils.logger.info(f'quantity: {quantity}, side: {side}')
        if side == 'Buy':
            self.client.create_market_buy_order(symbol=ticker, amount=quantity)
        elif side == 'Sell':
            self.client.create_market_sell_order(symbol=ticker, amount=quantity)
        self.__side__ = side
        self.ticker = ticker
        self.ordered = True
        self._add_order_count()

    def get_ticker_price(self,
                         ticker: str) -> float:
        return float(self.client.fetch_ticker(symbol=ticker)['close'])

    def new_order_buy(self,
                      ticker: str = None,
                      quantity: float = 0.0,
                      credit_leverage: float = 1.0,
                      logging=True):
        self.order_create('Buy',
                          ticker=ticker,
                          quantity=quantity * credit_leverage)
        if logging:
            utils.logger.info('client buy')

    def new_order_sell(self,
                       ticker: str = None,
                       quantity: float = 0.0,
                       credit_leverage: float = 1.0,
                       logging=True):
        self.order_create('Sell',
                          ticker=ticker,
                          quantity=quantity * credit_leverage)
        if logging:
            utils.logger.info('client sell')

    def get_data_historical(self,
                            ticker: str = None,
                            interval: str = '1m',
                            limit: int = 1000):

        frames = self.client.fetch_ohlcv(ticker,
                                         interval,
                                         limit=limit)
        data = pd.DataFrame(frames,
                            columns=['time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        return data.astype(float)

    def exit_last_order(self):
        if self.ordered:
            if self.__side__ == 'Sell':
                self.new_order_buy(self.ticker, self.get_balance_ticker(self.ticker.split('/')[0]),
                                   logging=False)  # buy for all balance
            elif self.__side__ == 'Buy':
                self.new_order_sell(self.ticker, self.get_balance_ticker(self.ticker.split('/')[0]),
                                    logging=False)  # sell all
            self.__side__ = 'Exit'
            self.ordered = False
            utils.logger.info('client exit')
            self._sub_order_count()

    def get_balance_ticker(self, ticker: str) -> float:
        return self.client.fetch_free_balance()[ticker]

    @classmethod
    def _add_order_count(cls):
        cls.cls_open_orders += 1

    @classmethod
    def _sub_order_count(cls):
        cls.cls_open_orders -= 1
