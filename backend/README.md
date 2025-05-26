# Instruction

## Step1 Run 上一層的 docker compose

參考上一層 Readme

## Step2 安裝相關套件(非必要，但方便開發時有提示)

Package                Version
---------------------- -------
pip                    22.3.1
psycopg2-binary        2.9.10
setuptools             65.5.0
SQLAlchemy             2.0.41
sqlalchemy-cockroachdb 2.0.2
typing_extensions      4.13.2

## Step3 填入 input

看到 ##################### 請修改你需要的input ###################### 時，請根據功能修改你要的參數
範例：如果要建立users這個table，需要修改功能

func = "create table"
sub_func = create user

並取消user的相關輸入的註解，賦值給參數

user 輸入：
email = "alex@example.com"
username = "alex"
password = "alexalex"
role = UserRole.CLIENT
phone_number = "0999654738"

同時註解 arena 輸入和 activity 輸入

## 文件說明

### api_doc folder

定義 route 文件

### crud folder

DB logic

### routes folder

Route implement

### db folder

存放連接 db 的相關設定，勿動

### Models folder

定義每個 table 的樣子

### schemas folder

定義狀態角色等等東西

### main.py

執行建立表格 create table 的動作，先 users/ arenas 再 activities -> arena_taken -> ticket，建立活動時會自動建立 arena_taken 和 ticket

### modify.py

執行修改的動作，如買票後更新 ticket.user_id, ticket.status，以及付款後更新 ticket.status
