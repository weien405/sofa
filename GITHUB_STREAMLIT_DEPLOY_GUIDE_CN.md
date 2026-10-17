# 创伤SOFA-2预测网站：GitHub与Streamlit Community Cloud部署指南

本指南面向没有网站部署经验的研究者。当前压缩包是**不含冻结模型的公开源码包**。在未取得PhysioNet及所需机构书面许可前，不得把模型上传至GitHub、Streamlit或其他第三方云平台，也不得把仅显示HOLD提示的网页宣传为已经可用的预测器。

## 一、部署前需要准备的内容

1. GitHub账号及登录状态。
2. Streamlit Community Cloud账号及登录状态。
3. 本部署包ZIP及解压工具。
4. 书面模型托管许可。许可必须明确覆盖拟采用的第三方模型存储方式和公众推理接口。
5. 必要的研究负责人、机构数据治理、隐私、网络安全及法律/技术转化审批。

当前冻结模型的SHA-256必须为：

`ef4917e9dd145e1699d2dac644798ac24fad8f2b67bc5a2fd80b2f2f12479bf1`

## 二、解压并检查GitHub上传包

1. 将ZIP解压到一个空文件夹。
2. 打开解压目录，确认`app.py`和`requirements.txt`直接位于根目录，不能再多套一层无关文件夹。
3. 确认`.streamlit/config.toml`、`config/`、`tests/`和说明文件仍保持原目录结构。
4. 确认目录中没有`.pkl`、`.pickle`、`.joblib`、患者数据、数据库密码或Secrets。
5. 当前代码包缺少模型时启动网页会显示授权HOLD提示，这是正确行为；它不会生成虚假概率。

## 三、在GitHub创建独立仓库

1. 登录GitHub，点击右上角“+”，选择“New repository”。
2. Repository name填写：`trauma-sofa2-trajectory-predictor`。
3. 建议在准备阶段先选择Private。只有完成全部授权审核后，再决定是否公开源码或更改可见性。
4. 不要勾选自动生成README、`.gitignore`或License，以免与本包已有文件冲突。
5. 点击“Create repository”。
6. 在新仓库页面选择“uploading an existing file”。
7. 上传ZIP解压后的全部文件和文件夹，而不是上传ZIP本身。
8. 核对`app.py`位于仓库根目录，并保留以点开头的`.streamlit`文件夹。
9. 提交前再次确认没有模型二进制文件、患者数据、`.streamlit/secrets.toml`或访问令牌。
10. 填写提交说明，例如`Prepare code-only Streamlit deployment package`，然后提交。

注意：创建Private仓库并不能自动解决PhysioNet权限问题。Streamlit读取Private仓库中的模型仍属于第三方托管，必须先获得明确许可。

## 四、在Streamlit Community Cloud连接仓库

只有在已具备相应授权，或仅准备展示不含预测功能的HOLD页面时，才继续本步骤。

1. 打开https://share.streamlit.io/并登录。
2. 点击“Create app”或“New app”。
3. 选择“Deploy from GitHub”。
4. Repository选择`weien405/trauma-sofa2-trajectory-predictor`。
5. Branch选择`main`。
6. Main file path填写`app.py`。
7. 打开“Advanced settings”。
8. Python version选择3.12。不要使用未经测试的其他版本。
9. 本项目不需要API密钥。不要在Secrets中粘贴GitHub密码、PhysioNet账号或患者信息。
10. 在拥有合法模型托管方案前，不要通过Secrets、Base64文本或下载脚本绕过模型限制。

## 五、模型文件配置

### 当前未获授权时

不要上传模型。部署代码后，页面应显示模型尚未配置及公开推理被暂停。此页面不是可用预测器，不应对外宣传。

### 获得书面许可后

必须按照许可指定的托管方式执行。应用默认查找：

`model/XGBoost_FINAL_TRAINING_ONLY_PIPELINE.pkl`

