import os
import io
import pypandoc # 使用 pypandoc 调用 pandoc
# 移除了未使用的 flash, redirect, url_for, secure_filename
from flask import Flask, request, render_template, send_file
# 移除了未使用的 werkzeug.utils import
import tempfile # 新增导入 tempfile 模块
import logging # 导入 logging 用于配置

# --- 配置 ---
# 决定是否允许 .txt 文件，如果允许，取消下一行的注释
# ALLOWED_EXTENSIONS = {'md', 'markdown', 'txt'}
ALLOWED_EXTENSIONS = {'md', 'markdown'} # 只允许 Markdown 文件

app = Flask(__name__)
# 用于 flash 消息等（如果将来使用），生产环境请更换为强密钥
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-default-secret-key')

# --- 辅助函数 ---
def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 路由 ---
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    input_filename = "converted_document" # Default output name base

    if request.method == 'POST':
        markdown_content = request.form.get('markdown_content', '') # Default to empty string
        file = request.files.get('markdown_file')

        # --- 文件上传处理 ---
        if file and file.filename:
            # 使用辅助函数检查文件类型
            if allowed_file(file.filename):
                try:
                    # 使用 secure_filename 处理原始文件名，以防潜在安全问题
                    # 注意：secure_filename 可能会改变或移除中文字符，
                    # 如果需要保留原始名称，需要谨慎使用或寻找替代方案
                    # from werkzeug.utils import secure_filename # 如果需要，在此处重新导入
                    # safe_filename = secure_filename(file.filename)

                    # Read content from uploaded file
                    markdown_content = file.read().decode('utf-8')
                    # Use original filename (without extension) for output
                    input_filename = os.path.splitext(file.filename)[0]
                    app.logger.info(f"Processing uploaded file: {file.filename}")
                except UnicodeDecodeError:
                    error = "无法将上传的文件解码为 UTF-8。请确保文件是 UTF-8 编码。"
                    app.logger.error(f"UTF-8 decoding error for file: {file.filename}")
                    return render_template('index.html', error=error)
                except Exception as e:
                    error = f"读取上传文件时出错: {e}"
                    app.logger.error(f"Error reading uploaded file {file.filename}: {e}")
                    return render_template('index.html', error=error)
            else:
                # 文件类型不允许
                allowed_ext_str = ", ".join(f".{ext}" for ext in ALLOWED_EXTENSIONS)
                error = f"不允许的文件类型。请上传 {allowed_ext_str} 文件。"
                app.logger.warning(f"Disallowed file type uploaded: {file.filename}")
                return render_template('index.html', error=error)
        # --- 输入验证 ---
        # 检查是否有有效内容（来自文件或文本框，且去除首尾空格后不为空）
            # print(markdown_content.strip())
        elif not markdown_content.strip():
            error = "请输入 Markdown 内容或上传一个有效的 Markdown 文件。"
            app.logger.warning("No valid Markdown content provided (empty text area and no valid file).")
            return render_template('index.html', error=error)

        # --- Pandoc 转换逻辑 ---
        temp_output_path = None # Initialize path variable
        try:
            # 1. 创建临时文件
            # 使用 with 语句确保即使发生错误，文件句柄也会关闭
            # delete=False 使得我们可以控制删除时机
            temp_fd, temp_output_path = tempfile.mkstemp(suffix=".docx")
            os.close(temp_fd) # 关闭文件描述符，我们只需要路径，Pandoc 会自己处理文件 I/O
            app.logger.debug(f"Created temporary file for Pandoc output: {temp_output_path}")

            # 2. 调用 Pandoc 进行转换
            app.logger.info(f"Starting Pandoc conversion to docx for base name: {input_filename}")
            pypandoc.convert_text(
                source=markdown_content,
                to='docx',
                format='md',
                encoding='utf-8',
                outputfile=temp_output_path, # 告知 Pandoc 写入此文件
                # extra_args=['--reference-doc=custom-reference.docx'] # 可选参数
            )
            app.logger.info("Pandoc conversion successful.")

            # 3. 从临时文件读取内容
            app.logger.debug(f"Reading content from temporary file: {temp_output_path}")
            with open(temp_output_path, 'rb') as f:
                output_docx_content = f.read()

            # 4. 准备文件流发送给用户
            file_stream = io.BytesIO(output_docx_content)
            download_name = f'{input_filename}.docx'
            app.logger.info(f"Sending file: {download_name}")

            # 5. 发送文件
            return send_file(
                file_stream,
                as_attachment=True,
                download_name=download_name,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

        except FileNotFoundError:
             error = "Pandoc 未安装或未在系统路径 (PATH) 中找到。请确保 Pandoc 已正确安装并可从命令行执行 'pandoc --version'。"
             app.logger.error("Pandoc executable not found (FileNotFoundError).")
             return render_template('index.html', error=error)
        except RuntimeError as e:
             # Pandoc 自身运行时错误
             error = f"Pandoc 转换过程中出错: {e}"
             app.logger.error(f"Pandoc conversion RuntimeError: {e}")
             return render_template('index.html', error=error)
        except Exception as e:
            # 其他意外错误
            error = f"转换过程中发生未知错误: {e}"
            # 使用 exception 会记录完整的 traceback，非常有用
            app.logger.exception("An unexpected error occurred during conversion.")
            return render_template('index.html', error=error)
        finally:
            # 清理临时文件
            if temp_output_path and os.path.exists(temp_output_path):
                try:
                    os.remove(temp_output_path)
                    app.logger.debug(f"Removed temporary file: {temp_output_path}")
                except OSError as e:
                    # 记录删除失败，但不影响用户（文件可能已被发送）
                    app.logger.warning(f"Could not remove temporary file {temp_output_path}: {e}")

    # GET 请求或处理 POST 后出错时，显示页面
    return render_template('index.html')

# --- 运行应用 ---
if __name__ == '__main__':
    # 配置日志记录
    # 在开发环境中，DEBUG 级别可能更有用
    # 在生产环境中，INFO 或 WARNING 可能更合适
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 检查 Pandoc 可用性
    try:
        pandoc_version = pypandoc.get_pandoc_version()
        app.logger.info(f"Pandoc version {pandoc_version} found at: {pypandoc.get_pandoc_path()}")
    except OSError:
        app.logger.error("Pandoc executable not found during startup check! Conversions WILL fail. Ensure pandoc is installed and in PATH.")
        # 可以在这里选择退出应用，或者让它继续运行但转换会失败
        # import sys
        # sys.exit("Error: Pandoc not found.")

    # 运行 Flask 开发服务器
    # debug=True 会自动重载代码，并提供调试器，切勿在生产环境中使用！
    # host='0.0.0.0' 使服务器可以从网络上的其他计算机访问
    app.logger.info("Starting Flask development server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
