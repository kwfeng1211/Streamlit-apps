import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title("Streamlit 超入門")

# st.write("DataFrame")
st.write("プレグレスバーの表示")
"Start!!"

latest_iteration = st.empty()  # 空を用意して
bar = st.progress(0)  # barを走る

for i in range(100):
    latest_iteration.text(f"Iteration {i+1}")
    bar.progress(i + 1)  # barをi+1の形に進む
    time.sleep(0.1)  # 止まる時間の設定するコマンド

"完成！！"

# text = st.sidebar.text_input('あなたの趣味をおしえてください')
# condition = st.sidebar.slider("あなたの調子は", 0, 100, 50)  # .sidebar左で表現するサイドバー


left_column, right_column = st.columns(2)
button = left_column.button("右カラムに文字を表示")
if button:
    right_column.write("ここは右カラム")

expander1 = st.expander("問い合わせ")  # .expander下拉式選單,
expander1.write("問い合わせ内容1")  # 選單內的內容
expander2 = st.expander("問い合わせ")  # .expander下拉式選單,
expander2.write("問い合わせ内容2")  # 選單內的內容
expander3 = st.expander("問い合わせ")  # .expander下拉式選單,
expander3.write("問い合わせ内容3")  # 選單內的內容

# text = st.text_input('あなたの趣味をおしえてください')
# 'あなたの趣味は:', text, "です。"
# condition = st.slider("あなたの調子は", 0, 100, 50)
# "コンディション", condition

# """
# これは↑のスライドsliderのコマンドです。
# condition = st.slider("あなたの調子は", 0, 100, 50) #
# "コンディション", condition

# """


# 下はセレクトの表示の例です、list(range（）)の数字を下のoptionに表示するように。
# option = st.selectbox(
#     "あなたの好きな数字をおしえてください",
#     list(range(1, 11))
# )
# "あなたが好きな数字は", option, "です。"


# if st.checkbox("Show Image"):#←は画像にチェックボックス式にするやり方です。
#     img = Image.open("8348.jpg")
#     st.image(img, caption="kwfeng", use_column_width=True)

# df = pd.DataFrame({
#     "一列目": [1, 2, 3, 4],
#     "二列目": [10, 20, 30, 40]
# })

# dataframeだけが widthとheight指定できます。
# st.dataframe(df.style.highlight_max(axis=0))
# 表示の仕方が違うtableただの表を表示したいときに使う、変更ができません。
# st.table(df.style.highlight_max(axis=0))
# # st.write(df)  # writeは指定できません
# df = pd.DataFrame(
#     np.random.rand(100, 2) / [50, 50]+[35.69, 139.70],
#     columns=["lat", "lon"]
# )

# st.line_chart(df)  # 線グラフの形で表現
# st.area_chart(df)  # エリアの範囲の形で表現
# st.map(df)         # マップの表現の仕方
