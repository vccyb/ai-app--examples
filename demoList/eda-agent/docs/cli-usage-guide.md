# 🧪 EDA Agent系统 - CLI测试指南

## 🚀 快速测试命令

### 测试1：基本优化指令
```bash
python3 cli.py "优化模块A时序<10ns"
```

**预期输出**：
```
======================================================================
🤖 EDA Agent系统 - 交互式界面

正在处理您的请求...
用户指令: 优化模块A时序<10ns

[Master] 步骤1：查询RAG知识...
[Master] 查询到规范: {'timing': {}, 'power': {}, 'area': {}}
[Master] 步骤2：执行EDA仿真...
[EDA Tool] 仿真完成: {'timing': '11.7ns', 'power': '48.6mW', 'area': '1000um²'}
[Master] 步骤3：评判结果...
[Master] 评判结果: FAIL - 实际11.7ns未达目标10ns，差距+17.0%

📊 处理结果
状态: success
模块: 模块A时序
仿真结果: {'timing': '11.7ns', 'power': '48.6mW', 'area': '1000um²'}
评判结果: FAIL - 实际11.7ns未达目标10ns，差距+17.0%

======================================================================
```

---

### 测试2：查询规范
```bash
python3 cli.py "查询模块A的设计规范"
```

**预期输出**：
```
[Master] 查询到规范: {'timing': {'max_clock': '100MHz', 'typical_timing': '10ns'}, 'power': {'max': '100mW'}, 'area': {'max': '1000um²'}}
```

---

### 测试3：查看帮助
```bash
python3 cli.py "help"
```

**预期输出**：
```
🎯 EDA Agent系统 - 交互式界面

📋 可用命令:
  优化 [模块] [指标] <值>         - 执行优化或仿真任务
  查询 [模块名]                          - 查询模块设计规范
  帮助                                  - 显示此帮助信息
  历史 [history/h]                          - 查看对话历史（最近5条）
  退出/quit [q]                             - 退出系统

💡 使用示例:
  EDA > 优化模块A时序<10ns
  EDA > 查询模块B的设计规范
  EDA > history
  EDA > quit
```

---

## 🔍 运行环境检查

**确认Python 3**：```bash
python3 --version
```

**确认src目录结构**：```bash
ls -la src/agents/
```

---

## 💡 使用提示

1. **确保在项目根目录运行**：
   ```bash
   cd /Users/chenyubo/Project/ai-project/demoList/eda-agent
   python3 cli.py "优化模块A时序<10ns"
   ```

2. **查看完整输出**：所有信息都会显示

3. **退出系统**：输入`quit`或`q`

---

**准备就绪！** 🎯 可以开始测试了！
