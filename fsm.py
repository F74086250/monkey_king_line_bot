from transitions.extensions import GraphMachine
import os
import sys
import requests
from pprint import pprint
from datetime import datetime
from utils import send_text_message
import message
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,ImageSendMessage,AudioSendMessage
import random
YOUTUBE_API_KEY = "AIzaSyDzE5WYhE6bTj-lu-xoi0Lb7L_UaeUIeHI"
video_url=[]
video_title=[]
image_audio_path=[]
image_audio_path.append(("https://media.discordapp.net/attachments/644155945420587020/926884695935955004/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125220265959434/artrox48.mp3"))  #artrox48
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927066818764472360/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125220739936316/compare_breast.mp3")) #compare breast
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927071992375570432/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125220945444874/deadliest_burn.mp3")) #deadliest burn
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927062533771264000/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125221306138674/fly_away.mp3"))     #fly away
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927070298967248917/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125221490700328/kiss.mp3"))  #kiss
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927077914221113354/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125303996854292/you_are_furious.mp3"))  #furious
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927078354748837999/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125303560658954/pick48pick.mp3"))    #pick48pick
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927079833748504646/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125303770365973/who_dare_to_surrend.mp3"))  #who want surrend
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927082358954410014/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125303380287579/monkey_congratulation.mp3")) #congratulation
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927061636697710592/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125221675270204/knock_your_head.mp3"))   #knock your head
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927151100279267328/AKedOLQlgszyJvY2Rg2WxOvJv7Zm_waH3J93YG5_QBcCdws900-c-k-c0x00ffffff-no-rj.png","https://cdn.discordapp.com/attachments/644155945420587020/927125304202395678/6bb7c1e977937ef3.mp3"))  # good luck to you
image_audio_path.append(("https://cdn.discordapp.com/attachments/644155945420587020/927143152387772446/unknown.png","https://cdn.discordapp.com/attachments/644155945420587020/927125221088067584/fetch_breast.mp3"))  #fetch your breast
def main():
    youtube_channel_id = "UC-lepqi1Wrt78Pbuldn49_Q"

    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    uploads_id = youtube_spider.get_channel_uploads_id(youtube_channel_id)
    print(uploads_id)

    video_ids = youtube_spider.get_playlist(uploads_id, max_results=3)
    for i in video_ids:
      video_url.append("https://www.youtube.com/watch?v="+i)
    print(video_url)
    #video_info=youtube_spider.get_video(youtube_channel_id)
    #print(video_info)


