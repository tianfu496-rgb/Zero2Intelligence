# Git学习笔记

## 1.安装

* **git下载**:下载win11x64版本即可

* **git设置**:安装时注意要选择vscode,在终端中使用`git config --global http.proxy "http://127.0.0.1:8080"`命令设置代理(clash猫的一般端口)

## 2.基本操作(以下皆在VSCode中操作)

* **初始化**:本地创建仓库的第一步是初始化仓库,在vscode中可以初始化
* **提交**:==commit提交==也就是在保留当前的版本,提交时命名要包含必要的信息

* **推送**:登录要上传的平台如GitHub或Gitee(需要先进行注册)。
  终端中设置用户名命令`git config --global user.name "Your Name"`
  设置邮箱命令`git config --global user.email "your.email@example.com"`

  * 本地第一次推送:
    本地点击==publish banrch==可以选择在云端发布,云端仓库名字与本地名字保持一致,可以在==setting==中重命名

  * 链接云端仓库推送:
    平台上创建仓库,在本地vscode上更改选项上点击=='''更多操作==中的远程添加已有仓库

  后续推送点击==同步更新==即可

* **拉取**:点击图表一栏的==抓取==获得远程更新,再点击==拉取==更新到本地
* **查看提交历史**:本地在终端输入`git log`,云可以直接查看
* **撤销指定提交**：`git revert <commit_id>`
* **本地仓库回退**:彻底回退到目标 commit（工作区、暂存区、HEAD 均同步到目标版本） `git reset --hard x7y8z9w` 
  可选：如果只想回退 HEAD 和暂存区，保留工作区修改（谨慎使用） `git reset --mixed x7y8z9w` 默认模式，可省略 --mixed
  `--hard`：会直接覆盖工作区和暂存区的内容，**未提交的修改会丢失**
* **远程仓库回退**:`git reset 哈希值`

## 3.开源贡献步骤(可以写在简历中如"XXX的开源贡献者")

* **fork**:
  首先将需要修改的项目fork到自己的仓库中

* **修改**:
  可以选择在线修改或者clone到自己本地进行修改

* **提交修改(自己账号上)**:
  点击==commit changes==提交修改,在提交时为修改命名,如果仓库没有要求==命名规范==的话,推荐命名格式(==方向:描述==。如==docs==:文档修改,==bug==:使用功能优化,)

  * 示例:docs: Update 2.installation.md

  ==扩展描述==:描述一下问题,修改了那些内容,达成了什么效果,优化什么东西,可以附带图片

* **提交修改(原始仓库)**:
  点击==creat pull request==提交到原始仓库,等待作者审核

## 4.协作

* **邀请协作者**:点击平台上仓库的==settings==,左边一栏找到==Collaborators==进入,点击==add people
* **制定合并规则**:左边一栏中找到==Rules==->==Rulesets==,进入后点击==New ruleset==->==New banrch ruleset==。设置名字和==Target branches(作用的分支)==,有需要选择==Require a pull request before merging(再合并前审查)==
* **创建新分支**:点击该图标创建新分支![image-20260626160326733](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260626160326733.png)
* **发送pull request请求并同意**:![image-20260626160619159](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260626160619159.png)![image-20260626160715470](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260626160715470.png)![image-20260626160844791](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260626160844791.png)
* **删除临时分支**:
  ![image-20260626160923290](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260626160923290.png)
  ![image-20260626160943083](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260626160943083.png)

## 5.GitHub Action