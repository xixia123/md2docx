# MD2DOCX - Markdown转Word转换器 (Web 应用 🌐)

一个使用 Flask 🧪 构建的简单 Web 应用程序，它利用强大的 **Pandoc** 🪄 文档转换器将 Markdown 文本或上传的 Markdown 文件（`.md`、`.markdown`）转换为 Microsoft Word 文档（`.docx`）。

该工具提供了一个用户友好的 Web 界面 😊，方便快速进行转换。与简单的转换方法相比，它利用 Pandoc 能更好地保留 Markdown 的格式 ✨ (如表格、代码块、强调、列表等)。

## 功能特性 🚀

*   ✅ 支持直接粘贴 Markdown 文本进行转换 📋。
*   ✅ 支持上传 `.md` 或 `.markdown` 文件进行转换 ⬆️📁。
*   ✅ 使用 **Pandoc** ⚙️ 进行高质量的格式转换。
*   ✅ 生成可直接下载的 `.docx` 文件 ⬇️💾。
*   ✅ 简洁清晰的 Web 用户界面 ✨。
*   ✅ 包含基本的错误处理 ⚠️ (例如输入无效或转换失败)。
*   ✅ 自动清理转换过程中产生的临时文件 🧹。

## 技术栈 🛠️

*   **后端:** Python 3 🐍, Flask 🧪
*   **前端:** HTML, CSS 🎨
*   **转换引擎:** Pandoc 🪄 (必须单独安装)
*   **环境/包管理:** uv 📦

## 环境要求 📋

在开始之前，请确保您已满足以下要求：

1.  **Python:** 🐍 推荐使用 Python 3.8 或更高版本 (项目中的 `.python-version` 文件可能指定了具体版本)。您可以从 [python.org](https://www.python.org/) 下载或者使用`uv`直接创建python环境。
2.  **uv:** 📦 这是本项目使用的 Python 包安装和环境管理工具。
    *   **安装说明:** 请参考 `uv` 官方文档进行安装，例如使用 pipx 或 curl。
    *   **验证安装:** 运行 `uv --version`。
3.  **Pandoc:** 🪄 这是转换过程的**核心依赖**，必须安装在运行 Flask 应用的服务器或本地计算机上。
    *   **安装说明:** 请访问 Pandoc 官方安装指南：[https://pandoc.org/installing.html](https://pandoc.org/installing.html) 🔗
    *   **验证安装:** 打开终端或命令提示符，运行 `pandoc --version`。

## 安装与设置 ⚙️🚀

1.  **克隆仓库 (如果尚未下载):** <0xF0><0x9F><0xAA><0x93>
    ```bash
    git clone <你的仓库URL>
    cd MD2DOCX
    ```
    (如果已下载，请直接进入 `MD2DOCX` 目录。)

2.  **创建虚拟环境:** 🌱
    使用 `uv` 创建虚拟环境 (默认会创建名为 `.venv` 的目录):
    ```bash
    uv venv
    ```

3.  **激活虚拟环境:** ▶️
    *   **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows (Command Prompt):**
        ```bash
        .\.venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell):**
        ```bash
        .\.venv\Scripts\Activate.ps1
        ```

4.  **安装项目依赖:** 📦⬇️
    使用 `uv` 根据 `pyproject.toml` 和 `uv.lock` 文件安装依赖项：
    ```bash
    uv sync
    ```
    这将安装 Flask 等必要的库。

5.  **确保 Pandoc 已安装并添加到系统 PATH:** ✅
    再次确认 Pandoc 已正确安装，并且可以通过命令行调用（运行 `pandoc --version` 进行测试）。

## 运行应用 ▶️🔥

1.  **确保虚拟环境已激活。** (如果终端提示符前没有 `(.venv)` 字样，请重新执行激活步骤)。

2.  **启动 Flask 开发服务器:** 🚀
    ```bash
    python app.py
    ```
    或者，如果 Flask CLI 配置在 `pyproject.toml` 中，也可以尝试：
    ```bash
    uv run flask run
    ```
    (通常 `python app.py` 即可工作)。

3.  **访问应用:** 🌐👉
    打开您的网页浏览器，访问 Flask 提供的 URL (通常是 `http://127.0.0.1:5000` 或 `http://localhost:5000`)。

## 如何使用 🤔🖱️

1.  网页加载后，您有两种方式提供 Markdown 内容：
    *   **上传文件:** ⬆️ 点击“上传 Markdown 文件”下的“选择文件”（或类似按钮），从您的计算机选择一个 `.md` 或 `.markdown` 文件。
    *   **粘贴文本:** 📋 将您的 Markdown 内容直接粘贴到“直接粘贴 Markdown 内容”下的文本区域中。

2.  点击标有“**使用 Pandoc 转换并下载 Word 文档**”的按钮 ✨。

3.  **下载文件:** ⬇️
    *   如果转换成功 🎉，您的浏览器将提示您下载生成的 `.docx` 文件。
    *   如果出现错误 ❌ (例如，未提供任何输入、找不到 Pandoc、转换失败等)，页面顶部将显示错误消息。

## 文件结构 📁🌳

```
MD2DOCX/
├── .venv/             # uv 创建的虚拟环境目录 🌱
├── templates/
│   └── index.html     # Web 界面的 HTML 模板 🎨
├── .python-version    # 指定 Python 版本 (可选) 🐍
├── app.py             # 主 Flask 应用文件 🧪
├── pyproject.toml     # 项目配置与依赖项 (由 uv 使用) ⚙️
├── README.md          # 本说明文件 📖
└── uv.lock            # uv 生成的锁定文件 🔒
```

## 故障排除 ❓🛠️🆘

*   **错误：“Pandoc not found” 或类似信息:** ⚠️ 请确保 Pandoc 🪄 已正确安装，并且其安装路径已添加到您系统的 PATH 环境变量中。在终端运行 `pandoc --version` 进行测试。
*   **错误：“Permission denied”（权限不足）:** 🚫 确保应用程序对项目文件夹具有写入权限（特别是如果需要创建 `uploads/` 或 `outputs/` 目录，虽然此版本可能在内存中处理）。
*   **错误：“请输入 Markdown 内容或上传一个有效的 Markdown 文件。”:** 🤔 这表示您在未上传文件也未粘贴文本的情况下点击了转换按钮。请提供有效的输入。
*   **依赖安装问题:** 📦❓ 确保 `uv sync` 命令成功执行，没有报错。如果报错，请检查 `pyproject.toml` 文件和网络连接 🌐。