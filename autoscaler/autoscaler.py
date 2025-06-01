#!/usr/bin/env python3
"""
Docker Compose Auto-scaler
監控 Nginx 請求量並自動調整 Flask 應用實例數量
"""

import os
import time
import json
import logging
import requests
import docker
from datetime import datetime, timedelta
from typing import Dict, List
import tarfile
from io import BytesIO

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def copy_to_container(container_name, src_path, dst_path):
    # 初始化 Docker 客戶端
    client = docker.from_env()
    
    try:
        # 取得容器物件
        container = client.containers.get(container_name)
        
        # 確認來源檔案存在
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"來源檔案 {src_path} 不存在")
        
        # 建立 tar 檔案
        tar_stream = BytesIO()
        with tarfile.open(fileobj=tar_stream, mode='w') as tar:
            # 將檔案加入 tar
            tar.add(src_path, arcname=os.path.basename(src_path))
        
        # 將 tar 流定位到開頭
        tar_stream.seek(0)
        
        # 將檔案複製到容器中的目標路徑
        # put_archive expects a directory path, so we use the parent directory
        target_dir = os.path.dirname(dst_path)
        container.put_archive(
            path=target_dir,
            data=tar_stream.getvalue()
        )
        logger.info(f"成功將 {src_path} 複製到容器 {container_name} 的 {dst_path}")
        
    except docker.errors.APIError as e:
        logger.error(f"Docker API 錯誤: {e.explanation}")
    except Exception as e:
        logger.error(f"複製檔案到容器時發生錯誤: {e}")
