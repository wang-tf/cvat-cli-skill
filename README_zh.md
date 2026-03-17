# CVAT CLI 技能

一个通过CLI与CVAT（计算机视觉标注工具）交互的技能，遵循Claude自定义技能规范。

## 功能

- 直接从Claude执行CVAT CLI命令
- 支持所有CVAT CLI命令和参数
- 通过环境变量进行配置
- 适当的错误处理和响应格式

## 要求

- Python 3.7+
- `cvat-cli` 包
- Claude API 访问权限

## 安装

1. 克隆此仓库：
   ```bash
   git clone https://github.com/yourusername/cvat-cli-skill.git
   cd cvat-cli-skill
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

### 作为Claude技能

1. 将技能目录打包为zip文件
2. 将其上传到Claude的技能管理界面
3. 配置技能，填写您的CVAT API URL、用户名和密码
4. 在Claude对话中使用技能：
   ```
   @CVAT CLI Skill
   {
     "command": "tasks list",
     "args": "--page_size 10"
   }
   ```

### 本地测试

您可以通过以下命令在本地测试技能：

```bash
python main.py '{"command": "tasks list", "args": "--page_size 10"}'
```

## 命令参考

此技能支持所有CVAT CLI命令。一些常用命令包括：

- `tasks list` - 列出所有任务
- `tasks create` - 创建新任务
- `tasks get` - 获取任务详情
- `projects list` - 列出所有项目
- `projects create` - 创建新项目

完整的命令列表，请运行 `cvat-cli --help`。

## 响应格式

技能以JSON格式返回响应，结构如下：

```json
{
  "status": "success" 或 "error",
  "message": "结果描述",
  "data": {
    "stdout": "命令输出",
    "stderr": "命令错误（如果有）"
  }
}
```

## 故障排除

- **缺少环境变量**：确保设置了所有必需的环境变量
- **CVAT CLI未找到**：确保安装了`cvat-cli`并在PATH中
- **认证错误**：验证您的CVAT API URL、用户名和密码
- **命令错误**：检查响应中的`stderr`字段获取错误详情

## 许可证

MIT
