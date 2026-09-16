# Git 学习笔记

> Git 是一个分布式版本控制工具：它记录文件演变、支持多人协作，也让我们能够安全地回退到历史版本。GitHub、Gitee 是托管 Git 仓库的平台；Git 不是 GitHub。

## 1. 安装与首次配置

### 1.1 安装 Git

在 [Git 官网](https://git-scm.com/) 下载适合 Windows 的安装包。安装时建议保留默认选项，并启用在终端和 VS Code 中使用 Git 的选项。

安装完成后，在 VS Code 终端运行：

```bash
git --version
```

能显示版本号即表示安装成功。

### 1.2 配置身份信息

每次提交都会记录作者信息，首次使用时配置一次即可：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

查看配置：

```bash
git config --global --list
```

若只想给当前项目设置身份，去掉 `--global` 即可。邮箱应尽量与 GitHub/Gitee 账户中验证过的邮箱一致。

### 1.3 代理设置（按需）

只有在网络环境确实需要代理时才配置，端口应以自己代理软件显示的端口为准：

```bash
git config --global http.proxy "http://127.0.0.1:端口号"
git config --global https.proxy "http://127.0.0.1:端口号"
```

取消代理：

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

不要把示例端口当作固定配置；代理失效时，`clone`、`pull`、`push` 都可能失败。

### 1.4 认证方式

连接 GitHub/Gitee 时可使用 HTTPS 或 SSH。

- **HTTPS**：上手简单；GitHub 不支持用账户密码直接进行 Git 操作，应使用浏览器授权或 Personal Access Token（PAT）。
- **SSH**：配置密钥后日常推送方便。公钥可以添加至平台账户，私钥绝不能上传或分享。

---

## 2. Git 的核心概念

### 2.1 四个区域

```text
工作区（Working Directory）
        │ git add
        ▼
暂存区（Staging Area / Index）
        │ git commit
        ▼
本地仓库（Local Repository）
        │ git push / git fetch、git pull
        ▼
远程仓库（Remote Repository）
```

- **工作区**：当前正在编辑的文件。
- **暂存区**：准备放入下一次提交的文件快照。
- **本地仓库**：本机 `.git` 目录中保存的提交历史。
- **远程仓库**：GitHub、Gitee 等平台上的仓库副本。

一个 commit 是某个时刻项目的快照，有唯一的提交哈希值（commit id）。

### 2.2 日常开发最小闭环

```bash
git status                 # 查看当前状态，最常用
git add <文件名>            # 将指定修改放入暂存区
git add .                  # 将当前目录下的修改放入暂存区
git commit -m "docs: 补充安装说明"
git push                   # 将本地提交推送到远程
```

建议每次 `git add` 前先执行 `git status`，每次提交前用 `git diff --staged` 确认暂存内容。

### 2.3 常用命令速查

| 目的 | 命令 | 说明 |
| --- | --- | --- |
| 查看状态 | `git status` | 查看当前分支、未暂存和已暂存的修改 |
| 查看未暂存改动 | `git diff` | 比较工作区与暂存区 |
| 查看已暂存改动 | `git diff --staged` | 比较暂存区与最新提交 |
| 查看历史 | `git log --oneline --graph --all` | 紧凑地显示分支与提交历史 |
| 查看某次提交 | `git show <commit>` | 查看提交具体改了什么 |
| 查看远程 | `git remote -v` | 查看远程仓库地址 |
| 重命名文件 | `git mv old new` | 让 Git 明确记录重命名 |
| 删除被追踪文件 | `git rm <文件>` | 删除文件并暂存删除操作 |

---

## 3. 仓库创建与远程连接

### 3.1 初始化本地仓库

在项目目录打开 VS Code 终端：

```bash
git init
git branch -M main
```

`git init` 会创建隐藏的 `.git` 目录；不要手动删除或随意修改该目录。之后按“修改 → add → commit”完成首次提交。

### 3.2 克隆已有仓库

要参与已有项目，通常使用：

```bash
git clone <仓库地址>
cd <仓库目录>
```

克隆时 Git 会自动添加名为 `origin` 的远程仓库。

### 3.3 关联远程仓库并首次推送

先在 GitHub/Gitee 创建一个空仓库；随后在本地项目中执行：

```bash
git remote add origin <仓库地址>
git branch -M main
git push -u origin main
```

`-u` 用于建立本地 `main` 与远程 `origin/main` 的跟踪关系。以后同一分支通常只需 `git push`。

也可以使用 VS Code 源代码管理面板的 **发布分支（Publish Branch）** 或 **添加远程仓库（Add Remote）**，但理解命令有助于排查问题。

### 3.4 获取远程更新：fetch 与 pull

```bash
git fetch origin            # 下载远程更新，不改当前工作区
git pull                    # 获取远程更新后，合并或变基到当前分支
```

`fetch` 适合先查看远程改动；`pull` 会直接尝试更新本地文件。开始工作前建议先 `git pull`，以减少与他人的冲突。

---

## 4. 提交规范与 .gitignore

### 4.1 写好提交信息

一次提交应只解决一类相关问题，保持小而完整，便于审查和回退。推荐格式：

```text
类型: 简短说明
```

常见类型：

- `feat`：新功能
- `fix`：修复问题
- `docs`：文档修改
- `refactor`：重构，功能行为不变
- `test`：测试相关
- `chore`：构建、依赖或杂项维护

示例：`docs: 补充 GitHub Actions 入门说明`。

### 4.2 使用 .gitignore

`.gitignore` 用于告诉 Git 忽略不应提交的文件，例如依赖目录、构建产物、日志和本地环境配置：

```gitignore
# Python
__pycache__/
.venv/

# Node.js
node_modules/
dist/

# 本地环境与日志
.env
*.log
```

**绝不要提交**密码、访问令牌、私钥、数据库连接串等敏感信息。已经被 Git 追踪的文件，即使之后加入 `.gitignore` 也不会自动停止追踪；需先执行：

```bash
git rm --cached <文件名>
```

若密钥已推送到远程，应立即在对应平台作废并更换；仅删除文件并不能清除历史记录中的泄漏。

---

## 5. 分支、合并与冲突

### 5.1 为什么使用分支

分支让新功能、修复或实验与稳定主线隔离。不要直接在共享的 `main` 分支上进行较大的开发。

常见命名：

```text
feature/login-page
fix/payment-timeout
docs/git-notes
```

### 5.2 创建与切换分支

```bash
git branch                         # 查看本地分支
git branch -a                      # 查看本地和远程分支
git switch -c feature/login-page   # 创建并切换分支（推荐）
git switch main                    # 切换到 main
```

兼容写法为 `git checkout -b <分支名>` 和 `git checkout <分支名>`。

推送新分支：

```bash
git push -u origin feature/login-page
```

### 5.3 合并（merge）

在目标分支上执行合并。例如把功能分支合入 `main`：

```bash
git switch main
git pull
git merge feature/login-page
git push
```

实际团队项目通常通过 Pull Request 合并，以便代码审查、自动测试和保护规则生效。

### 5.4 rebase 的用途

`rebase` 会把当前分支的提交“接到”另一个分支的最新提交之后，使历史更线性：

```bash
git switch feature/login-page
git fetch origin
git rebase origin/main
```

**不要对已推送且多人共用的分支随意 rebase**，因为它会改写提交历史。个人功能分支在创建 PR 前整理历史较常见；共享分支优先使用 merge。

### 5.5 处理合并冲突

当多人修改了同一位置，Git 无法自动决定保留哪一份，会标记冲突：

```text
<<<<<<< HEAD
当前分支的内容
=======
正在合入内容
>>>>>>> other-branch
```

处理步骤：

1. 使用 VS Code 的冲突编辑器或手动编辑，保留正确内容并删除冲突标记。
2. 运行测试或至少检查受影响功能。
3. `git add <已解决文件>`。
4. merge 冲突使用 `git commit` 完成合并；rebase 冲突使用 `git rebase --continue`。

放弃本次操作：

```bash
git merge --abort
git rebase --abort
```

### 5.6 删除分支

```bash
git branch -d feature/login-page       # 删除已合并的本地分支
git branch -D feature/login-page       # 强制删除本地分支，谨慎使用
git push origin --delete feature/login-page  # 删除远程分支
```

---

## 6. 撤销、回退与救援

> 先执行 `git status` 和 `git log --oneline` 确认状态。涉及远程历史时，团队协作优先选择安全、可追溯的 `revert`。

### 6.1 取消暂存

文件已经 `git add`，但还未提交：

```bash
git restore --staged <文件名>
```

这只把文件移出暂存区，不会丢失工作区中的修改。

### 6.2 丢弃未提交修改

```bash
git restore <文件名>
```

这会覆盖该文件未提交的改动。若修改很重要，先复制备份或提交到临时分支。

### 6.3 撤销一个已提交的改动：revert（推荐）

```bash
git revert <commit_id>
git push
```

`revert` 会新建一个“反向修改”的提交，不改写已有历史，适合已经推送或多人协作的提交。

### 6.4 本地回退：reset

```bash
git reset --soft <commit_id>    # 回退提交，保留暂存区和工作区修改
git reset --mixed <commit_id>   # 回退提交和暂存区，保留工作区修改（默认）
git reset --hard <commit_id>    # 回退提交、暂存区和工作区，未提交改动会丢失
```

`git reset --hard` 风险最高，使用前务必确认目标提交并备份重要内容。它只改变**本地**历史；若还要让远程回退，需要额外推送。

### 6.5 远程仓库如何回退

- 已经共享或不确定是否有人基于该提交开发：使用 `git revert <commit_id>`，再普通 `git push`。
- 确认只有自己使用该分支、且必须重写远程历史：本地 `git reset --hard <commit_id>` 后执行：

```bash
git push --force-with-lease origin <分支名>
```

相比 `--force`，`--force-with-lease` 会在远程出现你尚未获取的新提交时拒绝覆盖，仍需谨慎。

### 6.6 找回“丢失”的提交

误 reset、误删分支后可先查看引用日志：

```bash
git reflog
git switch -c recover-work <reflog中的提交哈希>
```

只要 Git 尚未清理对象，`reflog` 往往能找回本地曾指向的提交。

---

## 7. 开源贡献流程（Fork → PR）

### 7.1 Fork 与克隆

1. 在原项目页面点击 **Fork**，复制一份到自己的账户。
2. 克隆自己的 fork：`git clone <自己的仓库地址>`。
3. 将原项目添加为 `upstream`：

```bash
git remote add upstream <原项目仓库地址>
git remote -v
```

通常 `origin` 指向自己的 fork，`upstream` 指向原项目。

### 7.2 同步原项目并开发

```bash
git switch main
git fetch upstream
git merge upstream/main
git push origin main
git switch -c docs/improve-installation
```

不同项目默认分支可能叫 `master`，应以仓库实际情况为准。开发前请阅读项目的 `README.md`、`CONTRIBUTING.md`、代码规范和行为准则。

### 7.3 提交 Pull Request

1. 完成修改后，执行测试、格式化或项目要求的检查。
2. 用清晰的提交信息提交并推送自己的分支。
3. 在 GitHub/Gitee 创建 Pull Request（PR）：目标仓库/目标分支应为原项目要求的分支。
4. PR 描述应说明：解决了什么问题、改动内容、验证方式，以及是否存在限制或关联 Issue。
5. 根据维护者的 review 意见继续修改；新的 push 会自动更新同一个 PR。

合并后，可以删除远程功能分支和本地分支，保持仓库整洁。

---

## 8. 团队协作规范

### 8.1 邀请协作者与保护分支

在 GitHub 仓库中通常可通过 **Settings → Collaborators** 邀请成员。对 `main` 等稳定分支，建议在 **Settings → Rules / Rulesets** 配置规则：

- 禁止直接推送，要求通过 Pull Request 合并。
- 要求至少一位审查者批准。
- 要求状态检查（测试、构建、Lint）通过。
- 限制强制推送和删除分支。

实际界面名称可能因 GitHub/Gitee 版本和权限不同略有差异。

### 8.2 推荐协作流程

```text
从最新 main 创建功能分支
        ↓
开发、提交小而清晰的 commits
        ↓
push 功能分支并创建 PR
        ↓
自动检查 + 代码审查
        ↓
合并到 main，删除临时分支
```

协作习惯：

- 开始工作前拉取最新主分支；提交前再次同步并处理冲突。
- 不要在他人的分支上直接修改或强推。
- 一次 PR 聚焦一个目标，说明改动范围和验证结果。
- 代码审查关注正确性、边界条件、可读性、测试和安全性，而不只看格式。

---

## 9. GitHub Actions 入门

GitHub Actions 是 GitHub 提供的持续集成/持续部署（CI/CD）工具：当 push、创建 PR 等事件发生时，自动运行测试、检查、构建或部署。

工作流文件放在仓库的 `.github/workflows/` 目录下，扩展名为 `.yml` 或 `.yaml`。

### 9.1 一个最小工作流

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run a check
        run: echo "CI is running"
```

关键概念：

- **workflow**：一个自动化流程。
- **event / trigger**：触发流程的事件，如 `push`、`pull_request`、定时任务。
- **job**：在某个运行环境中执行的一组任务。
- **step**：job 中的一个具体步骤，可以运行命令（`run`）或复用 action（`uses`）。
- **runner**：执行 job 的虚拟环境，如 `ubuntu-latest`。

### 9.2 安全注意事项

- 密钥应存放于仓库/组织的 **Settings → Secrets and variables → Actions**，通过 `${{ secrets.NAME }}` 使用。
- 不要把 token、密码写进 YAML、提交信息、日志或截图。
- 来自 fork 的 PR 应谨慎使用具备写权限的 token 或部署密钥。
- 固定第三方 action 的可信版本，重要项目可固定到提交哈希以提高供应链安全性。

---

## 10. VS Code 中的常用操作

打开左侧的 **源代码管理（Source Control）** 面板即可完成多数日常操作：

- `+`：暂存单个文件；`+` 全部暂存。
- 输入框：填写提交信息；勾选按钮：提交。
- `…`：访问拉取、推送、抓取、分支、暂存（stash）等操作。
- 左下角分支名称：创建或切换分支。
- 遇到冲突时，编辑器会显示“接受当前更改 / 接受传入更改 / 两者都接受”等选项；选择前应理解两边内容。

图形界面和命令行操作的是同一个 Git 仓库。遇到问题时，终端中的 `git status` 往往最能说明当前状态。

---

## 11. 高频问题速记

| 问题 | 处理方式 |
| --- | --- |
| 修改了文件但 `git status` 没显示 | 检查文件是否被 `.gitignore` 忽略，或是否在正确仓库目录 |
| push 被拒绝 | 先 `git pull` / `git fetch` 了解远程更新，合并冲突后再 push；不要急于强推 |
| commit 写错了 | 尚未 push：可用 `git commit --amend`；已共享：通常另提交一次修正更安全 |
| 把文件 add 错了 | `git restore --staged <文件名>` |
| 想临时保存未完成工作 | `git stash`，恢复用 `git stash pop` |
| 找不到之前的提交 | `git reflog` 查找，再创建恢复分支 |
| 图片在别人电脑上不显示 | 将图片放入仓库如 `assets/`，用相对路径：`![说明](assets/example.png)` |

## 12. 推荐练习顺序

1. 新建一个练习仓库，完成 `init → add → commit → log`。
2. 新建远程仓库，完成 `remote add → push → clone`。
3. 创建两个分支，故意修改同一行并练习解决冲突。
4. 分别练习 `restore --staged`、`revert`、`reset` 和 `reflog`，理解它们的风险差异。
5. Fork 一个文档友好的开源项目，提交一次小型 PR。
6. 新建一个最小 GitHub Actions 工作流，让它在 push 时自动运行。
