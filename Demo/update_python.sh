#!/bin/bash
set -e

echo "=== 1. 更新 Homebrew ==="
brew update
brew upgrade

echo "=== 2. 卸载旧的 Python (可选) ==="
# 注意不要删除 /usr/bin 下系统自带 Python
brew uninstall --ignore-dependencies python@3.9 || true
brew uninstall --ignore-dependencies python@3.10 || true

echo "=== 3. 安装最新 Python ==="
brew install python@3.12

# 设置 PATH
echo 'export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"' >> ~/.zshrc
export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"

echo "=== 4. 升级 pip、setuptools、wheel ==="
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip setuptools wheel

echo "=== 5. 安装虚拟环境工具 ==="
python3 -m pip install virtualenv virtualenvwrapper

echo "=== 6. 创建干净虚拟环境（可选） ==="
python3 -m venv ~/python_venv
echo "source ~/python_venv/bin/activate" >> ~/.zshrc

echo "=== 7. 验证安装 ==="
python3 --version
pip --version
