 # 技术升级报告 & 维护者/提交者互动教程
 
 > 对比基准：`multiphase-data-hub/multiphase-data-hub.github.io` @ `6aa39e1`
 > 变更总量：18 个文件，+1294 / -54 行
 
 ---
 
 ## 一、技术升级总览
 
 ### 1.1 数据集全生命周期自动化
 
 | 阶段 | 原始版本 | 升级后 |
 |---|---|---|
 | 数据集提交 | 手动开 Issue | 结构化表单 → Issue 模板 |  
 | Issue 受理 | 无 | 自动打标签 + 机器人评论确认 |
 | 元数据校验 | 无 | CI 自动检查 `datasets/*.json` 必填字段 |
 | 网站同步 | 手动编辑 `datasets.js` | CI 从 JSON 全量重建 `datasets.js` |
 | 详情页 | 手动写 HTML | 从 JSON 自动生成 `dataset-{id}.html` |
 | 数据集删除 | 手动清理残留 | 自动删除孤儿详情页 |
 | 邮件通知 | 无 | Issue / Push 时 SMTP 邮件通知维护者 |
 | 直接 push 触发 | 不支持 | `datasets/**.json` 变更自动触发 |
 
 ### 1.2 新增文件清单
 
 **核心脚本（3 个）**
 
 | 文件 | 职责 |
 |---|---|
 | `scripts/generate_datasets_js.py` | 读取 `datasets/*.json` → 全量重建 `website/datasets.js` |
 | `scripts/generate_dataset_pages.py` | 读取 `datasets/*.json` → 生成/清理详情页，删除孤儿页面 |
 | `scripts/validate_dataset_metadata.py` | 校验 JSON 必填字段（id/title/domain/data/license/citation） |
 
 **通知系统（2 个）**
 
 | 文件 | 职责 |
 |---|---|
 | `scripts/notify_reviewers.py` | SMTP 邮件通知，异常时降级为 summary 日志 |
 | `.github/reviewers.yml` | 维护者邮箱列表 |
 
 **CI 工作流（1 个）**
 
 | 文件 | 职责 |
 |---|---|
 | `.github/workflows/dataset-intake.yml` | 三 job 编排：Issue 预检 / 元数据校验 + 自动生成 / 邮件通知 |
 
 ### 1.3 修改的文件
 
 | 文件 | 变更内容 |
 |---|---|
 | `.github/ISSUE_TEMPLATE/dataset_submission.yml` | `metadata_link` 改为必填，增加上传说明 |
 | `.github/PULL_REQUEST_TEMPLATE.md` | 新增数据集 PR 清单 |
 | `website/contribute.html` | 按钮链接指向 fork 仓库的 Issue 模板 |
 | `website/datasets.js` | 从硬编码改为 JSON 驱动自动生成 |
 | `website/dataset-hit-droplet-breakup.html` | 重命名为 `dataset-dns_droplet_breakup_hit_we15.html` 匹配 id |
 | `README.md` / `website/governance.html` | 补充数据提交流程说明 |
 
 ---
 
 ## 二、CI 流水线架构
 
 ```
 触发事件: push / pull_request / issues
                             |
         +-------------------+-------------------+
         |                   |                   |
    [Issue 事件]        [PR / Push 事件]    [所有事件]
         |                   |                   |
   issue-precheck      metadata-validation   notify-reviewers
         |                   |              (仅 Issue + Push)
   - 打标签                - checkout PR分支
   - 机器人评论             - validate_dataset_metadata
                            - generate_datasets_js
                            - generate_dataset_pages
                            - git diff → 有变更则 commit + push
 ```
 
 ---
 
 ## 三、维护者操作教程
 
 ### 3.1 前提：配置 Secrets
 
 Settings → Secrets and variables → Actions → 添加 5 个 secret：
 
 | Name | 示例值 |
 |---|---|
 | `SMTP_HOST` | `smtp.qq.com` |
 | `SMTP_PORT` | `587` |
 | `SMTP_USERNAME` | `your@email.com` |
 | `SMTP_PASSWORD` | 邮箱授权码 |
 | `MAIL_FROM` | `your@email.com` |
 
 ### 3.2 审核数据集提交
 
 1. 收到新 Issue（标题 `[Dataset]`）→ 评论区逐项核实
 2. 检查外部托管链接可访问、`info.json` 完整、许可证明确
 3. 审核通过后要求提交者发 PR，或维护者自行在 `datasets/` 添加 JSON
 
 ### 3.3 处理 PR
 
 1. 查看 PR 的 Files changed
 2. 确认 CI 全部绿灯（`Metadata validation` 通过）
 3. 若 CI 自动提交了补充文件，确认无误
 4. 点击 Merge → 数据集自动上线网站
 
 ### 3.4 删除数据集
 
 1. 删除 `datasets/<id>.json`
 2. Commit + push → CI 自动更新 `datasets.js` + 删除孤儿详情页
 3. 或走 PR 流程，CI 同样处理
 
 ---
 
 ## 四、提交者操作教程
 
 ### 4.1 准备工作
 
 1. 数据文件托管到 ModelScope / Kaggle / Zenodo 等外部平台
 2. 按数据标准编写 `multiphase_info.json`（和 README.md 一起放在数据包中）
 3. 准备一张代表性预览图
 
 ### 4.2 提交数据集申请
 
 1. 打开仓库 Issues 页面 → New Issue → 选 "Dataset submission"
 2. 填写标题、描述、托管平台、DOI、变量、网格、许可证、预览图等
 3. 提交后机器人自动回复确认，维护者开始审核
 
 ### 4.3 提交 JSON 记录（审核通过后）
 
 1. Fork 仓库
 2. 在 `datasets/` 下新建 `{your-dataset-id}.json`（参考已有文件格式）
 3. 发起 PR → CI 自动校验 + 自动生成 `datasets.js` 和详情页
 4. 维护者 review 通过后合并 → 网站自动更新
 
 ---
 
 ## 五、技术要点备忘
 
 - `generate_datasets_js.py` 和 `generate_dataset_pages.py` 均从 JSON 全量重建，无增量逻辑，保证数据一致性
 - `git push origin HEAD:${{ github.head_ref }}` 解决 PR 事件下 detached HEAD 问题
 - `fetch-depth: 0` 确保完整分支元数据可用于 push
 - 邮件通知跳过 PR 事件（fork PR 无法访问仓库 secrets）
 - 所有生成脚本只依赖 Python 标准库，无第三方依赖
