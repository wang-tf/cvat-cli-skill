---
name: CVAT CLI Tool
version: 2.0.0
description: CVAT (Computer Vision Annotation Tool) 命令行工具 - 直接使用命令行与 CVAT 交互，无需编写 Python 脚本。支持任务、项目、作业、用户和实现的管理。
dependencies:
  - cvat-sdk
scripts:
  - cvat-cli.py
  - scripts/base.py
---

# CVAT CLI Tool

## Overview

这是一个 CVAT 命令行工具，让您可以直接通过命令行与 CVAT 交互，**无需编写任何 Python 脚本**。本工具提供了完整的 CVAT API 访问能力，包括任务、项目、作业、用户和实现的管理。

## 重要提示

**请优先使用 `cvat-cli.py` 命令行工具，而不是编写 Python 脚本！** 所有功能都可以通过命令行直接完成。

## Configuration

工具需要设置以下环境变量：

- `CVAT_HOST`: 您的 CVAT 服务地址 (例如: https://your-cvat-instance)
- `CVAT_USERNAME`: 您的 CVAT 用户名
- `CVAT_PASSWORD`: 您的 CVAT 密码

## Usage - 命令行使用方式（推荐）

使用 `python cvat-cli.py` 或直接使用 `cvat-cli.py`（如果已设置执行权限）。

### 基本命令结构

```bash
cvat-cli.py <command> <subcommand> [options]
```

### 查看帮助

```bash
# 查看主帮助
cvat-cli.py --help

# 查看特定命令的帮助
cvat-cli.py task --help
cvat-cli.py project --help
```

### 任务管理 (Task Commands)

```bash
# 列出所有任务
cvat-cli.py task list

# 列出任务并应用过滤条件
cvat-cli.py task list --filters '{"status": "annotation"}'

# 获取任务详情
cvat-cli.py task get --task-id 1

# 创建新任务
cvat-cli.py task create --name "My Annotation Task" --project-id 2

# 创建任务并指定标签
cvat-cli.py task create --name "My Task" --labels '[{"name": "person"}, {"name": "car"}]'

# 更新任务
cvat-cli.py task update --task-id 1 --name "Updated Task Name" --status "completed"

# 删除任务
cvat-cli.py task delete --task-id 1
```

### 项目管理 (Project Commands)

```bash
# 列出所有项目
cvat-cli.py project list

# 获取项目详情
cvat-cli.py project get --project-id 1

# 创建新项目
cvat-cli.py project create --name "My Project"

# 创建项目并指定标签
cvat-cli.py project create --name "My Project" --labels '[{"name": "person"}, {"name": "car"}]'

# 更新项目
cvat-cli.py project update --project-id 1 --name "Updated Project Name"

# 删除项目
cvat-cli.py project delete --project-id 1
```

### 作业管理 (Job Commands)

```bash
# 列出所有作业
cvat-cli.py job list

# 获取作业详情
cvat-cli.py job get --job-id 1
```

### 用户管理 (User Commands)

```bash
# 列出所有用户
cvat-cli.py user list

# 获取用户详情
cvat-cli.py user get --user-id 1
```

### 实现管理 (Implementation Commands)

```bash
# 列出所有实现
cvat-cli.py implementation list
```

## Response Format

命令输出格式为 JSON，结构如下：

```json
{
  "status": "success" 或 "error",
  "message": "结果描述",
  "data": "结果数据（如果适用）"
}
```

## 为什么使用命令行而不是 Python 脚本？

1. **更简单直接**：无需编写、保存和执行 Python 脚本文件
2. **更快的工作流**：一条命令即可完成任务
3. **更少的错误**：不需要处理脚本文件路径、导入等问题
4. **更易于自动化**：可以轻松集成到 shell 脚本和 CI/CD 流程中
5. **更好的用户体验**：内置的帮助文档和命令补全支持

## Troubleshooting

- **缺少环境变量**：确保设置了所有必需的环境变量
- **CVAT SDK 未找到**：确保安装了 `cvat-sdk` 包 (`pip install cvat-sdk`)
- **认证错误**：验证您的 CVAT_HOST、用户名和密码
- **API 错误**：检查输出中的 `message` 字段获取错误详情
