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


@st.cache_data  # 素早くデータを取得するためのコマンド
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


try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin, ymax = st.sidebar.slider(
        "範囲を指定してください。",
        0.0, 500.0, (0.0, 500.0)  # 第三のステップのは（）を使ってスタート地点を指定できます。
    )

    tickers = {
        "apple": "AAPL",
        "facebook": "META",
        "google": "GOOGL",
        "microsoft": "MSFT",
        "netflix": "NFLX",
        "amazon": "AMZN"
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        "会社名を選擇してください",
        list(df.index),  # list()の中に入れればリスト化にできる。
        ["google", "amazon", "facebook", "apple"]
        # ↑大文字と小文字に区別があります。
    )

    if not companies:  # not もしcompaniesに何も入ってなかったら。
        st.error("少なくとも一社は選んでください。")
    else:
        data = df.loc[companies]
        st.write("### 株価 (USD)", data.sort_index())
        data = data.T.reset_index()  # データをD新しいataFreme型に返してくる
        data = pd.melt(data, id_vars=["Date"]).rename(
            columns={"value": "Stock Prices(USD)"}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD)", stack=None,
                        scale=alt.Scale(domain=[ymin, ymax])),
                color="Name:N"
            )
        )
        st.altair_chart(chart, use_container_width=True)

except:
    st.error(
        "おっと！何がエラーが起きているようです。"
    )