class AutoScaler:
    def __init__(self):
        # 環境變數配置
        self.prometheus_url = os.getenv('PROMETHEUS_URL', 'http://prometheus:9090')
        self.max_instances = int(os.getenv('MAX_INSTANCES', '5'))
        self.min_instances = int(os.getenv('MIN_INSTANCES', '2'))
        self.scale_up_threshold = int(os.getenv('SCALE_UP_THRESHOLD', '100'))
        self.scale_down_threshold = int(os.getenv('SCALE_DOWN_THRESHOLD', '20'))
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '10'))
        
        # Docker 客戶端
        self.docker_client = docker.from_env()
        
        # 當前實例追蹤
        self.current_instances = []
        self.last_scale_time = datetime.now()
        self.cooldown_period = timedelta(minutes=1)  # 冷卻期間，避免頻繁擴縮容
        
    def get_request_rate(self) -> float:
        """從 Prometheus 獲取 Nginx 請求速率"""
        try:
            # 查詢最近1分鐘的請求速率 (requests/second)
            query = 'rate(nginx_http_requests_total[1m]) * 60'  # 轉換為 requests/minute
            
            response = requests.get(
                f'{self.prometheus_url}/api/v1/query',
                params={'query': query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success' and data['data']['result']:
                    # 取所有實例的請求率總和
                    total_rate = sum(
                        float(result['value'][1]) 
                        for result in data['data']['result']
                    )
                    return total_rate
            
            logger.warning(f"Failed to get metrics from Prometheus: {response.status_code}")
            return 0.0
            
        except Exception as e:
            logger.error(f"Error getting request rate: {e}")
            return 0.0
    
    def get_current_flask_instances(self) -> List[str]:
        """獲取當前運行的 Flask 實例"""
        try:
            containers = self.docker_client.containers.list(
                filters={
                    'name': f'flask_app',
                    'status': 'running'
                         }
            )
            return sorted([c.name for c in containers])
        except Exception as e:
            logger.error(f"Error getting current instances: {e}")
            return []
    
    def scale_up(self) -> bool:
        """擴容 - 增加一個 Flask 實例"""
        try:
            current_instances = self.get_current_flask_instances()
            current_count = len(current_instances)

            if current_count >= self.max_instances:
                logger.info(f"Already at max instances ({self.max_instances})")
                return False
            
            # 生成新的實例編號
            existing_numbers = []
            for instance in current_instances:
                try:
                    # 從 flask_app3 這樣的名稱中提取數字
                    num = int(instance.replace('flask_app', ''))
                    existing_numbers.append(num)
                except ValueError:
                    continue
            
            # 找到下一個可用的編號
            new_instance_num = max(existing_numbers) + 1 if existing_numbers else 3
            
            container_name = f'flask_app{new_instance_num}'
            
            # 選擇要連接的 CockroachDB 節點 (輪流選擇)
            crdb_node = f'crdb{(new_instance_num % 3) + 1}'
            
            logger.info(f"Creating new Flask instance: {container_name}")
            
            # 創建新的 Flask 容器
            try:
                container = self.docker_client.containers.get(container_name)
                logger.info(f"Container {container_name} already exists, removing it")
                container.stop()
                container.remove()
            except docker.errors.NotFound:
                logger.info(f"Container {container_name} does not exist, creating new one")
            except Exception as e:
                logger.error(f"Error checking container {container_name}: {e}")
                return False

            container = self.docker_client.containers.run(
                image='final_project-flask_app:latest',
                name=container_name,
                environment={
                    'DATABASE_URL': f'postgresql://root@{crdb_node}:26257/defaultdb?sslmode=disable',
                    'FLASK_APP': 'main.py',
                    'FLASK_ENV': 'development',
                    'FLASK_DEBUG': '1'
                },
                entrypoint=["/bin/bash", "-c", "flask run --host=0.0.0.0 --port=8000"],
                network=f'mynetwork',
                detach=True,
            )
            
            # 等待容器啟動並健康檢查
            for i in range(10):  # 最多等待 10 秒
                time.sleep(1)
                logger.info(f"Waiting for container {container_name} to start...")
                container.reload()
                if container.status == 'running':
                    # 簡單的健康檢查
                    try:
                        health_check = container.exec_run('curl -f http://localhost:8000/health', timeout=2)
                        if health_check.exit_code == 0:
                            break
                    except:
                        continue
            
            if container.status != 'running':
                logger.error(f"Container {container_name} failed to start properly")
                return False
            
            # 更新 Nginx 配置以包含新實例
            if self.update_nginx_upstream():
                logger.info(f"Successfully scaled up: Added {container_name}")
                return True
            else:
                logger.error("Failed to update Nginx configuration, removing container")
                container.stop()
                container.remove()
                return False
            
        except Exception as e:
            logger.error(f"Error scaling up: {e}")
            return False
    
    def scale_down(self) -> bool:
        """縮容 - 移除一個 Flask 實例"""
        try:
            current_instances = self.get_current_flask_instances()
            if len(current_instances) <= self.min_instances:
                logger.info(f"Already at min instances ({self.min_instances})")
                return False
            
            # 找到編號最大的實例來移除 (避免移除基礎實例)
            instance_numbers = []
            for instance in current_instances:
                try:
                    # 從 flask_app3 這樣的名稱中提取數字
                    num = int(instance.replace('flask_app', ''))
                    instance_numbers.append(num)
                except ValueError:
                    continue
            
            if not instance_numbers:
                logger.error("No scalable instances found")
                return False
            
            # 選擇編號最大的實例移除
            instance_numbers.sort(reverse=True)
            instance_to_remove = f'flask_app{instance_numbers[0]}'  # 修正：直接使用最大編號構造容器名稱
            
            logger.info(f"Removing Flask instance: {instance_to_remove}")
            
            container = self.docker_client.containers.get(instance_to_remove)
            
            # 優雅停止容器
            container.stop(timeout=10)
            container.remove()
            
            # 更新 Nginx 配置
            if self.update_nginx_upstream():
                logger.info(f"Successfully scaled down: Removed {instance_to_remove}")
                return True
            else:
                logger.error("Failed to update Nginx configuration after scaling down")
                return False
            
        except Exception as e:
            logger.error(f"Error scaling down: {e}")
            return False
    
    def update_nginx_upstream(self):
        """更新 Nginx upstream 配置並重新載入"""
        try:
            logger.info("Updating Nginx upstream configuration")
            nginx_container = self.docker_client.containers.get(f'nginx_proxy')
            
            # 獲取當前所有 Flask 實例
            current_instances = self.get_current_flask_instances()
            logger.info(f"Current Flask instances: {current_instances}")
            # 生成新的 upstream 配置
            upstream_servers = []
            for instance in current_instances:
                upstream_servers.append(f'        server {instance}:8000 max_fails=3 fail_timeout=30s;')
                logger.info(f"Adding upstream server: {instance}:8000")
            # 生成完整的 nginx 配置
            nginx_config = f"""worker_processes auto;

events {{
    worker_connections 1024;
}}

http {{
    log_format detailed '$remote_addr - $remote_user [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent" '
                       'rt=$request_time uct="$upstream_connect_time" '
                       'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log detailed;
    error_log /var/log/nginx/error.log warn;

    upstream flaskapi_backend {{
        least_conn;
{chr(10).join(upstream_servers)}
    }}


    server {{
        listen 80;
        server_name localhost;

        location /health {{
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }}

        location /nginx_status {{
            stub_status on;
            access_log off;
            allow 127.0.0.1;
            allow 10.0.0.0/8;
            allow 172.16.0.0/12;
            allow 192.168.0.0/16;
            deny all;
        }}

        location /api/ {{
            
            proxy_pass http://flaskapi_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_next_upstream_tries 2;
        }}

        location / {{
            
            proxy_pass http://flaskapi_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
                        
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
            proxy_next_upstream_tries 2;
        }}

        location /cdbadmin/ {{
            proxy_pass http://crdb1:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}

        error_page 502 503 504 /50x.html;
        location = /50x.html {{
            return 503 '{{"error": "Service temporarily unavailable"}}';
            add_header Content-Type application/json;
        }}
    }}
}}"""

            # 寫入新配置到容器內
            logger.info("New nginx configuration content:")
            logger.info(nginx_config)
            # 先在 local 建立 nginx.conf.tmp, 再 copy 到容器內
            with open('/tmp/nginx.conf', 'w') as f:
                f.write(nginx_config)
            # Rename the copied file to the correct name
            copy_to_container('nginx_proxy', '/tmp/nginx.conf', '/etc/nginx/nginx.conf')
            test_result = nginx_container.exec_run('nginx -t -c /etc/nginx/nginx.conf')
            if test_result.exit_code != 0:
                logger.error(f"Nginx config test failed: {test_result.output.decode()}")
                return False
            
            # 重新載入 Nginx
            reload_result = nginx_container.exec_run('nginx -s reload -c /etc/nginx/nginx.conf')
            logger.info(f"Nginx reload command output: {reload_result.output.decode()}")
            if reload_result.exit_code == 0:
                logger.info(f"Nginx reloaded successfully with {len(upstream_servers)} servers")
                return True
            else:
                logger.error(f"Nginx reload failed: {reload_result.output.decode()}")
                return False
            
        except Exception as e:
            logger.error(f"Error updating nginx upstream: {e}")
            return False
    
    def should_scale(self, current_rate: float) -> str:
        """判斷是否需要擴縮容"""
        now = datetime.now()
        
        # 檢查冷卻期
        if now - self.last_scale_time < self.cooldown_period:
            return 'cooldown'
        
        current_count = len(self.get_current_flask_instances())
        
        # 擴容條件
        if current_rate > self.scale_up_threshold and current_count < self.max_instances:
            return 'scale_up'
        
        # 縮容條件
        if current_rate < self.scale_down_threshold and current_count > self.min_instances:
            return 'scale_down'
        
        return 'no_action'
    
    def run(self):
        """主要監控循環"""
        logger.info("Auto-scaler started")
        logger.info(f"Config: min={self.min_instances}, max={self.max_instances}")
        logger.info(f"Thresholds: up={self.scale_up_threshold}, down={self.scale_down_threshold}")
        
        while True:
            try:
                # 獲取當前請求率
                request_rate = self.get_request_rate()
                current_instances = len(self.get_current_flask_instances())
                
                logger.info(f"Request rate: {request_rate:.1f} req/min, Instances: {current_instances}")
                
                # 判斷是否需要擴縮容
                action = self.should_scale(request_rate)
                logger.info(f"Scaling decision: {action}")
                if action == 'scale_up':
                    if self.scale_up():
                        self.last_scale_time = datetime.now()
                        logger.info("Scaled up successfully")
                elif action == 'scale_down':
                    # logger.info("Scaling down not implemented yet")
                    if self.scale_down():
                        self.last_scale_time = datetime.now()
                        logger.info("Scaled down successfully")
                elif action == 'cooldown':
                    logger.debug("In cooldown period, skipping scaling decision")
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("Shutting down auto-scaler")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(self.check_interval)

if __name__ == '__main__':
    scaler = AutoScaler()
    scaler.run()
