# Go Rules

## 目录

- [适用范围](#适用范围)
- [语言规则](#语言规则)
- [Web 与数据库](#web-与数据库)
- [验证](#验证)

## 适用范围

加载条件包括 `.go`、`go.mod`、`go.work` 和 Go CI 配置。识别 Go 版本、模块边界、生成代码和 build tags。

## 语言规则

- `GO-ERROR-001`：检查 error 是否被忽略、是否丢失上下文、是否错误比较类型，以及调用方是否处理可恢复/不可恢复失败。
- `GO-CONTEXT-001`：请求、数据库和外部调用应传播 context；不要把 context 存进长期对象，也不要用 nil context。
- `GO-CONC-001`：检查 goroutine 的启动、退出、取消、channel 关闭和 backpressure，识别泄漏与重复消费。
- `GO-RACE-001`：检查共享 map/切片、懒初始化和闭包变量；有条件时使用 race detector 验证。
- `GO-RESOURCE-001`：检查 response body、文件、rows、ticker、listener 和锁的释放，特别是循环中的 defer。
- `GO-COR-001`：检查 nil interface、slice/map 语义、错误后的部分写入、整数溢出和时间处理。
- `GO-HTTP-001`：客户端和服务端应有超时、大小上限、取消和状态码处理。
- `GO-PERF-001`：检查循环内 IO、无界 goroutine/缓存、重复编码和不必要复制；不要仅凭“多一次分配”报告问题。
- `GO-BUILDER-001`：循环内字符串拼接的主规则见 `PERF-CONCAT-001`；Go 中优先使用 `strings.Builder`/`bytes.Buffer`，小规模或常量拼接不报。
- `GO-SLICE-001`：检查已知大小时 slice/map 是否预分配容量、循环内是否重复分配；只在规模或热点明确时报告。

## Web 与数据库

- `GO-HTTP-AUTH-001`：核对中间件顺序、对象级授权、请求体限制和敏感日志。
- `GO-SQL-001`：使用参数化查询，检查 rows/transaction 生命周期、N+1 和迁移锁风险。

## 验证

优先使用 `go test`、`go vet`、项目声明的静态分析和必要的 `-race`。命令不存在或环境不支持时如实记录。
