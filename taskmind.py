#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TaskMind - 轻量级AI智能任务管理与时间规划引擎
Lightweight AI Task Management & Time Planning Engine

Author: TaskMind Team
License: MIT
Version: 1.0.0
"""

import json
import os
import re
import sys
import argparse
import datetime
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from enum import Enum

__version__ = "1.0.0"
__author__ = "TaskMind Team"


class Priority(Enum):
    """任务优先级枚举"""
    CRITICAL = 4  # 紧急且重要
    HIGH = 3      # 重要
    MEDIUM = 2    # 一般
    LOW = 1       # 低优先级


class Status(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """任务数据模型"""
    id: str
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    estimated_minutes: int = 0
    actual_minutes: int = 0
    parent_id: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    recurrence: Optional[str] = None  # daily, weekly, monthly
    ai_score: float = 0.0  # AI优先级评分

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """从字典创建"""
        data = data.copy()
        data['priority'] = Priority(data.get('priority', 2))
        data['status'] = Status(data.get('status', 'pending'))
        return cls(**data)

    @property
    def priority_name(self) -> str:
        """获取优先级名称"""
        names = {
            Priority.CRITICAL: "🔴 紧急",
            Priority.HIGH: "🟠 高",
            Priority.MEDIUM: "🟡 中",
            Priority.LOW: "🟢 低"
        }
        return names.get(self.priority, "🟡 中")

    @property
    def status_icon(self) -> str:
        """获取状态图标"""
        icons = {
            Status.PENDING: "⏳",
            Status.IN_PROGRESS: "🔄",
            Status.COMPLETED: "✅",
            Status.CANCELLED: "❌"
        }
        return icons.get(self.status, "⏳")


class TaskStore:
    """任务数据存储管理"""

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            home = Path.home()
            self.data_dir = home / ".taskmind"
        else:
            self.data_dir = Path(data_dir)
        self.data_file = self.data_dir / "tasks.json"
        self.config_file = self.data_dir / "config.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """确保数据目录存在"""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_tasks(self) -> List[Task]:
        """加载所有任务"""
        if not self.data_file.exists():
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task.from_dict(t) for t in data.get('tasks', [])]
        except (json.JSONDecodeError, IOError):
            return []

    def save_tasks(self, tasks: List[Task]):
        """保存所有任务"""
        data = {
            'version': __version__,
            'updated_at': datetime.datetime.now().isoformat(),
            'tasks': [t.to_dict() for t in tasks]
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if not self.config_file.exists():
            return self._default_config()
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._default_config()

    def save_config(self, config: Dict[str, Any]):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            'version': __version__,
            'default_priority': 2,
            'ai_enabled': True,
            'time_block_minutes': 25,  # 默认番茄钟时长
            'theme': 'default'
        }


class AIPriorityEngine:
    """AI优先级评分引擎 - 纯本地算法实现"""

    def __init__(self):
        self.keywords_urgent = [
            '紧急', 'urgent', 'asap', '马上', '立即', '今天', 'deadline',
            '截止', '过期', 'expired', '重要', 'important', 'critical',
            'bug', '错误', '故障', '修复', 'fix'
        ]
        self.keywords_high = [
            '高', 'high', '优先', 'priority', '尽快', 'soon',
            '计划', 'plan', '准备', 'prepare'
        ]
        self.keywords_low = [
            '低', 'low', '稍后', 'later', '随便', 'maybe',
            '考虑', 'consider', '想', 'think'
        ]

    def calculate_score(self, task: Task) -> float:
        """
        计算任务优先级评分 (0-100)
        综合考虑多个因素
        """
        score = 0.0

        # 1. 基础优先级分数 (0-40分)
        priority_scores = {
            Priority.CRITICAL: 40,
            Priority.HIGH: 30,
            Priority.MEDIUM: 20,
            Priority.LOW: 10
        }
        score += priority_scores.get(task.priority, 20)

        # 2. 截止时间紧迫度 (0-30分)
        if task.due_date:
            try:
                due = datetime.datetime.fromisoformat(task.due_date)
                now = datetime.datetime.now()
                hours_until_due = (due - now).total_seconds() / 3600

                if hours_until_due < 0:
                    score += 30  # 已过期，最高紧迫度
                elif hours_until_due < 24:
                    score += 25  # 24小时内
                elif hours_until_due < 72:
                    score += 20  # 3天内
                elif hours_until_due < 168:
                    score += 15  # 一周内
                elif hours_until_due < 720:
                    score += 10  # 一个月内
                else:
                    score += 5   # 还有很长时间
            except (ValueError, TypeError):
                pass

        # 3. 关键词分析 (0-20分)
        text = f"{task.title} {task.description}".lower()
        urgent_count = sum(1 for kw in self.keywords_urgent if kw in text)
        high_count = sum(1 for kw in self.keywords_high if kw in text)
        low_count = sum(1 for kw in self.keywords_low if kw in text)

        keyword_score = min(urgent_count * 5 + high_count * 2 - low_count * 2, 20)
        score += max(keyword_score, 0)

        # 4. 任务年龄 (0-10分)
        try:
            created = datetime.datetime.fromisoformat(task.created_at)
            age_days = (datetime.datetime.now() - created).days
            if age_days > 30:
                score += 10  # 超过一个月未处理
            elif age_days > 14:
                score += 7
            elif age_days > 7:
                score += 5
            elif age_days > 3:
                score += 2
        except (ValueError, TypeError):
            pass

        return min(score, 100)

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """按AI评分排序任务"""
        for task in tasks:
            task.ai_score = self.calculate_score(task)

        # 按AI评分降序，然后按截止时间升序
        return sorted(tasks, key=lambda t: (-t.ai_score, t.due_date or '9999'))


class TaskManager:
    """任务管理核心类"""

    def __init__(self, store: Optional[TaskStore] = None):
        self.store = store or TaskStore()
        self.ai_engine = AIPriorityEngine()
        self._tasks: List[Task] = []
        self._load()

    def _load(self):
        """加载任务"""
        self._tasks = self.store.load_tasks()

    def _save(self):
        """保存任务"""
        self.store.save_tasks(self._tasks)

    def _generate_id(self) -> str:
        """生成唯一ID"""
        timestamp = datetime.datetime.now().isoformat()
        random_str = hashlib.md5(timestamp.encode()).hexdigest()[:8]
        return f"TM{random_str.upper()}"

    def add(self, title: str, **kwargs) -> Task:
        """添加新任务"""
        task = Task(
            id=self._generate_id(),
            title=title,
            **kwargs
        )
        self._tasks.append(task)
        self._save()
        return task

    def get(self, task_id: str) -> Optional[Task]:
        """获取单个任务"""
        for task in self._tasks:
            if task.id == task_id or task.id.lower().endswith(task_id.lower()):
                return task
        return None

    def update(self, task_id: str, **kwargs) -> Optional[Task]:
        """更新任务"""
        task = self.get(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            self._save()
        return task

    def delete(self, task_id: str) -> bool:
        """删除任务"""
        task = self.get(task_id)
        if task:
            self._tasks.remove(task)
            self._save()
            return True
        return False

    def complete(self, task_id: str) -> Optional[Task]:
        """完成任务"""
        task = self.get(task_id)
        if task:
            task.status = Status.COMPLETED
            task.completed_at = datetime.datetime.now().isoformat()
            self._save()
        return task

    def list_tasks(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        tag: Optional[str] = None,
        ai_sort: bool = False
    ) -> List[Task]:
        """列出任务"""
        tasks = self._tasks.copy()

        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        if tag:
            tasks = [t for t in tasks if tag in t.tags]

        if ai_sort:
            tasks = self.ai_engine.sort_tasks(tasks)
        else:
            # 默认按创建时间倒序
            tasks.sort(key=lambda t: t.created_at, reverse=True)

        return tasks

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = len(self._tasks)
        completed = len([t for t in self._tasks if t.status == Status.COMPLETED])
        pending = len([t for t in self._tasks if t.status == Status.PENDING])
        in_progress = len([t for t in self._tasks if t.status == Status.IN_PROGRESS])

        # 本周完成的任务
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        completed_this_week = len([
            t for t in self._tasks
            if t.status == Status.COMPLETED
            and t.completed_at
            and datetime.datetime.fromisoformat(t.completed_at) > week_ago
        ])

        # 即将到期（3天内）
        three_days_later = datetime.datetime.now() + datetime.timedelta(days=3)
        due_soon = len([
            t for t in self._tasks
            if t.status != Status.COMPLETED
            and t.due_date
            and datetime.datetime.fromisoformat(t.due_date) < three_days_later
        ])

        # 优先级分布
        priority_dist = {}
        for p in Priority:
            priority_dist[p.name] = len([t for t in self._tasks if t.priority == p])

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'completion_rate': round(completed / total * 100, 1) if total > 0 else 0,
            'completed_this_week': completed_this_week,
            'due_soon': due_soon,
            'priority_distribution': priority_dist
        }

    def export_markdown(self, filepath: str, status: Optional[Status] = None):
        """导出为Markdown"""
        tasks = self.list_tasks(status=status)

        lines = [
            "# TaskMind 任务清单",
            "",
            f"> 导出时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> 总任务数: {len(tasks)}",
            "",
            "## 任务列表",
            ""
        ]

        for task in tasks:
            status_icon = task.status_icon
            priority_text = task.priority_name
            due_text = f" (截止: {task.due_date[:10]})" if task.due_date else ""
            tags_text = f" [{', '.join(task.tags)}]" if task.tags else ""

            lines.append(f"- {status_icon} **{task.title}** {priority_text}{due_text}{tags_text}")
            if task.description:
                lines.append(f"  - {task.description}")
            lines.append("")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def get_today_focus(self) -> List[Task]:
        """获取今日专注任务（AI推荐）"""
        pending = self.list_tasks(status=Status.PENDING)
        in_progress = self.list_tasks(status=Status.IN_PROGRESS)

        all_active = pending + in_progress
        if not all_active:
            return []

        # AI排序后取前5个
        sorted_tasks = self.ai_engine.sort_tasks(all_active)
        return sorted_tasks[:5]


class TaskMindCLI:
    """命令行界面"""

    def __init__(self):
        self.manager = TaskManager()

    def run(self, args=None):
        """运行CLI"""
        parser = argparse.ArgumentParser(
            prog='taskmind',
            description='TaskMind - 轻量级AI智能任务管理与时间规划引擎',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例:
  taskmind add "完成项目报告" -p high -d "2025-05-20" -t 工作,紧急
  taskmind list
  taskmind complete TM123456
  taskmind today
  taskmind stats
            """
        )
        parser.add_argument('--version', action='version', version=f'TaskMind {__version__}')

        subparsers = parser.add_subparsers(dest='command', help='可用命令')

        # add 命令
        add_parser = subparsers.add_parser('add', help='添加新任务')
        add_parser.add_argument('title', help='任务标题')
        add_parser.add_argument('-d', '--description', help='任务描述')
        add_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high', 'critical'],
                               default='medium', help='优先级')
        add_parser.add_argument('--due', help='截止日期 (YYYY-MM-DD)')
        add_parser.add_argument('-t', '--tags', help='标签 (逗号分隔)')
        add_parser.add_argument('-e', '--estimate', type=int, help='预计耗时(分钟)')

        # list 命令
        list_parser = subparsers.add_parser('list', help='列出任务')
        list_parser.add_argument('-s', '--status', choices=['pending', 'in_progress', 'completed'],
                                help='按状态筛选')
        list_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high', 'critical'],
                                help='按优先级筛选')
        list_parser.add_argument('--ai', action='store_true', help='AI智能排序')

        # complete 命令
        complete_parser = subparsers.add_parser('complete', help='完成任务')
        complete_parser.add_argument('task_id', help='任务ID')

        # delete 命令
        delete_parser = subparsers.add_parser('delete', help='删除任务')
        delete_parser.add_argument('task_id', help='任务ID')

        # update 命令
        update_parser = subparsers.add_parser('update', help='更新任务')
        update_parser.add_argument('task_id', help='任务ID')
        update_parser.add_argument('-t', '--title', help='新标题')
        update_parser.add_argument('-d', '--description', help='新描述')
        update_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high', 'critical'],
                                  help='新优先级')

        # today 命令
        subparsers.add_parser('today', help='查看今日推荐任务')

        # stats 命令
        subparsers.add_parser('stats', help='查看统计信息')

        # export 命令
        export_parser = subparsers.add_parser('export', help='导出任务')
        export_parser.add_argument('filepath', help='导出文件路径')
        export_parser.add_argument('-s', '--status', choices=['pending', 'in_progress', 'completed'],
                                  help='按状态筛选')

        # search 命令
        search_parser = subparsers.add_parser('search', help='搜索任务')
        search_parser.add_argument('keyword', help='搜索关键词')

        parsed_args = parser.parse_args(args)

        if not parsed_args.command:
            parser.print_help()
            return

        self._handle_command(parsed_args)

    def _handle_command(self, args):
        """处理命令"""
        if args.command == 'add':
            self._cmd_add(args)
        elif args.command == 'list':
            self._cmd_list(args)
        elif args.command == 'complete':
            self._cmd_complete(args)
        elif args.command == 'delete':
            self._cmd_delete(args)
        elif args.command == 'update':
            self._cmd_update(args)
        elif args.command == 'today':
            self._cmd_today()
        elif args.command == 'stats':
            self._cmd_stats()
        elif args.command == 'export':
            self._cmd_export(args)
        elif args.command == 'search':
            self._cmd_search(args)

    def _cmd_add(self, args):
        """添加任务"""
        priority_map = {
            'low': Priority.LOW,
            'medium': Priority.MEDIUM,
            'high': Priority.HIGH,
            'critical': Priority.CRITICAL
        }

        kwargs = {
            'description': args.description or '',
            'priority': priority_map.get(args.priority, Priority.MEDIUM),
            'estimated_minutes': args.estimate or 0
        }

        if args.due:
            kwargs['due_date'] = f"{args.due}T23:59:59"

        if args.tags:
            kwargs['tags'] = [t.strip() for t in args.tags.split(',')]

        task = self.manager.add(args.title, **kwargs)

        print(f"✅ 任务已添加!")
        print(f"   ID: {task.id}")
        print(f"   标题: {task.title}")
        print(f"   优先级: {task.priority_name}")
        if task.due_date:
            print(f"   截止: {task.due_date[:10]}")

    def _cmd_list(self, args):
        """列出任务"""
        status_map = {
            'pending': Status.PENDING,
            'in_progress': Status.IN_PROGRESS,
            'completed': Status.COMPLETED
        }
        priority_map = {
            'low': Priority.LOW,
            'medium': Priority.MEDIUM,
            'high': Priority.HIGH,
            'critical': Priority.CRITICAL
        }

        status = status_map.get(args.status) if args.status else None
        priority = priority_map.get(args.priority) if args.priority else None

        tasks = self.manager.list_tasks(
            status=status,
            priority=priority,
            ai_sort=args.ai
        )

        if not tasks:
            print("📭 没有找到任务")
            return

        print(f"\n📋 任务列表 (共 {len(tasks)} 个)\n")
        print(f"{'ID':<12} {'状态':<4} {'优先级':<8} {'标题':<30} {'截止日期':<12}")
        print("-" * 70)

        for task in tasks:
            due = task.due_date[:10] if task.due_date else '-'
            title = task.title[:28] + '..' if len(task.title) > 30 else task.title
            print(f"{task.id:<12} {task.status_icon:<4} {task.priority_name:<8} {title:<30} {due:<12}")

        if args.ai:
            print("\n💡 已按AI智能优先级排序")

    def _cmd_complete(self, args):
        """完成任务"""
        task = self.manager.complete(args.task_id)
        if task:
            print(f"✅ 任务已完成: {task.title}")
        else:
            print(f"❌ 未找到任务: {args.task_id}")

    def _cmd_delete(self, args):
        """删除任务"""
        if self.manager.delete(args.task_id):
            print(f"🗑️ 任务已删除")
        else:
            print(f"❌ 未找到任务: {args.task_id}")

    def _cmd_update(self, args):
        """更新任务"""
        kwargs = {}
        if args.title:
            kwargs['title'] = args.title
        if args.description:
            kwargs['description'] = args.description
        if args.priority:
            priority_map = {
                'low': Priority.LOW,
                'medium': Priority.MEDIUM,
                'high': Priority.HIGH,
                'critical': Priority.CRITICAL
            }
            kwargs['priority'] = priority_map.get(args.priority)

        task = self.manager.update(args.task_id, **kwargs)
        if task:
            print(f"✏️ 任务已更新: {task.title}")
        else:
            print(f"❌ 未找到任务: {args.task_id}")

    def _cmd_today(self):
        """今日推荐"""
        tasks = self.manager.get_today_focus()

        if not tasks:
            print("🎉 太棒了！没有待处理的任务")
            return

        print("\n🎯 今日AI推荐任务 (按优先级排序)\n")
        print(f"{'排名':<6} {'ID':<12} {'优先级':<8} {'AI评分':<8} {'标题':<30}")
        print("-" * 70)

        for i, task in enumerate(tasks, 1):
            title = task.title[:28] + '..' if len(task.title) > 30 else task.title
            medal = {1: '🥇', 2: '🥈', 3: '🥉'}.get(i, f"{i}.")
            print(f"{medal:<6} {task.id:<12} {task.priority_name:<8} {task.ai_score:>6.1f}   {title:<30}")

        print("\n💡 建议: 优先完成前3个任务，保持专注！")

    def _cmd_stats(self):
        """统计信息"""
        stats = self.manager.get_stats()

        print("\n📊 TaskMind 统计概览\n")
        print(f"  总任务数:     {stats['total']}")
        print(f"  已完成:       {stats['completed']} ({stats['completion_rate']}%)")
        print(f"  待处理:       {stats['pending']}")
        print(f"  进行中:       {stats['in_progress']}")
        print(f"  本周完成:     {stats['completed_this_week']}")
        print(f"  即将到期:     {stats['due_soon']}")
        print("\n  优先级分布:")
        for name, count in stats['priority_distribution'].items():
            bar = '█' * (count // 2)
            print(f"    {name:<10} {count:>3} {bar}")

    def _cmd_export(self, args):
        """导出任务"""
        status_map = {
            'pending': Status.PENDING,
            'in_progress': Status.IN_PROGRESS,
            'completed': Status.COMPLETED
        }
        status = status_map.get(args.status) if args.status else None

        self.manager.export_markdown(args.filepath, status=status)
        print(f"📄 任务已导出到: {args.filepath}")

    def _cmd_search(self, args):
        """搜索任务"""
        keyword = args.keyword.lower()
        all_tasks = self.manager.list_tasks()

        results = [
            t for t in all_tasks
            if keyword in t.title.lower()
            or keyword in t.description.lower()
            or any(keyword in tag.lower() for tag in t.tags)
        ]

        if not results:
            print(f"🔍 未找到包含 '{args.keyword}' 的任务")
            return

        print(f"\n🔍 找到 {len(results)} 个匹配任务:\n")
        for task in results:
            print(f"  {task.status_icon} [{task.id}] {task.title}")


def main():
    """主入口"""
    cli = TaskMindCLI()
    cli.run()


if __name__ == '__main__':
    main()