如果许可允许把模型放入部署仓库，需要先由数据治理人员书面确认，并移除`.gitignore`中对应的阻止规则。提交前计算SHA-256并确认完全一致。

如果许可要求使用受控模型存储，应由具备相应权限的技术人员配置。Streamlit运行环境中的`SOFA2_TRAUMA_MODEL_PATH`必须指向已经安全取得的模型文件，而不是研究者本机Windows路径。

不得以改名、压缩分卷、Base64编码或代码内嵌方式绕过模型共享限制。

## 六、点击Deploy

1. 核对Repository、Branch、Main file path和Python版本。
2. 点击“Deploy”。
3. 页面进入构建状态后等待依赖安装。
4. 如果仅部署代码包且没有模型，构建应成功，但网页会显示HOLD提示。
5. 只有模型按照合法方式配置、哈希校验通过并完成合成病例验证后，才可称为正常预测网站。

## 七、上线后的检查

1. 复制Streamlit生成的公网网址。
2. 退出账号或使用浏览器无痕窗口访问，确认访客不需要登录。
3. 分别使用电脑和手机访问，检查标题、14项输入及说明文字。
4. 使用预先批准的人工合成病例测试，不得上传MIMIC或eICU逐患者数据。
5. 核对云端合成病例概率与本地预计算值一致。
6. 确认页面不输出死亡风险、四分类概率、治疗建议或临床阈值。
7. 确认错误信息不显示服务器路径、Secrets或异常堆栈。
8. 确认应用没有提供数据文件上传、模型上传或患者身份字段。
9. 保存网站URL、GitHub提交SHA、模型SHA-256、Python版本、依赖版本和验证截图。

## 八、获取网站URL

部署成功后，浏览器地址栏中的`https://...streamlit.app/`地址即为最终网站URL。将该地址记录到README、模型卡和论文补充材料前，应先完成匿名访问和合规审核。

## 九、常见失败及排查

### 1. ModuleNotFoundError或依赖安装失败

- 在Streamlit应用管理页面打开“Manage app”或日志页面。
- 确认`requirements.txt`位于仓库根目录。
- 确认只保留一个主要Python依赖文件。
- 确认Python版本选择3.12。
- 不要在查看测试结果后随意升级XGBoost、scikit-learn或NumPy。

### 2. 页面提示模型尚未配置

这是当前无模型公开源码包的预期行为。不要用随机模型或重新训练模型替代。取得授权后，再按照批准的路径配置正式模型。

### 3. SHA-256 mismatch

说明模型文件不是正式STEP20冻结版本，或文件在传输中发生变化。停止部署，重新核对文件来源和哈希；不得关闭哈希校验。

### 4. Pickle或版本兼容错误

- 核对Python 3.12及`requirements.txt`中的固定版本。
- 确认加载的是完整冻结pipeline，而不是单独的XGBoost对象。
- 不要重新保存模型来掩盖兼容问题，除非重新保存行为经过完整一致性验证和审计。

### 5. 构建成功但网页空白或不断重启

- 查看Streamlit日志的第一条真实错误。
- 核对入口文件为`app.py`。
- 核对模型和静态资源的大小写及相对路径。
- 不要在日志或GitHub Issue中粘贴Secrets、患者数据或本地隐私路径。

### 6. GitHub仓库在Streamlit中看不到

- 确认Streamlit已获得访问对应GitHub仓库的权限。
- 对Private仓库，只授权必要仓库，不要扩大到无关项目。
- 重新载入仓库列表；不要把账号令牌写入代码。

## 十、维护原则

- 任何模型、特征、插补器或阈值变化都视为新版本，不能直接覆盖现有文件。
- 每次更新记录GitHub commit SHA、模型SHA-256和QA结果。
- 不记录访客输入、预测概率或可识别信息。
- 授权、PhysioNet规则或Streamlit数据处理政策变化时，重新执行合规审核。
- 发现哈希错误、隐私风险或授权撤回时，应立即停止公开服务。

