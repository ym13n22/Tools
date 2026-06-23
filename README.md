# Tools 项目合集

这个仓库目前包含两个独立项目：

|项目|简介|入口|
|-|-|-|
|AI RSS Intelligence|使用 n8n、Docker 和本地 Ollama 自动抓取、筛选并总结 AI 行业 RSS，生成中文日报|[查看项目](#ai-rss-intelligence--n8n--ollama)|
|电子木鱼|Windows 桌面托盘程序，按键时播放木鱼音效，支持音量调节、暂停和直接运行 EXE|[查看项目](#电子木鱼--windows-桌面托盘程序)|

## 项目导航

* [AI RSS Intelligence — n8n + Ollama](#ai-rss-intelligence--n8n--ollama)
* [电子木鱼 — Windows 桌面托盘程序](#电子木鱼--windows-桌面托盘程序)

\---

# AI RSS Intelligence — n8n + Ollama

## 项目介绍

这是一个基于 **n8n、Docker 和本地 Ollama** 的 AI 行业资讯自动化项目。

它会定时抓取 OpenAI、Google AI、Hugging Face、NVIDIA、AWS、Microsoft、GitHub 等来源的 RSS，使用本地模型筛选高价值新闻、抓取正文并生成中文分析，最后通过邮件发送日报。

适合用于：

* AI 新闻自动收集
* 产品与竞品情报筛选
* Agent、Workflow、API、模型能力跟踪
* 企业 AI 落地与行业动态观察

## 实现方式

整体流程：

```text
定时触发
→ 抓取 RSS
→ 解析 XML
→ 筛选最近 7 天文章
→ Ollama 初步评分
→ 抓取高价值文章正文
→ Ollama 深度分析
→ 汇总中文日报
→ 邮件发送
```

项目主要组件：

* **n8n**：工作流编排
* **Docker**：运行 n8n
* **Ollama**：本地模型推理
* **qwen3:8b**：新闻评分与深度分析
* **r.jina.ai**：提取网页正文
* **SQLite**：保存 n8n 运行数据

默认配置：

```text
时区：Europe/London
筛选范围：最近 7 天
每个 RSS 最多处理：20 篇
模型：qwen3:8b
n8n 地址：http://localhost:5678
```

## 运行方法

### 1\. 安装环境

需要安装：

* Git
* Docker Desktop
* Ollama

### 2\. 克隆项目

```bash
git clone https://github.com/ym13n22/Tools.git
cd Tools/newsFatch/n8n
```

### 3\. 安装模型

```bash
ollama pull qwen3:8b
```

确认 Ollama 正常运行：

```bash
ollama list
```

### 4\. 启动 n8n

```bash
docker compose up -d
```

浏览器打开：

```text
http://localhost:5678
```

### 5\. 导入工作流

在 n8n 中导入：

```text
workflows/My workflow.json
```

然后：

1. 配置 SMTP 邮箱凭据
2. 检查 Ollama 地址
3. 手动执行一次
4. 确认正常后激活工作流

Ollama 地址应为：

```text
http://host.docker.internal:11434/api/generate
```

## 常用命令

启动：

```bash
docker compose up -d
```

停止：

```bash
docker compose down
```

查看日志：

```bash
docker compose logs -f n8n
```

重启：

```bash
docker compose restart n8n
```

# 电子木鱼 — Windows 桌面托盘程序

## 项目介绍

这是一个可直接运行的 Windows 电子木鱼程序。

程序会在后台监听键盘按键，每次按键时播放木鱼音效，并通过系统托盘提供音量调节、暂停和退出功能。

适合用于：

* 打字时自动播放木鱼声音
* 后台常驻运行
* 快捷键调节音量
* 托盘控制程序状态

## 实现方式

整体流程：

```text
监听键盘按键
→ 检查暂停状态
→ 检查冷却时间
→ 播放木鱼音效
→ 托盘控制音量、暂停和退出
```

主要组件：

* **keyboard**：全局键盘监听
* **pygame**：播放木鱼音效
* **pystray**：系统托盘菜单
* **Pillow**：生成托盘图标
* **Tkinter**：音量调节窗口

默认配置：

```text
基础音量：0.5
用户音量倍率：0.0～2.0
按键冷却：0.05 秒
音量增加：Ctrl + ↑
音量降低：Ctrl + ↓
```

## 运行方法

项目已经提供打包好的 Windows EXE，不需要安装 Python，也不需要安装依赖。

下载或克隆项目后，直接运行：

```text
muyu.exe
```

启动后：

```text
任意按键：播放木鱼声音
Ctrl + ↑：提高音量
Ctrl + ↓：降低音量
```

右键点击系统托盘中的木鱼图标，可以：

* 调节音量
* 暂停或继续
* 退出程序

如果 Windows 显示安全提醒，请确认文件来自本项目后再运行。

## 项目文件

```text
muyu/
├── muyu.exe          # 可直接运行
├── muyu.py           # 源代码
└──muyu.mp3          # 木鱼音效
```

如果 EXE 已经将音频打包到程序内部，只需要保留 `muyu.exe` 即可运行。

如果 EXE 使用外部音频文件，则需要将 `muyu.mp3` 与 `muyu.exe` 放在同一目录。

## 开发与重新打包

普通用户不需要执行这一部分。

安装依赖：

```bash
pip install pygame keyboard pystray pillow pyinstaller
```

运行源码：

```bash
python muyu.py
```

重新打包：

```bash
pyinstaller --onefile --noconsole --add-data "muyu.mp3;." muyu.py
```

生成文件位于：

```text
dist/muyu.exe
```

## 注意事项

* 程序仅支持 Windows
* 全局键盘监听在部分电脑上可能需要管理员权限
* 安全软件可能提示键盘监听行为
* 程序只监听按键事件，不保存或上传输入内容
* 如果没有声音，请检查系统音量和音频输出设备

