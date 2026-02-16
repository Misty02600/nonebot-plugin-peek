set windows-shell := ["powershell", "-NoProfile", "-Command"]

# 默认任务列表
default:
    @just --list

<<<<<<< HEAD
=======
# 运行   nonebot
run:
    uv run nb run --reload

>>>>>>> 571d17c64c0c479fc06149d3129ec4bfd8931216
# 运行测试
test:
    uv run pytest -n auto

# 版本发布（更新版本号、更新 lock 文件）
bump:
    uv run cz bump
    uv lock
<<<<<<< HEAD
    git push --tags
=======
    git push --follow-tags
>>>>>>> 571d17c64c0c479fc06149d3129ec4bfd8931216

# 生成 changelog
changelog:
    uv run git-cliff --latest

<<<<<<< HEAD
# 安装 pre-commit hooks
hooks:
    uv run prek install

# 代码检查与格式化
lint:
    uv run ruff check . --fix
=======
# 代码检查
lint:
    uv run ruff check . --fix

# 代码格式化
format:
>>>>>>> 571d17c64c0c479fc06149d3129ec4bfd8931216
    uv run ruff format .

# 类型检查
check:
    uv run basedpyright

<<<<<<< HEAD
=======
# 安装 pre-commit hooks
hooks:
    uv run prek install

>>>>>>> 571d17c64c0c479fc06149d3129ec4bfd8931216
# 更新 pre-commit hooks
update:
    uv run prek auto-update

# 从 dev 向 main 创建 PR
pr:
    gh pr create --base main --fill
    gh pr view --web

# PR 合并后强制同步到 main
sync:
    git fetch origin
    git reset --hard origin/main
    git push origin --force-with-lease
