<div align="center">

# 🧠 TaskMind

**轻量级AI智能任务管理与时间规划引擎**

*Lightweight AI Task Management & Time Planning Engine*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange)](https://github.com/gitstq/TaskMind-CLI)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey)](https://github.com/gitstq/TaskMind-CLI)

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

**TaskMind** 是一款专为开发者和效率爱好者打造的轻量级AI智能任务管理工具。它采用纯Python标准库实现，零外部依赖，单文件即可运行，帮助你在终端中高效管理任务、规划时间、提升生产力。

#### 💡 核心价值

- 🎯 **AI智能优先级排序** - 基于多维度算法自动评估任务优先级
- ⏰ **智能时间规划** - 支持截止日期管理、时间估算
- 📊 **生产力洞察** - 任务完成统计与趋势分析
- 🔄 **循环任务支持** - 支持日常、周常、月常任务
- 📝 **Markdown导出** - 一键导出任务清单，支持与其他工具同步

#### ✨ 自研差异化亮点

1. **零依赖设计** - 纯Python标准库实现，无需安装任何第三方包
2. **AI评分引擎** - 本地算法实现，无需联网，保护隐私
3. **轻量级架构** - 单文件设计，即拷即用
4. **中文原生支持** - 完美支持中文任务管理
5. **智能推荐** - 每日AI推荐任务，帮你聚焦最重要的事

---

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 🎯 **AI优先级评分** | 基于截止时间、关键词、任务年龄智能评分 | ✅ |
| 📋 **任务管理** | 增删改查、状态追踪、标签分类 | ✅ |
| ⏰ **时间规划** | 截止日期、预计耗时、循环任务 | ✅ |
| 📊 **统计洞察** | 完成率、优先级分布、本周完成数 | ✅ |
| 🔍 **智能搜索** | 支持标题、描述、标签搜索 | ✅ |
| 📝 **Markdown导出** | 导出任务清单，支持同步到其他工具 | ✅ |
| 🎨 **美观输出** | 彩色终端界面，图标丰富 | ✅ |
| 🚀 **快速启动** | 单文件运行，无需配置 | ✅ |

---

### 🚀 快速开始

#### 环境要求

- Python 3.8 或更高版本
- 任何支持Python的操作系统（Windows/macOS/Linux）

#### 安装方式

**方式一：直接运行（推荐）**

```bash
# 克隆仓库
git clone https://github.com/gitstq/TaskMind-CLI.git
cd TaskMind-CLI

# 直接运行
python taskmind.py
```

**方式二：安装到系统**

```bash
# 安装
pip install -e .

# 使用
taskmind --help
# 或简写
tm --help
```

#### 快速使用示例

```bash
# 添加任务
taskmind add "完成项目报告" -d "编写README和使用文档" -p high --due 2025-05-25 -t 工作,文档

# 查看所有任务
taskmind list

# AI智能排序查看
taskmind list --ai

# 查看今日推荐任务
taskmind today

# 完成任务
taskmind complete TMXXXXXX

# 查看统计
taskmind stats

# 导出为Markdown
taskmind export tasks.md
```

---

### 📖 详细使用指南

#### 添加任务

```bash
# 基础添加
taskmind add "任务标题"

# 完整参数
taskmind add "任务标题" \
  -d "任务描述" \
  -p critical \  # 优先级: low/medium/high/critical
  --due 2025-05-20 \  # 截止日期
  -t 标签1,标签2 \  # 标签
  -e 120  # 预计耗时(分钟)
```

#### 任务优先级说明

| 优先级 | 图标 | 说明 | AI评分权重 |
|--------|------|------|-----------|
| 🔴 Critical | 紧急 | 需要立即处理 | 40分 |
| 🟠 High | 高 | 重要任务 | 30分 |
| 🟡 Medium | 中 | 一般任务 | 20分 |
| 🟢 Low | 低 | 可延后处理 | 10分 |

#### AI评分算法

TaskMind的AI引擎综合考虑以下因素计算任务优先级（0-100分）：

1. **基础优先级** (0-40分) - 根据设定的优先级
2. **截止时间紧迫度** (0-30分) - 距离截止日期的远近
3. **关键词分析** (0-20分) - 检测紧急、重要等关键词
4. **任务年龄** (0-10分) - 任务创建时间越久分数越高

#### 常用命令速查

```bash
# 任务管理
taskmind add "标题"          # 添加任务
taskmind list               # 列出任务
taskmind list --ai          # AI排序
taskmind complete <ID>      # 完成任务
taskmind delete <ID>        # 删除任务
taskmind update <ID> -t "新标题"  # 更新任务

# 查询与导出
taskmind today              # 今日推荐
taskmind stats              # 统计信息
taskmind search "关键词"     # 搜索任务
taskmind export tasks.md    # 导出Markdown

# 筛选
taskmind list -s pending    # 只看待处理
taskmind list -p high       # 只看高优先级
```

---

### 💡 设计思路与迭代规划

#### 技术选型原因

- **纯Python标准库** - 确保零依赖，降低使用门槛
- **dataclass数据模型** - 类型安全，代码简洁
- **JSON本地存储** - 数据透明，易于备份和同步
- **argparse命令行** - 无需学习成本，符合Unix哲学

#### 后续功能迭代计划

- [ ] **时间块管理** - 番茄钟与专注时段追踪
- [ ] **习惯养成** - 连续打卡与习惯统计
- [ ] **数据同步** - Git同步、云同步支持
- [ ] **Web界面** - 可选的Web UI
- [ ] **插件系统** - 支持自定义扩展

#### 社区贡献方向

欢迎提交Issue和PR！优先关注的领域：
- 🐛 Bug修复
- 🌍 多语言支持
- 📚 文档完善
- ✨ 新功能建议

---

### 📦 打包与部署指南

#### 本地开发

```bash
# 克隆项目
git clone https://github.com/gitstq/TaskMind-CLI.git
cd TaskMind-CLI

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
make test

# 代码格式化
make format

# 代码检查
make lint
```

#### 构建分发包

```bash
# 清理并构建
make build

# 生成的文件在 dist/ 目录
```

#### 跨平台打包

```bash
# 使用PyInstaller打包单文件可执行程序
pip install pyinstaller
pyinstaller --onefile --name taskmind taskmind.py
```

---

### 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

提交规范遵循 [Conventional Commits](https://www.conventionalcommits.org/)。

---

### 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

## 繁體中文

### 🎉 專案介紹

**TaskMind** 是一款專為開發者和效率愛好者打造的輕量級AI智慧任務管理工具。它採用純Python標準庫實現，零外部依賴，單檔案即可執行，幫助你在終端機中高效管理任務、規劃時間、提升生產力。

#### ✨ 自研差異化亮點

1. **零依賴設計** - 純Python標準庫實現，無需安裝任何第三方套件
2. **AI評分引擎** - 本地演算法實現，無需連網，保護隱私
3. **輕量級架構** - 單檔案設計，即拷即用
4. **中文原生支援** - 完美支援中文任務管理
5. **智慧推薦** - 每日AI推薦任務，幫你聚焦最重要的事

---

### 🚀 快速開始

```bash
# 克隆倉庫
git clone https://github.com/gitstq/TaskMind-CLI.git
cd TaskMind-CLI

# 直接執行
python taskmind.py

# 或使用安裝模式
pip install -e .
taskmind --help
```

#### 快速使用範例

```bash
# 新增任務
taskmind add "完成專案報告" -d "編寫README和使用文件" -p high --due 2025-05-25 -t 工作,文件

# 檢視所有任務
taskmind list

# AI智慧排序檢視
taskmind list --ai

# 檢視今日推薦任務
taskmind today

# 完成任務
taskmind complete TMXXXXXX

# 檢視統計
taskmind stats
```

---

## English

### 🎉 Introduction

**TaskMind** is a lightweight AI-powered task management and time planning engine designed for developers and productivity enthusiasts. Built with pure Python standard library, zero external dependencies, single-file execution - helping you efficiently manage tasks, plan time, and boost productivity right in your terminal.

#### ✨ Key Differentiators

1. **Zero Dependencies** - Pure Python standard library, no third-party packages required
2. **AI Scoring Engine** - Local algorithm implementation, no internet needed, privacy-protected
3. **Lightweight Architecture** - Single-file design, copy-and-run
4. **Native Chinese Support** - Perfect Chinese task management support
5. **Smart Recommendations** - Daily AI-recommended tasks to help you focus on what matters most

---

### 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/gitstq/TaskMind-CLI.git
cd TaskMind-CLI

# Run directly
python taskmind.py

# Or install
pip install -e .
taskmind --help
```

#### Quick Usage Examples

```bash
# Add task
taskmind add "Complete project report" -d "Write README and docs" -p high --due 2025-05-25 -t work,docs

# List all tasks
taskmind list

# AI smart sorting
taskmind list --ai

# Today's recommended tasks
taskmind today

# Complete task
taskmind complete TMXXXXXX

# View statistics
taskmind stats

# Export to Markdown
taskmind export tasks.md
```

---

### ✨ Core Features

- 🎯 **AI Priority Scoring** - Multi-dimensional algorithm for automatic task prioritization
- 📋 **Task Management** - CRUD operations, status tracking, tag categorization
- ⏰ **Time Planning** - Due dates, time estimation, recurring tasks
- 📊 **Productivity Insights** - Completion rate, priority distribution, weekly stats
- 🔍 **Smart Search** - Search by title, description, or tags
- 📝 **Markdown Export** - Export task lists for syncing with other tools
- 🎨 **Beautiful Output** - Colorful terminal interface with rich icons
- 🚀 **Quick Start** - Single-file execution, zero configuration

---

### 📄 License

This project is licensed under the [MIT](LICENSE) License.

---

<div align="center">

Made with ❤️ by TaskMind Team

</div>
