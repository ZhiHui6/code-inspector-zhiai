# Additional Language Rules

## 目录

- [PHP](#php)
- [Ruby](#ruby)
- [Swift 与 Objective-C](#swift-与-objective-c)
- [Dart 与 Flutter](#dart-与-flutter)
- [Scala 与 Elixir](#scala-与-elixir)
- [验证](#验证)

## PHP

- `PHP-SEC-001`：检查 SQL/命令/路径注入、输出编码、CSRF、会话 cookie、文件上传和反序列化。
- `PHP-TYPE-001`：检查 `strict_types`、外部输入验证、隐式类型转换和 null 语义。
- `LARAVEL-PERF-001`：在 Laravel 中检查 mass assignment、策略授权、ORM N+1、队列幂等和配置缓存边界。

## Ruby

- `RUBY-SEC-001`：检查 SQL/模板/命令注入、强参数、反序列化和秘密日志。
- `RUBY-REL-001`：检查异常边界、事务、后台任务重试和资源释放。
- `RAILS-PERF-001`：检查 ActiveRecord N+1、未分页查询、回调副作用和迁移锁。

## Swift 与 Objective-C

- `SWIFT-LIFE-001`：检查强制解包、可选值边界、retain cycle、delegate 注销和资源生命周期。
- `SWIFT-CON-001`：检查 MainActor/UI 线程、actor 隔离、Task 取消和共享状态。
- `OBJC-MEM-001`：检查手动内存管理、block 捕获、指针和 Objective-C 异常/错误边界。

## Dart 与 Flutter

- `DART-ASYNC-001`：检查未处理 Future、取消、stream subscription 和 isolate 边界。
- `FLUTTER-LIFE-001`：检查 controller、focus、animation 和 subscription 的 `dispose`。
- `FLUTTER-RENDER-001`：检查 build 中副作用、大列表、稳定 key 和 UI 线程阻塞。

## Scala 与 Elixir

- `SCALA-COR-001`：检查 `Option`/`Either`/`Try` 的错误路径、Future 执行上下文、可变集合和隐式转换边界。
- `SCALA-PERF-001`：检查集合惰性/物化、并行集合和 Spark 转换是否符合数据规模与执行计划。
- `ELIXIR-CON-001`：检查 process/supervision 生命周期、消息积压、状态隔离和 mailbox 中的未处理消息。
- `ELIXIR-DATA-001`：检查 pattern matching、Ecto changeset、事务和 SQL 参数化是否覆盖异常路径。

Lua、R 及其他未列出的语言先应用通用规则和制品规则；只有发现明确语法证据并加载对应扩展包后，才提出语言特定结论。

## 验证

按项目声明运行 Composer/PHPUnit/PHPStan、Bundler/RSpec/RuboCop/Brakeman、Swift test/Xcode 构建或 Dart/Flutter test/analyzer。工具缺失时只报告静态证据和未验证项。
