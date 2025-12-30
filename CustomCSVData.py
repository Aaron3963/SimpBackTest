from backtrader.feeds import GenericCSVData

class CustomCSVData(GenericCSVData):
    """
    A customized CSV Data feed derived from GenericCSVData.
    It supports a 'preset' parameter to quickly load 3 specific CSV formats.
    """
    
    # Add a 'preset' parameter to our class
    params = (
        ('preset', 'standard'), 
    )

    def __init__(self):
        presets = {
            # Format 1: Standard prediction
            'standard': {
                'dtformat': '%Y-%m-%d',
                'datetime': 0,
                'open': 1,
                'high': 2,
                'low': 3,
                'close': 4,
                'volume': 5,
            },

            # Format 2: date indexed e.g. 002054.XSHE.csv
            # CSV Header: ,open,close,high,low,volume,money,avg,high_limit,low_limit,pre_close,paused,factor
            'dateIndexed': {
                'dtformat': '%Y-%m-%d',
                'datetime': 0,
                'open': 1,
                'high': 2,
                'low': 3,
                'close': 4,
                'volume': 5,
                'openinterest': -1
            },

            # Format 3: Hourly data, e.g. ERCOTDA_price.csv
            # CSV Header: Date,Hour_of_Day,Close
            'hourly': {
                'dtformat': '%d/%m/%Y',
                'tmformat': '%H',
                'datetime': 0,
                'time': 1,
                'close': 2,
                'open': -1,
                'high': -1,
                'low': -1,
                'volume': -1,
                'openinterest': -1
            },
            # Format 4: predicted signals, use openInterest to store predicted signal
            # CSV Header: Date,Close,Actual,Predicted
            'predicted': {
                'dtformat': '%Y-%m-%d',
                'datetime': 0,
                'close': 4,
                'open': 1,
                'high': 2,
                'low': 3,
                'volume': -1,
                'openinterest': 7
            }
        }

        # Apply the configuration based on the 'preset' parameter
        if self.p.preset in presets:
            config = presets[self.p.preset]
            
            # Dynamically set the parameters of the instance
            # We iterate over the config dict and set self.p.<param>
            for param, value in config.items():
                setattr(self.p, param, value)
        else:
            print(f"Warning: Preset '{self.p.preset}' not found. Using defaults.")

        # Initialize the parent class
        super().__init__()