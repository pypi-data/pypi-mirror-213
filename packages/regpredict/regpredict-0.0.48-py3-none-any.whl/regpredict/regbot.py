#!/usr/bin/env python3
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import joblib
import numpy as np
from pkg_resources import resource_filename
import fire, warnings
from dataclasses import dataclass

@dataclass
class Regbot:
  open: float
  high: float
  asks: float
  bids: float
  vc: float
  ema_26: float
  ema_12: float
  macd: float
  macdsignal: float
  macd_histogram: float
  low: float
  grad_histogram: float
  close: float
  rsi_05: float
  rsi_15: float
  sma_25: float
  close_grad: float
  close_grad_neg: float
  grad_sma_25: float
  reg_model_path: str = resource_filename(__name__, 'minute_model.pkl')
  scaler_path: str = resource_filename(__name__, 'minutescaler.gz')

  def loadmodel(self):
    try:
      return joblib.load(open(f'{self.reg_model_path}', 'rb'))
    except Exception as e:
      return {
        'Error': e
      }


  def prepareInput(self):
    try:
      test_data = np.array([[self.open,self.high,self.asks,self.bids,self.vc,self.ema_26,self.ema_12,self.macd,self.macdsignal,
                            self.macd_histogram,self.low,self.grad_histogram,self.close,self.rsi_05,self.rsi_15,self.sma_25,self.close_grad,
                            self.close_grad_neg,self.grad_sma_25]])
      scaler = joblib.load(f'{self.scaler_path}')
      return scaler.transform(test_data)
    except Exception as e:
      return {
        'Error': e
      }


  def buySignalGenerator(self):
    try:
      return (self.loadmodel().predict(self.prepareInput())[0])
    except Exception as e:
      return {
        'Error': e
      }



def signal(open,high,asks,bids,vc,ema_26,ema_12,macd,macdsignal,macd_histogram,low,grad_histogram,close,
          rsi_05,rsi_15,sma_25,close_grad,close_grad_neg,grad_sma_25):
  try:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        return Regbot(open,high,asks,bids,vc,ema_26,ema_12,macd,macdsignal,macd_histogram,low,
                      grad_histogram,close,rsi_05,rsi_15,sma_25,close_grad,
                      close_grad_neg,grad_sma_25).buySignalGenerator()
  except Exception as e:
    return {
      'Error': e
    }


if __name__ == '__main__':
  fire.Fire(signal)
