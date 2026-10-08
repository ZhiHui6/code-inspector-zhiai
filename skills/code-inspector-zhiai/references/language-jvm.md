# Java and Kotlin Rules

## 目录

- [适用范围与版本](#适用范围与版本)
- [Java 语义与类型](#java-语义与类型)
- [异常与资源](#异常与资源)
- [并发与现代运行时](#并发与现代运行时)
- [安全与序列化](#安全与序列化)
- [Spring 与服务边界](#spring-与服务边界)
- [JPA/Hibernate 与数据](#jpahibernate-与数据)
- [性能](#性能)
- [Kotlin 互操作](#kotlin-互操作)
- [构建、测试与验证](#构建测试与验证)

## 适用范围与版本

加载条件包括 `.java`、`.kt`、`.kts`、`pom.xml`、Gradle 文件、Maven/Gradle wrapper、Android 构建文件或 JVM 配置。识别实际 JDK release/toolchain、Kotlin/JVM target、Spring/Jakarta 代际、模块边界、annotation processor 和静态分析配置。版本不明时不要建议只在新 JDK 可用的 API；多模块仓库分别确认各模块设置。

## Java 语义与类型

- `JAVA-EQUALITY-001`：核对 `equals`/`hashCode`/`compareTo` 一致性、数组比较、BigDecimal 值/尺度语义、实体身份和可变 map/set key。只有实际进入比较或哈希容器时报告。
- `JAVA-NULL-001`：检查 nullable 边界、自动拆箱、反射/框架注入、空集合语义和 Optional 的返回/字段/参数误用；不要把 Optional 机械扩散到所有模型。
- `JAVA-GENERIC-001`：检查 raw type、unchecked cast、heap pollution、泛型数组、通配符边界和反射类型擦除造成的契约缺口。
- `JAVA-MUTABLE-001`：检查内部可变集合泄漏、防御性复制、不可变对象中的可变字段、record 成员和 builder 重用。
- `JAVA-COR-001`：检查整数溢出、精度、时区/locale、charset、正则、字符串解析和 switch/enum 的未知值路径。
- `JAVA-API-001`：检查 public API、record/DTO、枚举、序列化字段和异常类型的二进制/源代码/数据兼容性。

## 异常与资源

- `JAVA-ERROR-001`：检查过宽捕获、空 catch、重新抛出时丢失 cause、checked/unchecked 边界、finally 覆盖异常和业务失败被返回为成功。
- `JAVA-RESOURCE-001`：检查文件、stream、JDBC、锁、executor、HTTP body 和临时资源的所有路径；优先 try-with-resources，并关注 suppressed exception。
- `JAVA-INTERRUPT-001`：捕获 `InterruptedException` 后应恢复中断状态或明确结束任务；不要静默吞掉取消信号。
- `JAVA-RETRY-001`：检查重试上限、退避、异常筛选、幂等性、事务和重复外部副作用。

## 并发与现代运行时

- `JAVA-JMM-001`：检查共享可变状态的安全发布、volatile/atomic/锁语义、复合操作和 happens-before；线程安全集合不能自动保证跨操作原子性。
- `JAVA-EXECUTOR-001`：检查线程池/队列上限、拒绝策略、异常可见性、关闭等待和任务取消。不要在库代码中无依据使用 common pool。
- `JAVA-FUTURE-001`：检查 CompletableFuture 的 executor、异常链、超时、取消、组合顺序和阻塞 join/get；异步返回不能掩盖失败。
- `JAVA-LOCK-001`：检查锁顺序、锁内 IO、读写锁升级、condition 循环和资源获取失败后的释放。
- `JAVA-SYNC-001`：检查是否过度使用 `synchronized`（可用 `java.util.concurrent` 原子类/并发集合/显式锁替代）、锁粒度是否过粗；不做纯风格判定，需有并发语义或热点证据。
- `JAVA-VTHREAD-001`：仅在目标 JDK 支持时检查 virtual thread 的无界外部资源、synchronized/native pinning、ThreadLocal 成本和结构化生命周期；不要机械把所有 executor 改成虚拟线程。
- `JAVA-CONTEXT-001`：检查 MDC、安全上下文、事务和租户信息在线程池、异步回调和虚拟线程之间的传播与清理。

## 安全与序列化

- `JAVA-INJECT-001`：追踪输入到 SQL/JPQL、命令、模板、日志、LDAP、SpEL/表达式和脚本引擎，优先参数化和固定映射。
- `JAVA-SSRF-001`：检查 URL scheme、重定向、DNS/IP、代理和云元数据访问，并证明不可信输入可达网络 sink。
- `JAVA-PATH-001`：检查路径规范化、zip slip、上传文件名、临时文件权限和符号链接边界。
- `JAVA-XML-001`：检查 XML parser 的外部实体、DOCTYPE、schema 和资源上限；结合具体 parser/JDK 默认值，避免版本误报。
- `JAVA-DESER-001`：检查原生序列化、Jackson polymorphic typing、XStream/Kryo 等类型允许范围和 gadget 暴露；不能只因使用 Jackson 就判为不安全。
- `JAVA-AUTH-001`：核对 endpoint/method/object 层授权、租户隔离、CSRF/CORS/session/token 和默认拒绝。
- `JAVA-DATA-001`：日志、异常、trace 和序列化输出不得泄露 token、个人数据、连接串或完整请求体。

## Spring 与服务边界

- `SPRING-TX-001`：检查 `@Transactional` 的代理可见性、自调用、传播、只读语义、回滚异常、异步边界和外部副作用。
- `SPRING-PROXY-001`：检查 `@Async`、`@Cacheable`、`@Secured` 等代理注解是否因 final/private/self-invocation 或对象创建方式失效。
- `SPRING-CONTRACT-001`：检查 DTO 与实体隔离、Bean Validation 是否真正触发、错误响应、分页、文件上传、幂等键和 API 版本兼容。
- `SPRING-ERROR-001`：检查 controller advice、状态码、异常映射、敏感详情和 trace ID；不要将所有异常统一返回 200。
- `SPRING-WEBFLUX-001`：只在 WebFlux/reactive 路径检查阻塞 JDBC/IO、subscribe 调用、背压、context 和错误恢复；MVC 项目不套用 reactive 规则。
- `SPRING-CONFIG-001`：检查 profile、property precedence、秘密、默认值、actuator 暴露和滚动升级期间的配置兼容。
- `SPRING-RESILIENCE-001`：检查 HTTP/消息调用的超时、连接池、重试、熔断、bulkhead 和重复消费幂等性。

## JPA/Hibernate 与数据

- `JPA-IDENTITY-001`：检查实体 equals/hashCode 与持久化身份、代理、生命周期和集合成员关系，避免 ID 分配前后语义变化。
- `JPA-PERF-001`：检查 N+1、lazy loading 越界、错误 fetch join、entity graph、未分页查询和序列化触发查询；用 SQL/统计或调用路径佐证。
- `JPA-TX-001`：检查事务范围、flush 时机、乐观锁/version、悲观锁、隔离和数据库约束，避免仅靠应用层先查后写。
- `JPA-BATCH-001`：检查批量写入的 batch 配置、flush/clear、内存增长和部分失败；不要在小数据量上强制批处理。
- `JPA-CASCADE-001`：检查 cascade、orphanRemoval、双向关系维护和删除范围，防止意外级联或孤儿数据。
- `JPA-PAGE-001`：检查排序稳定性、offset/keyset 选择、collection fetch join 分页和 count 查询成本。
- `JDBC-RESOURCE-001`：检查参数化查询、statement/result set 生命周期、事务提交/回滚和连接池泄漏。

## 性能

- `JAVA-PERF-001`：检查热路径装箱、重复分配、循环内字符串拼接（见 `PERF-CONCAT-001`）、正则编译、反射和重复序列化；必须有输入规模、profile 或基准依据。
- `JAVA-STREAM-001`：检查 stream 重用、副作用、短路、collector 并发属性和 `parallelStream` common pool；普通循环与 stream 之间不做纯风格判定。
- `JAVA-CACHE-001`：检查缓存 key、租户/权限、过期、最大容量、stampede 和失败缓存；不把缓存作为无测量的默认优化。
- `JAVA-COLLECTION-001`：集合初始容量、实现类型和并发结构只有在规模或语义明确时报告，不能机械要求预分配。

## Kotlin 互操作

- `KOTLIN-NULL-001`：检查 `!!`、平台类型、可空链和默认值是否掩盖 Java nullable 契约。
- `KOTLIN-COROUTINE-001`：检查 coroutine scope、structured concurrency、取消传播、阻塞调用 dispatcher 和 Java future 互操作。
- `KOTLIN-STATE-001`：检查 data class、不可变集合、共享状态、默认参数和 Java 序列化/框架代理兼容。

## 构建、测试与验证

- `JVM-BUILD-001`：检查 Maven/Gradle wrapper、toolchain/release、依赖 scope/configuration、BOM/convergence、插件/annotation processor 版本和可复现构建；不要无请求升级依赖。
- `JAVA-TEST-001`：检查 JUnit 异常/异步断言、时间与随机性、Mockito 过度 mock、Spring slice 边界、数据库清理和并发测试是否真实失败。
- `JAVA-TEST-002`：事务、授权、序列化、迁移和消息问题优先使用集成/契约测试；Testcontainers 等工具只在项目已有依赖或用户授权时使用。

优先使用仓库 wrapper 和 CI 中的 Maven/Gradle test、compile/check、静态分析与格式命令；常见工具包括 Error Prone、SpotBugs、PMD、Checkstyle、JaCoCo 和依赖审计。记录 JDK、toolchain、profile、模块和测试选择；没有版本或配置依据时，不套用特定 Spring/JDK 规则。
