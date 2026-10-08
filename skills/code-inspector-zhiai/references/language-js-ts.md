# JavaScript and TypeScript Rules

## 目录

- [适用范围与版本](#适用范围与版本)
- [类型与契约](#类型与契约)
- [语言语义](#语言语义)
- [异步、并发与资源](#异步并发与资源)
- [安全](#安全)
- [Node.js 与服务端框架](#nodejs-与服务端框架)
- [浏览器与前端框架](#浏览器与前端框架)
- [模块、依赖与构建](#模块依赖与构建)
- [测试与验证](#测试与验证)

## 适用范围与版本

加载条件包括 `.js`、`.jsx`、`.mjs`、`.cjs`、`.ts`、`.tsx`、`.mts`、`.cts`、`package.json`、`tsconfig*.json` 或对应构建配置。先识别 Node/浏览器/Bun/Deno 运行时、模块系统、TypeScript 版本、包管理器、框架版本和项目 lint/formatter 规则。同一仓库可能同时存在服务端、客户端、SSR、worker 和构建脚本，分别检查其信任边界。

## 类型与契约

- `TS-CONFIG-001`：读取实际生效的 `extends` 链和 project references，核对 `strict`、模块解析、JSX、lib、target 和 emit 设置。只有能证明配置掩盖缺陷时才建议收紧选项，不机械要求一次性启用全部严格标志。
- `TS-TYPE-001`：检查 `any` 扩散、双重断言、非空断言、未收窄的 `unknown`、宽泛索引签名和 `@ts-ignore` 是否越过真实边界。测试夹具和第三方类型缺口可作为局部例外。
- `TS-CONTRACT-001`：检查可辨识联合、泛型约束、重载、可选字段与 `undefined`、readonly 和错误类型是否与运行时数据一致；公共函数与导出 API 应显式声明返回类型，避免推断漂移或意外暴露内部类型；类型通过不等于外部 JSON、环境变量或 DOM 数据已验证。
- `TS-BOUNDARY-001`：在 HTTP、消息、数据库、localStorage、文件和反序列化边界执行运行时 schema 校验，并保留拒绝路径；不要在可信内部对象上重复校验。
- `TS-API-001`：检查导出类型、声明文件、package exports 和生成客户端是否保持向后兼容，特别关注枚举、联合类型和 optional/nullable 变化。

## 语言语义

- `JS-COR-001`：检查 `null`/`undefined`、NaN、负零、BigInt、浮点精度、时区、truthy/falsy 和隐式字符串/数字转换。`value == null` 等有意写法需结合 lint 和语义判断。
- `JS-OBJECT-001`：检查对象/数组浅拷贝、原型继承、getter 副作用、可变 key、稀疏数组、`sort` 原地修改和遍历期间修改集合。
- `JS-CLOSURE-001`：检查闭包捕获、`this` 绑定、循环变量、模块级可变状态和前端 stale closure；必须指出实际异步或生命周期路径。
- `JS-ERROR-001`：检查 throw 非 Error 值、错误 cause 丢失、同步/异步错误通道混用和业务失败被转换为成功返回。
- `JS-REGEX-001`：对不可信长输入检查灾难性回溯、无界匹配和错误 Unicode 假设；只有可构造输入与复杂度证据时报告 ReDoS。
- `JS-MODERN-001`：检查严格相等（`===`/`!==`）以及可被现代语法（可选链、空值合并）简化的冗余判断；可变性声明偏好（`const`/`let`/`var`）见门控的 `STYLE-CONST-001`；仅在项目未由 lint/formatter 统一约束时报告。
- `JS-ARRAY-001`：检查数组/迭代方法是否与意图一致（`map`/`filter`/`reduce`/`forEach`/`for...of`），避免为副作用使用 `map`、在 `forEach` 中 `await`、忽略 `reduce` 初值；不做纯风格判定。
- `JS-PROMISE-001`：检查深层 Promise 链、回调地狱、混用 `then` 与 `async/await` 造成的错误通道割裂；优先统一为 `async/await`，同时保留必要的并发语义。
- `JS-OPTCHAIN-001`：检查可选链/空值合并是否被滥用而导致逻辑静默失败（该报错时返回 `undefined`、`??` 掩盖缺失配置）；需能指出实际被掩盖的错误路径。

## 异步、并发与资源

- `JS-ASYNC-001`：检查 Promise 是否被 await、return 或显式处理，是否存在 floating promise、遗失 rejection、异步回调未等待和错误上下文丢失。不要把所有回调机械改成 `async/await`。
- `JS-CONC-001`：检查 `Promise.all` 的 fail-fast/部分成功语义、无界并发、重复提交、乱序响应覆盖新状态和共享缓存竞态；需要有幂等、限流或版本戳的证据。
- `JS-CANCEL-001`：检查 AbortSignal 是否从请求/组件传播到 fetch、数据库、流和子任务，取消后是否仍写状态或继续消耗资源。
- `JS-RESOURCE-001`：检查事件监听器、定时器、订阅、WebSocket、MessagePort、observer、文件句柄和流在成功、异常与卸载路径都能清理。
- `JS-STREAM-001`：检查 Node/Web streams 的 error、backpressure、pipeline 结束、Body 大小限制和 partial read，不要把缓冲整个输入作为默认实现。

## 安全

- `JS-XSS-001`：从 URL、表单、消息和存储追踪数据到 `innerHTML`、模板、DOM URL、脚本和 CSS sink，区分 HTML/属性/URL/JS 上下文编码；仅“包含字符串”不能证明 XSS。
- `JS-INJECT-001`：检查 SQL/NoSQL、命令、路径、模板、header、日志和动态 import 拼接，优先参数化、固定映射和 allowlist。
- `JS-PROTOTYPE-001`：检查深合并、动态属性赋值和对象反序列化是否允许 `__proto__`、`constructor` 或 `prototype` 污染；确认库版本和对象创建方式。
- `JS-SSRF-001`：检查可控 URL 的 scheme、DNS/IP、重定向、代理和云元数据访问；必须证明输入可达服务端网络请求。
- `JS-AUTH-001`：核对路由/handler 的认证、对象级授权、租户隔离、CSRF/CORS/Cookie 属性和默认拒绝，不能只因存在全局中间件就判定安全。
- `JS-SERIALIZE-001`：检查不可信对象的 schema、原型、日期/大整数、循环引用和敏感字段；不要用 `JSON.parse(JSON.stringify(...))` 作为通用深拷贝或安全过滤。

## Node.js 与服务端框架

- `NODE-TIMEOUT-001`：外部 HTTP、数据库、队列、DNS、子进程和流必须有可解释的超时、取消、并发与大小上限。
- `NODE-ERROR-001`：检查 Express/Nest/Fastify/Koa 中间件错误链、stream `error`、后台任务 rejection 和进程级异常策略；进程级 handler 不能代替请求级恢复。
- `NODE-PROCESS-001`：检查 graceful shutdown、连接停止接收、任务 drain、退出码、signal 和 worker/child process 生命周期。
- `NODE-API-001`：检查请求 schema、状态码、错误模型、上传限制、分页、幂等键和响应中敏感字段。框架 DTO 类型不能替代运行时验证。
- `NODE-DATA-001`：在 Prisma/TypeORM/Sequelize/Mongoose 等数据层检查 N+1、未分页查询、事务边界、批量写入、mass assignment 和模型钩子副作用。
- `NODE-CACHE-001`：检查缓存键是否包含租户/权限/版本，失效是否一致，值和 key 数量是否有界，失败时是否绕过安全校验。

## 浏览器与前端框架

- `UI-LIFECYCLE-001`：检查 effect/watch/subscription 的依赖、清理、取消和竞态；不要仅凭 lint 警告断言功能错误。
- `UI-STATE-001`：检查基于旧值的更新、直接变异、派生状态重复存储、稳定 key、表单受控状态和异步结果覆盖。
- `UI-SSR-001`：检查服务端/客户端初始值、浏览器专属 API、随机数/时间、认证状态和数据缓存导致的 hydration 或跨请求泄漏。
- `UI-ACCESS-001`：检查语义、键盘、焦点、标签、错误提示、加载/空状态和动态更新通知；只在真实交互代码适用。
- `UI-RENDER-001`：检查大列表、重复请求、昂贵计算和 context/store 广播；必须结合 profiler、依赖路径或输入规模，不能机械添加 memo。
- `UI-PERF-001`：检查高频事件的防抖/节流、图片/静态资源懒加载与压缩；长列表、昂贵计算与缓存见 `UI-RENDER-001`；结合真实交互频率与输入规模，不机械添加 memo/debounce。
- `REACT-HOOK-001`：检查 Hook 调用顺序、effect 依赖/清理、并发渲染下副作用、Suspense/transition 失败状态和 server/client component 边界。
- `VUE-REACTIVITY-001`：检查 ref/reactive 解包、watch flush/cleanup、computed 副作用、组件作用域资源和 SSR 状态隔离。
- `ANGULAR-RX-001`：检查 Observable 订阅释放、错误通道、switch/merge/concat 语义、change detection、DI scope 和 route guard 不能代替服务端授权。

## 模块、依赖与构建

- `JS-MODULE-001`：检查 ESM/CJS、条件 exports、default/named import、循环依赖、side effect import、top-level await 和动态 import 错误边界。
- `JS-BUILD-001`：检查浏览器/服务端环境变量隔离、source map 暴露、tree-shaking side effects、SSR bundle 和 polyfill/target 兼容性。
- `JS-DEP-001`：核对 lockfile 与包管理器、直接依赖来源、脚本生命周期和 workspace 边界；未使用依赖的通用判定见 `MAINT-UNUSED-001`；漏洞结论必须来自实际版本和审计证据。

## 测试与验证

- `JS-TEST-001`：检查异步断言是否被等待、fake timer/microtask 是否正确推进、mock 是否复位、snapshot 是否掩盖行为以及 jsdom 与真实浏览器差异。
- `JS-TEST-002`：安全、并发、SSR、路由和数据库问题优先添加边界或集成测试；只测实现细节的 mock 不能证明真实契约。

优先读取项目 scripts 和 CI，再运行现有的 lint、`tsc --noEmit`/typecheck、单元测试、浏览器测试和构建。记录 Node、TypeScript、包管理器、模块系统及实际配置；没有配置时，不把某个工具的默认规则当成项目标准。
