# Step1 啟動 cockroach db: 
開啟終端機：
啟動指令：cockroach start-single-node \
  --insecure \
  --store=localdb \
  --listen-addr=localhost:26257 \
  --http-addr=localhost:8080

關閉指令：control C

使用的 --store=localdb 用來保存資料的資料夾
瀏覽器可以查看 http://localhost:8080/

# Step2 安裝相關套件
Package                Version
---------------------- -------
pip                    22.3.1
psycopg2-binary        2.9.10
setuptools             65.5.0
SQLAlchemy             2.0.41
sqlalchemy-cockroachdb 2.0.2
typing_extensions      4.13.2

# Step3 填入 input
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

# Step4 啟動服務
python3 main.py or python3 modify.py

# Step5 查看寫入資料
另開一個終端機，輸入：cockroach sql --insecure，開始可以寫sql
輸入：USE mydb
終端機呈現 root@localhost:26257/mydb>時，接下來就可以輸入相關sql去查詢是否正確寫入：SELECT * FROM users;

# 文件說明：
## db file
存放連接 db 的相關設定，勿動

## module file 
定義每個 table 的樣子

## schemas
定義狀態角色等等東西

## main.py
執行建立表格 create table 的動作，先 users/ arenas 再 activities -> arena_taken -> ticket，建立活動時會自動建立 arena_taken 和 ticket

## modify.py
執行修改的動作，如買票後更新 ticket.user_id, ticket.status，以及付款後更新 ticket.status
