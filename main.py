import json
from linebot import LineBotApi
from linebot.models import TextSendMessage
import yfinance as yf

#設定ファイルを開く
with open("info.json","r") as file:
    info = json.load(file)

#チャンネルトークンを変数に格納
#LINE bot APIを生成
CHANNEL_TOKEN = info['CHANNEL_TOKEN']
line_bot_api = LineBotApi(CHANNEL_TOKEN)

#株式情報をYahooファイナンスから取り出す変数を作る
def get_stock_data(code):
    df = yf.download(code, period='7d', interval ="1d").sort_index()
    return df

#一番直近の終値を取り出す変数を作る
def get_close(df):
    return df.tail(1)['Close'].values

#ATRを算出する変数を作る
def get_ATR(df):
    TH = df[-1:]['High'].values
    TL = df[-1:]['Low'].values
    YC = df[-2:-1]['Close'].values

    #当日高値ー当日安値
    R1 = TH - TL
    #当日高値ー前日終値
    R2 = TH - YC
    #当日安値ー前日終値
    R3 = TL - YC

#真の値幅（三つの値の中で一番大きい）を返す
    return max(R1,R2,R3)

#真の値幅、値幅５０％、値幅８０％を算出し、ラインに送る
#\nは改行の意味、strは数値→文章化
def main():
    USER_ID = info['USER_ID']

    df = get_stock_data('^N225')
    price = str(get_close(df)[0])
    ATR = round(get_ATR(df)[0],2)

    mess = "日経平均終日終値" + price + "\n"\
    "真の値幅" + str(ATR) + "\n"\
    "真の値幅(50%)"  + str(ATR*0.5) + "\n"\
    "真の値幅(80%)"  + str(ATR*0.8) + "\n"\

    messages = TextSendMessage(text= mess)
    line_bot_api.push_message(USER_ID, messages=messages)

if __name__== "__main__":
    main()
    