import pandas as pd
import yfinance as yf
import streamlit as st
import altair as alt

st.title("米国株価可視化アプリ")

st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションが表示日付を指定できます。
""")
st.sidebar.write("""
## 表示日数の選擇
""")

days = st.sidebar.slider("日数", 1, 50, 20)

st.write(f"""
### 過去 **{days}** のGAFA株価  
""")


@st.cache  # 素早くデータを取得するためのコマンド
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f"{days}d")
        hist.index = hist.index.strftime("%d %B %Y")
        hist = hist[["Close"]]  # Closeだけの取得
        # カラムの列名を変更 動画では"company"でしたが、正しいやり方は[company]でした。
        hist.columns = [company]
        hist = hist.T
        hist.index.name = "Name"  # インデックスの列名を変更
        df = pd.concat([df, hist])
    return df


st.sidebar.write("""
## 株価の範囲指定
""")


ymin, ymax = st.sidebar.slider(
    "範囲を指定してください。",
    0.0, 3500.0, (0.0, 3500.0)  # 第三のステップのは（）を使ってスタート地点を指定できます。
)
