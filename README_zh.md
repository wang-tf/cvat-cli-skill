# CVAT SDK 技能

一个通过 CVAT SDK 与 CVAT（计算机视觉标注工具）交互的技能，遵循 Claude 自定义技能规范。

## 功能

- 全面访问 CVAT API 功能
- 支持任务、项目、作业、用户和实现的管理
- 通过环境变量进行配置
- 适当的错误处理和响应格式

## 要求

- Python 3.7+
- `cvat-sdk` 包
- Claude API 访问权限

## 安装

1. 克隆此仓库：
   ```bash
   git clone https://github.com/yourusername/cvat-sdk-skill.git
   cd cvat-sdk-skill
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 设置环境变量：
   ```bash
   export CVAT_API_URL=https://your-cvat-instance/api/v1
   export CVAT_USERNAME=your-username
   export CVAT_PASSWORD=your-password
   ```

## 使用

### 作为 Claude 技能

1. 将技能目录打包为 zip 文件
2. 将其上传到 Claude 的技能管理界面
3. 配置技能，填写您的 CVAT API URL、用户名和密码
4. 在 Claude 对话中使用技能：
   ```
   @CVAT SDK Skill
   {
     "action": "list_tasks"
   }
   ```

### 本地测试

您可以通过以下命令在本地测试技能：

```bash
python scripts/cvat_cli_tools.py '{"action": "list_tasks"}'
```

## 支持的操作

### 任务
- `list_tasks` - 列出所有任务
- `get_task` - 获取任务详情
- `create_task` - 创建新任务
- `update_task` - 更新任务
- `delete_task` - 删除任务

### 项目
- `list_projects` - 列出所有项目
- `get_project` - 获取项目详情
- `create_project` - 创建新项目
- `update_project` - 更新项目
- `delete_project` - 删除项目

### 作业
- `list_jobs` - 列出所有作业
- `get_job` - 获取作业详情

### 用户
- `list_users` - 列出所有用户
- `get_user` - 获取用户详情

### 实现
- `list_implementations` - 列出所有实现

### Lambda 函数
- `list_lambdas` - 列出所有 lambda 函数
- `get_lambda` - 获取 lambda 函数详情
- `create_lambda` - 创建新的 lambda 函数
- `update_lambda` - 更新 lambda 函数
- `delete_lambda` - 删除 lambda 函数
- `upload_lambda_code` - 上传代码到 lambda 函数

## 响应格式

技能以 JSON 格式返回响应，结构如下：

```json
{
  "status": "success" 或 "error",
  "message": "结果描述",
  "data": "结果数据（如果适用）"
}
```

## 故障排除

- **缺少环境变量**：确保设置了所有必需的环境变量
- **CVAT SDK 未找到**：确保安装了 `cvat-sdk`
- **认证错误**：验证您的 CVAT API URL、用户名和密码
- **API 错误**：检查响应中的 `message` 字段获取错误详情

## 许可证

MIT
