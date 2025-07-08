# 1. 克隆项目
git clone https://github.com/hsliuping/TradingAgents-CN.git
cd TradingAgents-CN

# 2. 创建虚拟环境
python -m venv env
# Windows
env\Scripts\activate
# Linux/macOS
source env/bin/activate

# 3. 安装基础依赖
pip install -r requirements.txt

# 4. 安装A股数据支持（可选）
pip install pytdx  # 通达信API，用于A股实时数据

# 5. 安装数据库支持（可选，推荐）
pip install -r requirements_db.txt  # MongoDB + Redis 支持
# 6. 安装交易所支持（可选）
pip install -r requirements_exchanges.txt  # 支持不同交易所的API
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，配置以下必需的API密钥：
DASHSCOPE_API_KEY=your_dashscope_api_key_here
FINNHUB_API_KEY=your_finnhub_api_key_here

# 可选：Google AI API（支持Gemini模型）
GOOGLE_API_KEY=your_google_api_key_here

# 可选：数据库配置（提升性能，默认禁用）
MONGODB_ENABLED=false  # 设为true启用MongoDB
REDIS_ENABLED=false    # 设为true启用Redis
MONGODB_HOST=localhost
MONGODB_PORT=27018     # 使用非标准端口避免冲突
REDIS_HOST=localhost
REDIS_PORT=6380        # 使用非标准端口避免冲突
# OpenAI (需要科学上网)
OPENAI_API_KEY=your_openai_api_key

# Anthropic (需要科学上网)
ANTHROPIC_API_KEY=your_anthropic_api_key
# 启动 MongoDB + Redis 服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 停止服务
docker-compose down# config/database_config.py
DATABASE_CONFIG = {
    'mongodb': {
        'host': 'localhost',
        'port': 27017,
        'database': 'trading_agents',
        'username': 'admin',
        'password': 'your_password'
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'password': 'your_redis_password',
        'db': 0
    }
}📊 数据获取流程：
1. 🔍 检查 Redis 缓存 (毫秒级)
2. 📚 查询 MongoDB 存储 (秒级)
3. 🌐 调用通达信API (秒级)
4. 💾 本地文件缓存 (备用)
5. ❌ 返回错误信息# 在 .env 文件中配置
ENABLE_MONGODB=true
ENABLE_REDIS=true
ENABLE_FALLBACK=true

# 缓存过期时间（秒）
REDIS_CACHE_TTL=300
MONGODB_CACHE_TTL=3600
# MongoDB 优化
MONGODB_MAX_POOL_SIZE=50
MONGODB_MIN_POOL_SIZE=5
MONGODB_MAX_IDLE_TIME=30000

# Redis 优化
REDIS_MAX_CONNECTIONS=20
REDIS_CONNECTION_POOL_SIZE=10
REDIS_SOCKET_TIMEOUT=5# 初始化数据库
python scripts/init_database.py

# 数据库状态检查
python scripts/check_database_status.py

# 数据同步工具
python scripts/sync_stock_data.py

# 清理过期缓存
python scripts/cleanup_cache.py




