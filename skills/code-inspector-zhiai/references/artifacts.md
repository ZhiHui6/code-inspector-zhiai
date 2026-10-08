# Data, API, Script, Configuration, and Infrastructure Rules

## 目录

- [SQL 与迁移](#sql-与迁移)
- [GraphQL 与 OpenAPI](#graphql-与-openapi)
- [HTML/CSS 与 Web 标记](#htmlcss-与-web-标记)
- [Schema 与序列化](#schema-与序列化)
- [Shell 与 PowerShell](#shell-与-powershell)
- [配置文件](#配置文件)
- [Docker](#docker)
- [Kubernetes 与 Helm](#kubernetes-与-helm)
- [Terraform](#terraform)
- [CI/CD](#cicd)
- [验证](#验证)

## SQL 与迁移

- `SQL-SEC-001`：确认应用输入使用参数化查询，动态标识符使用 allowlist；仅看到字符串拼接时需继续追踪输入来源。
- `SQL-COR-001`：检查 NULL、时区、精度、排序稳定性、重复行和 JOIN 基数语义。
- `SQL-TX-001`：检查事务隔离、锁顺序、部分提交、重试和外部副作用。
- `SQL-PERF-001`：使用执行计划、索引、行数估计和真实访问模式判断全表扫描、N+1、低效分页和重复聚合。
- `SQL-MIG-001`：检查迁移可逆性、表锁、长事务、非空字段默认值、索引在线创建、回填和多版本应用兼容。
- `SQL-DATA-001`：优先依赖数据库约束维护唯一性、外键和范围不变量；检查应用校验与数据库约束是否冲突。

不要在未知数据库方言和版本下断言某语法或索引策略可用。

## GraphQL 与 OpenAPI

- `OPENAPI-SCHEMA-001`：检查删除/重命名字段、必填化、枚举扩展、默认值和错误响应的兼容性。
- `GRAPHQL-SEC-001`：检查字段级授权、深度/复杂度限制、批量查询和 introspection 暴露策略。
- `GRAPHQL-PERF-001`：检查 resolver N+1、DataLoader 生命周期、缓存键和分页。
- `OPENAPI-CONTRACT-001`：核对实现与 schema 的状态码、content type、nullable、format、分页和错误模型。
- `API-GEN-001`：生成客户端/服务端代码通常只读；优先修复 schema 或生成配置。

## HTML/CSS 与 Web 标记

- `WEB-SEC-001`：检查输出编码、危险 URL scheme、内联脚本、CSP/安全头和模板上下文；不要把静态文案误判为注入。
- `WEB-ACCESS-001`：检查语义元素、表单 label、键盘焦点、错误提示、对比度和动态内容通知。
- `WEB-CSS-001`：检查布局溢出、断点、堆叠上下文、选择器冲突和 `prefers-reduced-motion`；视觉建议必须有可观察的交互或可用性影响。
- `WEB-COMPAT-001`：检查浏览器 API、polyfill、SSR hydration 和资源加载失败的降级路径。

## Schema 与序列化

- `SCHEMA-COMPAT-001`：protobuf/Avro/JSON Schema 等变更不得复用已发布字段编号或破坏未知字段处理。
- `SCHEMA-VALIDATION-001`：检查 schema 校验是否真正应用在信任边界，错误是否返回稳定且不泄露内部信息。

## Shell 与 PowerShell

- `SHELL-QUOTE-001`：检查变量引用、数组参数、路径空格、通配符和命令替换，避免参数注入和单词拆分。
- `SHELL-ERROR-001`：检查退出码、pipeline 错误、trap/finally、临时文件清理和部分成功。不要机械添加 `set -e`，先确认脚本控制流。
- `SHELL-SECRET-001`：不要在参数、日志、process list 或调试输出中暴露凭据。
- `SHELL-PATH-001`：使用已解析的明确路径执行删除、移动和递归操作；检查 symlink、根目录和空变量风险。
- `PS-ERROR-001`：检查 PowerShell 的 terminating/non-terminating error、`-LiteralPath`、`$ErrorActionPreference` 和外部命令退出码。

## 配置文件

- `CONFIG-SECRET-001`：识别硬编码秘密、默认口令和敏感日志，但必须脱敏值。
- `CONFIG-DEFAULT-001`：检查缺失键、类型、环境覆盖、feature flag 默认值和开发/生产差异。
- `CONFIG-SCHEMA-001`：使用 schema 或官方工具验证 YAML/JSON/TOML；注意 YAML 隐式类型、锚点和重复键。
- `CONFIG-COMPAT-001`：检查配置重命名、弃用和滚动升级期间的新旧版本兼容。

## Docker

- `DOCKER-BASE-001`：检查基础镜像来源、不可变 tag/digest、支持周期和构建上下文。
- `DOCKER-SEC-001`：检查非 root 用户、能力、秘密挂载、敏感层、文件权限和网络暴露。
- `DOCKER-SIZE-001`：检查多阶段构建、缓存顺序和不必要文件；镜像大小优化不能牺牲可复现性。
- `DOCKER-RUNTIME-001`：检查入口信号、健康检查、只读文件系统、资源/临时目录和 shutdown。

## Kubernetes 与 Helm

- `K8S-SEC-001`：检查 service account、RBAC、privileged、hostPath、capability、secret 和网络策略。
- `K8S-REL-001`：检查 readiness/liveness/startup probe、滚动策略、PDB、资源 requests/limits 和优雅退出。
- `K8S-CONFIG-001`：检查 selector/label、namespace、service port、配置挂载和 Helm values 默认值。
- `K8S-DATA-001`：检查持久卷、StatefulSet 身份、备份和不可逆变更。

## Terraform

- `TF-STATE-001`：检查 state backend、锁、敏感输出和资源导入/移动计划。
- `TF-SEC-001`：检查公开网络、宽泛 IAM、未加密存储、秘密变量和 provider 凭据。
- `TF-LIFE-001`：检查 `prevent_destroy`、replace、依赖、漂移和生产资源的销毁风险。
- `TF-VERSION-001`：固定 Terraform/provider/module 兼容版本并保留锁文件；不要无请求升级。

## CI/CD

- `CI-SEC-001`：检查第三方 action/image 固定、pull request 秘密边界、脚本注入和最小 token 权限。
- `CI-COR-001`：检查缓存键、矩阵覆盖、条件表达式、失败传播和产物来源。
- `CI-DEPLOY-001`：检查环境审批、并发部署、回滚、不可变产物和生产变量隔离。

## 验证

优先使用数据库 explain/migration dry-run、schema validator、ShellCheck/PSScriptAnalyzer、Docker/Compose 检查、Kubernetes/Helm dry-run、Terraform fmt/validate/plan 和 CI 官方校验。任何 plan、迁移或集群命令都必须确认不会写入远程或生产状态。
