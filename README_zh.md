# CVAT CLI 工具

一个通过命令行直接与 CVAT（计算机视觉标注工具）交互的工具，遵循 Claude 自定义技能规范。**无需编写 Python 脚本，直接使用命令行即可完成所有操作！**

## 功能

- 全面访问 CVAT API 功能
- 支持任务、项目、作业、用户和实现的管理
- 通过环境变量进行配置
- 简单直观的命令行界面
- 内置帮助文档和使用示例

## 要求

- Python 3.7+
- `cvat-sdk` 包
- Claude API 访问权限（如果作为技能使用）

## 安装

1. 克隆此仓库：
   ```bash
   git clone https://github.com/yourusername/cvat-cli.git
   cd cvat-cli
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 设置环境变量：
   ```bash
   export CVAT_HOST=https://your-cvat-instance
   export CVAT_USERNAME=your-username
   export CVAT_PASSWORD=your-password
   ```

## 使用 - 命令行方式（强烈推荐）

**请使用 `cvat-cli.py` 命令行工具，无需编写 Python 脚本！**

### 查看帮助

```bash
python cvat-cli.py --help
```

### 任务管理

```bash
# 列出所有任务
python cvat-cli.py task list

# 获取任务详情
python cvat-cli.py task get --task-id 1

# 创建新任务
python cvat-cli.py task create --name "My Task" --project-id 2

# 更新任务
python cvat-cli.py task update --task-id 1 --name "New Name"

# 删除任务
python cvat-cli.py task delete --task-id 1
```

### 项目管理

```bash
# 列出所有项目
python cvat-cli.py project list

# 获取项目详情
python cvat-cli.py project get --project-id 1

# 创建新项目
python cvat-cli.py project create --name "My Project"

# 更新项目
python cvat-cli.py project update --project-id 1 --name "New Name"

# 删除项目
python cvat-cli.py project delete --project-id 1
```

### 作业管理

```bash
# 列出所有作业
python cvat-cli.py job list

# 获取作业详情
python cvat-cli.py job get --job-id 1
```

### 用户管理

```bash
# 列出所有用户
python cvat-cli.py user list

# 获取用户详情
python cvat-cli.py user get --user-id 1
```

### 实现管理

```bash
# 列出所有实现
python cvat-cli.py implementation list
```

## 作为 Claude 技能使用

1. 将技能目录打包为 zip 文件
2. 将其上传到 Claude 的技能管理界面
3. 配置技能，填写您的 CVAT_HOST、用户名和密码
4. 在 Claude 对话中使用技能时，**优先使用命令行方式**，例如：
   ```
   请帮我列出所有 CVAT 任务
   ```
   Claude 会自动使用 `cvat-cli.py task list` 命令完成，而不是编写 Python 脚本。

## 响应格式

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

## 故障排除

- **缺少环境变量**：确保设置了所有必需的环境变量
- **CVAT SDK 未找到**：确保安装了 `cvat-sdk`
- **认证错误**：验证您的 CVAT_HOST、用户名和密码
- **API 错误**：检查输出中的 `message` 字段获取错误详情

## 许可证

MIT
