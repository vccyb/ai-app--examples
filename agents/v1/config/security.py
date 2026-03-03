"""
安全配置

实现白名单/黑名单命令验证机制
（来自参考架构的安全设计）
"""
from typing import Dict, Set


# 默认允许的命令（简化版本，适合通用场景）
DEFAULT_ALLOWED_COMMANDS: Set[str] = {
    # 基础命令
    "help", "echo", "pwd", "ls", "cd", "cat", "head", "tail",
    "date", "whoami", "uname",

    # 进程管理
    "sleep", "ps", "top", "kill",

    # 文件操作
    "cp", "mv", "mkdir", "touch", "find", "grep",

    # 网络工具
    "ping", "curl", "wget",

    # 开发工具
    "python", "python3", "node", "npm", "pip",
    "git",

    # 文本处理
    "wc", "sort", "uniq", "cut", "awk", "sed",
}

# 默认阻止的命令（危险命令）
DEFAULT_BLOCKED_COMMANDS: Set[str] = {
    "exec", "system", "eval", "open", "close", "file",
    "spawn", "fork", "execvp", "rm", "delete", "rmdir",
    "chmod", "chown", "su", "sudo", "passwd",
    "dd", "mkfs", "fdisk", "mount", "umount",
}


def validate_command(command: str) -> Dict:
    """
    根据白名单/黑名单验证命令

    Args:
        command: 要验证的命令字符串

    Returns:
        包含 'allowed' 布尔值和可选的 'reason' 字符串的字典
    """
    if not command or not command.strip():
        return {
            "allowed": False,
            "reason": "命令为空"
        }

    # 提取基础命令（第一个单词）
    base_command = command.strip().split()[0]

    # 先检查黑名单
    if base_command in DEFAULT_BLOCKED_COMMANDS:
        return {
            "allowed": False,
            "reason": f"命令 '{base_command}' 因安全原因被阻止"
        }

    # 检查白名单
    if base_command not in DEFAULT_ALLOWED_COMMANDS:
        return {
            "allowed": False,
            "reason": f"命令 '{base_command}' 不在允许列表中",
            "suggestion": f"允许的命令: {', '.join(sorted(DEFAULT_ALLOWED_COMMANDS))}"
        }

    return {"allowed": True}


def load_commands_from_file(filepath: str) -> Set[str]:
    """
    从文件加载命令列表（每行一个命令）

    Args:
        filepath: 命令列表文件的路径

    Returns:
        命令集合
    """
    commands = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    commands.add(line)
    except FileNotFoundError:
        pass  # 返回空集如果文件不存在

    return commands
