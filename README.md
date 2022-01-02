主題:猴哥聊天機器人<太消剛了猴寶2>   (這次有用到heroku (deploy)、網路爬蟲、image/sound/video)

為什麼會叫太消剛了猴寶"2"呢?因為原本的Line API在我測試時因為測試太多次導致用完本月次數上限，因此只好新創一個API了。

![image](https://user-images.githubusercontent.com/79431564/147877585-508ff645-59f1-4455-9318-e0c14c1bd07a.png)

設計動機與理念:由於本身偶爾會玩LOL，加上猴哥一直是我喜歡且常看的LOL遊戲主播之一，效果十足且遊戲技術很好，影片中也充滿許多笑料，因此就設計了這款包含了不少猴哥的影片中常常出現的梗的聊天機器人。

FSM圖:![image](https://user-images.githubusercontent.com/79431564/147877691-c8875f46-2147-4917-9bbf-d84653aa7203.png)

包含的元素:有用到line的內建的特殊回覆格式、以及網路爬蟲(爬youtube影片網址)、顯示圖片、播放音檔(Audio)、回覆文字等功能

各個state介紹:
user:初始的state，line bot啟動後按任意鍵就可以進入這個state，這邊可以選擇前往state0(顯示FSM圖片)、前往state1(機器人會丟給你猴哥影片頻道的最新影片連結)、前往state2(前往猴哥梗圖與語音包抽抽樂)
![image](https://user-images.githubusercontent.com/79431564/147877808-f84bbb60-ef81-4dbc-9700-bafc5b42b71a.png)


state0:顯示FSM圖片，可以按按鈕回猴寶主選單
![image](https://user-images.githubusercontent.com/79431564/147877822-454a0584-eba5-4931-b854-dc8677ae03ae.png)



state1:機器人會丟給你猴哥影片頻道的最新影片網址連結，可以選擇前往state2去抽抽樂或是前往state3去評論
![image](https://user-images.githubusercontent.com/79431564/147877912-44a4257f-3a55-4ab1-b052-d4ac2ea113df.png)


state2:機器人會隨機抽給你猴哥的梗圖+猴哥語音包(有配套過的，一個梗圖都會搭配相對應的語音)，這時可以選擇前往state1去獲取最新影片連結、重複抽取梗圖(再回state2抽一次)、或是前往state3評論
![image](https://user-images.githubusercontent.com/79431564/147877919-f040dfbf-adba-4d9a-90a4-a1d9dd57cb9c.png)



state3:可以評論，選擇讚或是倒讚，讚會前往state4,倒讚會前往state5
![image](https://user-images.githubusercontent.com/79431564/147877924-56962380-6cd4-43ff-92b9-2426cf410d19.png)


state4:因為剛剛按讚了，所以猴哥會傳好人一生平安，並且可以選擇回到猴寶的主選單
![image](https://user-images.githubusercontent.com/79431564/147877985-f6075606-74bc-4ce5-977f-74d9002f8a5d.png)


state5:因為剛剛按倒讚，所以猴哥生氣了，他會傳生氣的語音跟照片，這時可以選擇回猴寶主選單

![image](https://user-images.githubusercontent.com/79431564/147878073-c2d7524b-38bb-431b-8611-6ca4f6cf915a.png)

