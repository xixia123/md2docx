# 使用官方 Python 镜像作为基础镜像 (选择一个你项目兼容的版本)
# slim 版本更小巧
FROM python:3.13-slim-bookworm

# 设置工作目录
WORKDIR /app

# 安装系统依赖：Pandoc 是必需的，curl 用于下载 uv
# --no-install-recommends 减少不必要的包，保持镜像大小
# 在同一层清理 apt 缓存
RUN apt-get update && \
    apt-get install -y --no-install-recommends pandoc curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安装 uv (使用官方推荐方式)
# 安装脚本会将 uv 安装到 /root/.local/bin/uv
# 安装完成后，立即将其移动到标准的 /usr/local/bin 路径下
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv
    # 如果需要 uvx, 也可添加: && mv /root/.local/bin/uvx /usr/local/bin/uvx

# 将依赖定义文件复制到工作目录
COPY pyproject.toml uv.lock ./

# 使用 uv pip install 安装项目依赖
# '.' 表示安装当前目录下的项目 (会读取 pyproject.toml)
# --system 明确指示安装到基础 Python 环境，而不是寻找虚拟环境
# --no-cache 避免在镜像中留下 uv 的缓存
# uv pip install 会优先使用 uv.lock 文件来确定版本（如果存在）
RUN uv pip install --system --no-cache .

# 将项目代码复制到工作目录
COPY . .

# 创建应用运行时需要的目录
RUN mkdir -p uploads outputs && \
    chown -R nobody:nogroup uploads outputs

# 声明容器运行时监听的端口 (Flask 默认 5000)
EXPOSE 5000

# 容器启动时运行的命令
CMD ["python", "app.py"]

# --- 可选：非 Root 用户运行 ---
# RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser
# RUN chown -R appuser:appgroup /app
# USER appuser
# CMD ["python", "app.py"]
# ----------------------------------------

