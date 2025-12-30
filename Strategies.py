import backtrader as bt

class Momentum3(bt.Strategy):
    
    params = (
        ('printlog', True),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        #predicted was mapped to openinterest
        self.signal = self.datas[0].openinterest 
        self.order = None # To track pending orders

    def log(self, txt, dt=None):
        if self.params.printlog:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')
            
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.4f}, Cost: {order.executed.value:.4f}, Comm: {order.executed.comm:.4f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.4f}, Cost: {order.executed.value:.4f}, Comm: {order.executed.comm:.4f}')
                
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        if self.order:
            return

        # ----- Build rolling 3-day confirmation -----
        last3 = self.signal.get(size=3)   # array of last 3 values, newest last

        # If we don't have 3 bars yet, skip
        if len(last3) < 3:
            return

        three_up = all(s == 1 for s in last3)   # 1,1,1 → buy signal
        three_down = all(s == 0 for s in last3) # 0,0,0 → sell/exit signal


        # ----- Trading Logic -----

        # No position → wait for 3 consecutive 1s
        if not self.position:
            if three_up:
                self.log(f'BUY CREATE (3-day confirmed), {self.dataclose[0]:.4f}')
                self.order = self.buy()

        # In a position → wait for 3 consecutive 0s
        else:
            if three_down:
                self.log(f'SELL CREATE (3-day confirmed), {self.dataclose[0]:.4f}')
                self.order = self.close()


class RollingVote(bt.Strategy):
    params = (
        ('window', 10),     # lookback window
        ('vote_buy', 0.6),  # buy if >= 60% are 1
        ('vote_sell', 0.6), # sell if >= 60% are 0
        ('printlog', True),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.signal = self.datas[0].openinterest  # ML prediction stored here
        self.order = None

    def log(self, txt, dt=None):
        if self.params.printlog:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status == order.Completed:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.4f}')
            else:
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.4f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log(f'OPERATION PROFIT, GROSS {trade.pnl:.4f}, NET {trade.pnlcomm:.4f}')

    def next(self):
        # If an order is pending, skip
        if self.order:
            return

        # Get last N signals
        N = self.params.window
        lastN = self.signal.get(size=N)

        # Not enough bars yet
        if len(lastN) < N:
            return

        # Voting
        count_ones = sum(lastN)
        count_zeros = N - count_ones

        buy_cond = (count_ones / N) >= self.params.vote_buy
        sell_cond = (count_zeros / N) >= self.params.vote_sell

        # No position
        if not self.position:
            if buy_cond:
                self.log(f'BUY CREATE (vote {count_ones}/{N}), Price: {self.dataclose[0]:.4f}')
                self.order = self.buy()
        else:
            if sell_cond:
                self.log(f'SELL CREATE (vote {count_zeros}/{N}), Price: {self.dataclose[0]:.4f}')
                self.order = self.close()