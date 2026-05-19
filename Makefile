# TaskMind - Makefile
# 轻量级AI智能任务管理与时间规划引擎

.PHONY: help install install-dev test lint format clean build run

# 默认目标
help:
	@echo "TaskMind - 轻量级AI智能任务管理与时间规划引擎"
	@echo ""
	@echo "可用命令:"
	@echo "  make install      - 安装项目"
	@echo "  make install-dev  - 安装开发依赖"
	@echo "  make test         - 运行测试"
	@echo "  make lint         - 代码检查"
	@echo "  make format       - 代码格式化"
	@echo "  make clean        - 清理构建文件"
	@echo "  make build        - 构建分发包"
	@echo "  make run          - 运行TaskMind"
	@echo "  make demo         - 运行演示"

# 安装
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# 测试
test:
	pytest tests/ -v --cov=taskmind --cov-report=html --cov-report=term

# 代码检查
lint:
	flake8 taskmind.py --max-line-length=100
	mypy taskmind.py --ignore-missing-imports

# 代码格式化
format:
	black taskmind.py --line-length=100

# 清理
clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# 构建
build: clean
	python setup.py sdist bdist_wheel

# 运行
run:
	python taskmind.py

# 演示
demo:
	@echo "🚀 TaskMind 演示模式"
	@echo ""
	@echo "1. 添加示例任务..."
	@python taskmind.py add "完成项目文档" -d "编写README和使用文档" -p high --due 2025-05-25 -t 工作,文档
	@python taskmind.py add "修复登录bug" -d "用户反馈无法登录的问题" -p critical --due 2025-05-20 -t 工作,bug
	@python taskmind.py add "学习Python新特性" -d "阅读Python 3.12文档" -p low -t 学习
	@echo ""
	@echo "2. 查看任务列表..."
	@python taskmind.py list
	@echo ""
	@echo "3. 查看今日推荐..."
	@python taskmind.py today
	@echo ""
	@echo "4. 查看统计..."
	@python taskmind.py stats
