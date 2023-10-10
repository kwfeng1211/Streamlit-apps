import streamlit as st
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