class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key

    def get_html_to_json(self, path):
        """組合 URL 後 GET 網頁並轉換成 JSON"""
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data

    def get_channel_uploads_id(self, channel_id, part='contentDetails'):
        """取得頻道上傳影片清單的ID"""
        # UC7ia-A8gma8qcdC6GDcjwsQ
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        try:
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            uploads_id = None
        return uploads_id

    def get_playlist(self, playlist_id, part='contentDetails', max_results=10):
        """取得影片清單ID中的影片"""
        # UU7ia-A8gma8qcdC6GDcjwsQ
        path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}'
        data = self.get_html_to_json(path)
        if not data:
            return []

        video_ids = []
        for data_item in data['items']:
            video_ids.append(data_item['contentDetails']['videoId'])
        return video_ids

    def get_video(self, video_id, part='snippet,statistics'):
        """取得影片資訊"""
        # jyordOSr4cI
        # part = 'contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails'
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        # 以下整理並提取需要的資料
        data_item = data['items'][0]

        try:
            # 2019-09-29T04:17:05Z
            time_ = datetime.strptime(data_item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            # 日期格式錯誤
            time_ = None

        url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

        info = {
            'id': data_item['id'],
            'channelTitle': data_item['snippet']['channelTitle'],
            'publishedAt': time_,
            'video_url': url_,
            'title': data_item['snippet']['title'],
            'description': data_item['snippet']['description'],
            'likeCount': data_item['statistics']['likeCount'],
            'dislikeCount': data_item['statistics']['dislikeCount'],
            'commentCount': data_item['statistics']['commentCount'],
            'viewCount': data_item['statistics']['viewCount']
        }
        #print(data_item['snippet']['title'])
        return info

    def get_comments(self, video_id, page_token='', part='snippet', max_results=100):
        """取得影片留言"""
        # jyordOSr4cI
        path = f'commentThreads?part={part}&videoId={video_id}&maxResults={max_results}&pageToken={page_token}'
        data = self.get_html_to_json(path)
        if not data:
            return [], ''
        # 下一頁的數值
        next_page_token = data.get('nextPageToken', '')

        # 以下整理並提取需要的資料
        comments = []
        for data_item in data['items']:
            data_item = data_item['snippet']
            top_comment = data_item['topLevelComment']
            try:
                # 2020-08-03T16:00:56Z
                time_ = datetime.strptime(top_comment['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                # 日期格式錯誤
                time_ = None

            if 'authorChannelId' in top_comment['snippet']:
                ru_id = top_comment['snippet']['authorChannelId']['value']
            else:
                ru_id = ''

            ru_name = top_comment['snippet'].get('authorDisplayName', '')
            if not ru_name:
                ru_name = ''

            comments.append({
                'reply_id': top_comment['id'],
                'ru_id': ru_id,
                'ru_name': ru_name,
                'reply_time': time_,
                'reply_content': top_comment['snippet']['textOriginal'],
                'rm_positive': int(top_comment['snippet']['likeCount']),
                'rn_comment': int(data_item['totalReplyCount'])
            })
        return comments, next_page_token
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    def is_going_to_state0(self, event):
        text = event.message.text
        return text.lower() == "image.show()" 
    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "我要看最新影片"
    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "來點有料的"

    def state1_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "我要玩玩看猴哥梗圖+語音包抽抽樂"
    def state2_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "我要看猴哥頻道最新影片"
    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "judge"
    def is_going_to_state4(self, event):
        text = event.message.text
        return text.lower() == "你有料"
    def is_going_to_state5(self, event):
        text = event.message.text
        return text.lower() == "你鬧"
    def state2_loop(self, event):
        text = event.message.text
        return text.lower() == "再來點有料的"
    def is_going_to_user(self,event):
        text=event.message.text
        return text.lower()=="下次一定" or text.lower()=="起飛囉" or text.lower()=="回家嘍"

    def on_enter_state0(self, event):
        id = event.source.user_id
        main()
        message_text = message.state0_menu
        reply = FlexSendMessage("主選單", message_text)
    
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        #line_bot_api.push_message(id,TextSendMessage(text=video_title))
        fsm_path="https://cdn.discordapp.com/attachments/927181929856520214/927191853005144094/fsm.png"
        line_bot_api.push_message(id, ImageSendMessage(fsm_path , fsm_path))
        line_bot_api.push_message(id,reply)

    def on_enter_state1(self, event):
        id = event.source.user_id
        main()
        message_text = message.state1_menu
        reply = FlexSendMessage("主選單", message_text)
        url=video_url[0]
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        #line_bot_api.push_message(id,TextSendMessage(text=video_title))
        line_bot_api.push_message(id,TextSendMessage(text=url))
        line_bot_api.push_message(id,reply)

    def on_enter_state2(self, event):
        id = event.source.user_id
        message_text = message.state2_menu
        reply = FlexSendMessage("主選單", message_text)

        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        num=random.randrange(0,len(image_audio_path)-3)


        line_bot_api.push_message(id, ImageSendMessage(image_audio_path[num][0] , image_audio_path[num][0]))
        line_bot_api.push_message(id, AudioSendMessage(image_audio_path[num][1],duration=15000,quick_reply=None))

        line_bot_api.push_message(id,reply)
    def on_enter_state3(self, event):
        id = event.source.user_id
        main()
        message_text = message.state3_menu
        reply = FlexSendMessage("主選單", message_text)

        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        #line_bot_api.push_message(id,TextSendMessage(text=video_title))

        line_bot_api.push_message(id, ImageSendMessage(image_audio_path[9][0] , image_audio_path[9][0]))
        line_bot_api.push_message(id, AudioSendMessage(image_audio_path[9][1],duration=15000,quick_reply=None))
        line_bot_api.push_message(id,reply)
    def on_enter_state4(self, event):
        id = event.source.user_id
        main()
        message_text = message.back_to_menu_like
        reply = FlexSendMessage("主選單", message_text)
        #url=video_url[0]
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        #line_bot_api.push_message(id,TextSendMessage(text=video_title))
        #line_bot_api.push_message(id,TextSendMessage(text=url))
        line_bot_api.push_message(id, ImageSendMessage(image_audio_path[10][0] , image_audio_path[10][0]))
        line_bot_api.push_message(id, AudioSendMessage(image_audio_path[10][1],duration=15000,quick_reply=None))
        line_bot_api.push_message(id,reply)
    def on_enter_state5(self, event):
        id = event.source.user_id
        main()
        message_text = message.back_to_menu_unlike
        reply = FlexSendMessage("主選單", message_text)
        #url=video_url[0]
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        #line_bot_api.push_message(id,TextSendMessage(text=video_title))
        #line_bot_api.push_message(id,TextSendMessage(text=url))
        line_bot_api.push_message(id, ImageSendMessage(image_audio_path[11][0] , image_audio_path[11][0]))
        line_bot_api.push_message(id, AudioSendMessage(image_audio_path[11][1],duration=15000,quick_reply=None))
        line_bot_api.push_message(id,reply)
    
    def on_enter_user(self, event):
        id = event.source.user_id
        #user_id.append(id)

        message_text = message.main_menu
        reply = FlexSendMessage("主選單", message_text)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.push_message(id,TextSendMessage(text="感謝您使用猴寶!"))
        line_bot_api.push_message(id,TextSendMessage(text="你挺消剛阿小夥子"))
        line_bot_api.push_message(id,reply)