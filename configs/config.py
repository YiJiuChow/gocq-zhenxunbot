from typing import Optional
from pathlib import Path
from .utils import ConfigsManager



# 回复消息名称
NICKNAME: str = "大头"

# 数据库（必要）
# 如果填写了bind就不需要再填写后面的字段了#）
# 示例："bind": "postgresql://user:password@127.0.0.1:5432/database"
bind: str = ""  # 数据库连接链接
sql_name: str = "postgresql"
user: str = "postgres"  # 数据用户名
password: str = "261806"  # 数据库密码
address: str = "127.0.0.1"  # 数据库地址
port: str = "5432"  # 数据库端口
database: str = "chow"  # 数据库名称

# 全局代理，例如 "http://127.0.0.1:7890"
SYSTEM_PROXY: Optional[str] = "http://127.0.0.1:7890"


Config = ConfigsManager(Path() / "data" / "configs" / "plugins2config.yaml")