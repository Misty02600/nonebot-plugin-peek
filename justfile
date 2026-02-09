set windows-shell := ["powershell", "-NoProfile", "-Command"]

# 默认任务列表
default:
    @just --list

<<<<<<< HEAD
# 运行测试
test:
    uv run pytest --cov=src --cov-report xml --junitxml=./junit.xml -n auto
=======
# 运行   nonebot
run:
    uv run nbr run --reload

# 运行测试
test:
    uv run pytest -n auto
>>>>>>> bed50d109db8bcb12270510364bc42dcf4c7fe7b

# 版本发布（更新版本号、更新 lock 文件）
bump:
    uv run cz bump
    uv lock

# 生成 changelog
changelog:
    uv run git-cliff --latest

<<<<<<< HEAD
# 安装 pre-commit hooks
hooks:
    uv run prek install

=======
>>>>>>> bed50d109db8bcb12270510364bc42dcf4c7fe7b
# 代码检查
lint:
    uv run ruff check . --fix

# 代码格式化
format:
    uv run ruff format .

# 类型检查
check:
    uv run basedpyright

<<<<<<< HEAD
=======
# 安装 pre-commit hooks
hooks:
    uv run prek install

>>>>>>> bed50d109db8bcb12270510364bc42dcf4c7fe7b
# 更新 pre-commit hooks
update:
    uv run prek auto-update
