# Python Rules

## 目录

- [适用范围](#适用范围)
- [语言规则](#语言规则)
- [Web 与数据框架](#web-与数据框架)
- [验证](#验证)

## 适用范围

加载条件包括 `.py`、`pyproject.toml`、`setup.cfg`、`requirements*.txt`、`Pipfile` 或 `poetry.lock`。读取 Python 版本、async 使用方式、类型检查配置和测试入口。

## 语言规则

- `PY-COR-001`：检查可变默认参数、浅拷贝/深拷贝、迭代器一次性消费、时区和 `Decimal`/浮点混用。只在参数或状态确实跨调用共享时报告可变默认值。
- `PY-REL-001`：检查 `except:`/过宽异常、空 `except`、异常上下文丢失和错误返回值混用。测试中的故意捕获需结合断言判断。
- `PY-RESOURCE-001`：文件、锁、连接、临时目录和生成器资源应使用 context manager 或等价的 `finally` 生命周期。
- `PY-SEC-001`：检查 `eval`/`exec`、不可信 `pickle`/yaml、`subprocess` shell 拼接、路径和 SQL 插值；说明输入来源和 sink。
- `PY-TYPE-001`：检查 `Any` 扩散、未标注公共边界、`cast` 滥用和运行时校验缺失。数据解析边界可使用 `TypedDict`、dataclass 或验证库，但不要为了注解而重写内部代码。
- `PY-ASYNC-001`：在 async 函数中寻找阻塞 IO、同步锁、未 await 的 coroutine 和任务泄漏；确认 event loop 生命周期。
- `PY-GIL-001`：检查 CPU 密集任务误用线程（受 GIL 限制）应改用多进程或 native 扩展，以及 async 中混入阻塞调用；只在确有并发场景时报告。
- `PY-PERF-001`：检查循环内查询/HTTP、全量读取大文件、重复正则编译和不必要的对象复制；列表推导式不是一律优于 `map`/生成器。
- `PY-COMPREHENSION-001`：检查列表推导式/生成器与 `map`/`filter` 的取舍是否影响可读性或内存峰值；列表推导式不是无条件缺陷，不一律判优或判劣。
- `PY-PACKAGE-001`：检查依赖范围、导入副作用、启动时执行外部操作和配置默认值。
- `PY-STYLE-001`：检查现代惯用法（`f-string`、`dataclasses`、`@property`）与类型标注一致性；f-string 与格式化风格不得作为无条件缺陷，仅在用户显式要求风格维度时按门控给出偏好提示。

## Web 与数据框架

- `DJANGO-SEC-001`：检查 CSRF、对象级授权、模板自动转义、ORM 参数化、文件上传和管理端暴露。
- `DJANGO-PERF-001`：检查 queryset N+1、未分页列表、事务范围和信号副作用。
- `FASTAPI-CONTRACT-001`：检查 Pydantic 输入/输出模型、认证依赖、异常响应和 async/sync 路由边界。
- `DATA-RESOURCE-001`：检查数据库游标、连接池、事务、批量写入和 pandas/NumPy 的内存峰值。

## 验证

优先运行项目现有的 pytest、ruff/flake8、mypy/pyright、bandit 或构建命令。不要把 f-string、列表推导式或某种格式化风格当成无条件缺陷。
