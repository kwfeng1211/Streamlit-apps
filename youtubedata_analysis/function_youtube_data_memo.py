from apiclient.discovery import build
import pandas as pd
import streamlit as st

# キーに問題もしくは期限、ユニットの問題があれば↓のURLでしらべる
# https://console.cloud.google.com/apis/credentials?hl=zh-tw&project=youtube-data-analysis-402105
DEVELOPER_KEY = "AIzaSyDCFSYrgJS2tMLHIpIytMpD1_gP4UvfDCk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

maxResults = 30


def video_search(youtube, q="中国語", max_results=50):

    search_response = youtube.search().list(
        q=q,
        part="id,snippet",
        order="viewCount",
        type="video",
        maxResults=maxResults
    ).execute()

    items_id = []
    items = search_response["items"]
    for item in items:  # for分で下のようにビデオ一個取ったら下のIDとチャンネルも取る文章
        item_id = {}  # これは辞書型を
        item_id["video_id"] = item["id"]["videoId"]
        item_id["channel_id"] = item["snippet"]["channelId"]
        items_id.append(item_id)

    df_video = pd.DataFrame(items_id)

    return df_video


def get_results(df_video, threshold=20000):
    channel_ids = df_video['channel_id'].unique()

    subscriber_list = youtube.channels().list(
        id=",".join(channel_ids),
        part="statistics",
        fields="items(id,statistics(subscriberCount))"
    ).execute()

    subscribers = []
    for item in subscriber_list["items"]:
        subscriber = {}
        if len(item["statistics"]) > 0:
            subscriber["channel_id"] = item["id"]
            # print(item,len(item["statistics"]))#中に取れっているものを確認だけ。
            subscriber["subscriber_count"] = int(
                item["statistics"]["subscriberCount"])
        else:
            subscriber["channel_id"] = item["id"]
        subscribers.append(subscriber)

    df_subscribers = pd.DataFrame(subscribers)

    df = pd.merge(left=df_video, right=df_subscribers, on="channel_id")
    df_extracted = df[df["subscriber_count"] < threshold]

    video_ids = df_extracted["video_id"].tolist()

    videos_list = youtube.videos().list(
        id=",".join(video_ids),
        part="snippet,statistics",
        fields="items(id,snippet(title),statistics(viewCount))"
    ).execute()

    videos_info = []
    items = videos_list["items"]
    for item in items:
        video_info = {}
        video_info["video_id"] = item["id"]
        video_info["title"] = item["snippet"]["title"]
        video_info["view_count"] = item["statistics"]["viewCount"]
        videos_info.append(video_info)

    df_videos_info = pd.DataFrame(videos_info)

    results = pd.merge(left=df_extracted, right=df_videos_info, on="video_id")
    results = results.loc[:, ["video_id", "title",
                              "view_count", "subscriber_count", "channel_id"]]
    return results
# これから↓はstreamiltのコードです。


st.title("YouTube分析")

st.sidebar.write("## クリエと閾値の設定")
st.sidebar.write("### クリエの入力")
query = st.sidebar.text_input("検索クリエを入力してください", "Python自動化")

st.sidebar.write("### 閾値の設定")
threshold = st.sidebar.slider("登録者数の閾値", 0, 1000000, 500000)

st.write("### 選択中のパラメータ")
st.markdown(f"""
- 検索クリエ: {query}, 
- 登録社数の閾値: {threshold},
""")


df_video = video_search(youtube, q=query, max_results=50)
results = get_results(df_video, threshold=threshold)

st.write("### 分析結果", results)
st.write("### 動画再生")

video_id = st.text_input("動画IDを入力してください")
url = f"https://youtu.be/{video_id}"

video_field = st.empty()
video_field.write("こちらに動画が表示されます")

if st.button("ビデオ表示"):
    if len(video_id) > 0:  # ここはvideo_idの変数がもし1文字以上でしたらの設定。
        try:
            video_field.video(url)  # videoを表示するプログラム
        except:
            st.error("何がエラーが起きているようです。")
