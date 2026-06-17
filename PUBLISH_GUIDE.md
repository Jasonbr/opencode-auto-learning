# v1.2.0 发布指南

## 手动发布步骤

由于自动化推送遇到认证问题，请按以下步骤手动发布：

### 步骤 1: 确认本地状态

```bash
cd ~/opencode-auto-learning

# 检查状态
git status

# 应该显示：
# On branch main
# nothing to commit, working tree clean
```

### 步骤 2: 推送代码

```bash
# 推送到 main
git push origin main

# 如果提示输入用户名和密码：
# Username: Jasonbr
# Password: [你的 GitHub Personal Access Token]
```

**获取 GitHub Token：**
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 选择 "repo" 权限
4. 复制生成的 token 作为密码

### 步骤 3: 创建标签

```bash
# 创建 v1.2.0 标签
git tag v1.2.0

# 推送标签
git push origin v1.2.0
```

### 步骤 4: 验证发布

访问以下链接确认发布成功：

- **主仓库**: https://github.com/Jasonbr/opencode-auto-learning
- **Releases**: https://github.com/Jasonbr/opencode-auto-learning/releases
- **v1.2.0 标签**: https://github.com/Jasonbr/opencode-auto-learning/releases/tag/v1.2.0

### 步骤 5: 创建 GitHub Release（可选）

1. 访问 https://github.com/Jasonbr/opencode-auto-learning/releases
2. 点击 "Create a new release"
3. 选择标签: v1.2.0
4. 标题: OpenCode Auto-Learning v1.2.0
5. 内容: 复制 RELEASE_v1.2.0.md 的内容
6. 点击 "Publish release"

## 一键脚本

如果希望自动化，可以运行：

```bash
cd ~/opencode-auto-learning

# 配置 git 使用 token
git remote set-url origin https://Jasonbr:YOUR_TOKEN@github.com/Jasonbr/opencode-auto-learning.git

# 推送
git push origin main
git tag v1.2.0
git push origin v1.2.0
```

**注意**: 将 YOUR_TOKEN 替换为你的 GitHub Personal Access Token

## 验证命令

```bash
# 检查远程分支
git branch -r

# 检查标签
git ls-remote --tags origin

# 查看 GitHub 状态
curl -s https://api.github.com/repos/Jasonbr/opencode-auto-learning/releases/latest | grep tag_name
```

## 发布成功标志

✅ 访问 https://github.com/Jasonbr/opencode-auto-learning 能看到所有文件
✅ Releases 页面显示 v1.2.0
✅ 本地运行 `git ls-remote --tags origin` 显示 v1.2.0

---

**需要帮助？** 检查 ~/.git-credentials 或运行 `gh auth login`
