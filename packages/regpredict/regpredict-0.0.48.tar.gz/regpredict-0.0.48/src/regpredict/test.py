import pandas as pd
from regbot import signal

df = pd.read_csv('../reinforce/regbot_v47_training.csv')

y_pred = []
def getSignal(a,b,c,d,e,f,g,h,i,j,k,l,t,u,v,w,x,y,z):
    return signal(a,b,c,d,e,f,g,h,i,j,k,l,t,u,v,w,x,y,z)

print(df.head())
df = df.sample(frac=1).reset_index(drop=True)
print(df.head())
df = df[df['targets'] == 0].tail(20)
print(df.head())

df['result'] = df.apply(lambda row: getSignal(row['open'],row['high'],row['a'], row['b'],row['vc'],row['ema-26'],row['ema-12'],row['macd'],row['macdsignal'],
                                              row['macd-histogram'],row['low'],row['grad-histogram'], row['close'], row['rsi-05'],
                                              row['rsi-15'],row['sma-25'],row['close-gradient'],row['close-gradient-neg'],row['grad-sma-25']), axis=1)

print(df.head())

print(len(df[df['result'] == df['targets']]), len(df))
