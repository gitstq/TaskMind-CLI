#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TaskMind - 轻量级AI智能任务管理与时间规划引擎
Setup 配置
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="taskmind",
    version="1.0.0",
    author="TaskMind Team",
    author_email="taskmind@example.com",
    description="轻量级AI智能任务管理与时间规划引擎 | Lightweight AI Task Management & Time Planning Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/TaskMind",
    py_modules=["taskmind"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Productivity :: Task Management",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "taskmind=taskmind:main",
            "tm=taskmind:main",
        ],
    },
    extras_require={
        "tui": ["rich>=13.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords="task management, todo, ai, productivity, cli, time planning",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/TaskMind/issues",
        "Source": "https://github.com/gitstq/TaskMind",
        "Documentation": "https://github.com/gitstq/TaskMind#readme",
    },
)
