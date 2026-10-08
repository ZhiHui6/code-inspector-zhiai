# Rust Rules

## 目录

- [适用范围](#适用范围)
- [所有权与错误](#所有权与错误)
- [并发与异步](#并发与异步)
- [unsafe 与 FFI](#unsafe-与-ffi)
- [验证](#验证)

## 适用范围

加载条件包括 `.rs`、`Cargo.toml`、`Cargo.lock` 和 workspace 配置。识别 edition、MSRV、feature、unsafe/FFI 和 async runtime。

## 所有权与错误

- `RUST-PANIC-001`：检查生产路径上的 `unwrap`/`expect`/索引 panic 是否能由外部输入触发；测试、不可达不变量和启动期硬失败需保留上下文。
- `RUST-ERROR-001`：检查 `Result`/`Option` 的错误转换、来源链、错误信息和调用方处理。
- `RUST-CLONE-001`：识别为绕过借用而产生的大对象 clone、隐式分配和锁内 clone；需有规模或热点证据。
- `RUST-COR-001`：检查整数溢出模式、UTF-8/字节边界、drop 顺序和取消时的部分状态。
- `RUST-ITER-001`：检查命令式索引循环是否可安全改为迭代器/`iter()` 链；不做纯风格判定，优先关注边界与 panic 风险。
- `RUST-LIFETIME-001`：检查生命周期标注是否可省略（编译器可推断时）或因过度借用导致不必要的复杂度；结合借用检查器输出判断。
- `RUST-ERRORLIB-001`：检查是否手工实现错误类型而不复用 `thiserror`/`anyhow` 等生态约定；仅在项目已引入或明确需要统一错误处理时建议。

## 并发与异步

- `RUST-ASYNC-001`：检查 async 中的阻塞 IO、runtime 混用、任务取消、join 错误和 backpressure。
- `RUST-CON-001`：检查 mutex/RwLock 持有时间、锁顺序、channel 关闭和 `Send`/`Sync` 边界。
- `RUST-ARC-001`：检查 `Arc<Mutex<>>`/`RwLock` 粒度是否过粗、是否可用更细粒度锁或消息传递替代；需有竞争或热点证据。

## unsafe 与 FFI

- `RUST-UNSAFE-001`：每个 unsafe 块都要有可验证的不变量、最小范围和安全封装；不能只因存在 unsafe 就判为漏洞。
- `RUST-FFI-001`：检查指针生命周期、布局、错误码、线程/异常边界和资源释放。

## 验证

优先运行 `cargo check`、`cargo test`、`cargo fmt --check`、`cargo clippy` 及项目声明的 audit 工具。遵循项目 MSRV 和 feature 组合，不擅自升级工具链。
