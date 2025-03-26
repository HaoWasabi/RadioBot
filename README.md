# RDO
🎧 RDO – Mang Radio vào Discord của bạn! 📻

Want to listen to the radio right in your Discord voice channel? RDO makes it easy! With just one simple command, enjoy live radio stations anytime for relaxation, entertainment, or great music.

Bạn muốn nghe radio ngay trên kênh âm thanh của server Discord? RDO sẽ giúp bạn! Chỉ với một lệnh đơn giản, bot sẽ phát trực tiếp các đài radio yêu thích, giúp bạn thư giãn, giải trí hoặc thưởng thức nhạc mọi lúc mọi nơi.


```
                    -- GCdev Solo Project --
                                                       Spring 2025
         ██████╗  ██████╗██████╗ ███████╗██╗   ██╗     + HaoWasabi
        ██╔════╝ ██╔════╝██╔══██╗██╔════╝██║   ██║     + Discord
        ██║  ███╗██║     ██║  ██║█████╗  ██║   ██║     + ChatGPT
        ██║   ██║██║     ██║  ██║██╔══╝  ╚██╗ ██╔╝     
        ╚██████╔╝╚██████╗██████╔╝███████╗ ╚████╔╝      
        ╚═════╝  ╚═════╝╚═════╝ ╚══════╝  ╚═══╝        

``` 
## Installation

1. Clone the repository.  
   Sao chép repository về máy.

2. Create a virtual environment and activate it.  
   Tạo môi trường ảo và kích hoạt nó.

3. Install dependencies:  
   Cài đặt các phụ thuộc:  
    `pip install -r requirements.txt`

4. Create a `.env` file and add the following information:  
    Tạo file `.env` và thêm thông tin sau:
```
DISCORD_TOKEN=your_bot_token_here
```

5. Run the bot:
    Chạy bot:
    `python main.py`

## **Basic slash commands / Các lệnh cơ bản**
### User commands:

- `_show`: Display detailed information of radio channels (including channel id).
Hiển thị thông tin chi tiết các kênh radio (bao gồm cả id kênh).

- `_join`: Let RDO join the Discord voice channel where you are in.
Chỉ định RDO tham gia kênh âm thanh của Discord mà bạn ở đó.

- `_play <id_channel>`: Plays the radio channel with the specified id.
Phát kênh radio có id được chỉ định.

- `_leave`: Let RDO leave the voice channel.
Chỉ định RDO rời kênh âm thanh.

- `_setcolor`: Choice default color for embed.
Chọn màu mặc định cho embed.

### Admin commands:
- `_shutdown`: Shut down bot. Tắt nguồn bot.

- `_insert`: Insert data to the database.
Thêm dữ liệu vào database.

- `_update`: Update data in the database.
Sửa dữ liệu trong database. 

- `_delete`: Delte data in the database.
Xóa dữ liệu trong database.

**Note / Lưu ý**:  
This version is not built to work in DM channels.  
Phiên bản hiện tại không được xây dựng để hoạt động ở các kênh DMChannel.

## **Other Information / Thông Tin Khác**

- **Channel**: Radio channel / Kênh radio
- **Group**: Group of channel/ Nhóm kênh radio
- **Server**: Discord's server/ Server của Discord

---

This project is designed with a focus on efficient and responsive Discord integration.  
Dự án này được thiết kế với mục tiêu tích hợp hiệu quả và đáp ứng nhanh trong môi trường Discord.
