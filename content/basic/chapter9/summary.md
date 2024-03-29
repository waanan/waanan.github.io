---
title: "第9章总结"
date: 2024-01-17T13:13:14+08:00
---

***
## 章节回顾

项目进程中新增或变更的需求,导致项目范围超出最初的计划和预算,这又称需求蔓延（Scope creep）。

软件验证是测试软件在所有情况下是否按预期工作的过程。单元测试是一种测试，旨在单独测试代码的一小部分（通常是函数或调用），以确保特定行为按预期发生。单元测试框架可以帮助您组织单元测试。集成测试，测试一组单元的集成，以确保它们正常工作。

代码覆盖率是指在测试时执行了多少源代码。语句覆盖率是指程序中已由测试例程执行的语句的百分比。分支覆盖率是指测试例程已执行的分支的百分比。循环覆盖（也称为0、1、2测试）意味着，如果您有一个循环，则应该确保它在迭代0次、1次和2次时正常工作。

快乐路径（happy path）是在没有遇到错误时发生的执行路径。故障路径（sad path）是发生错误或故障状态的执行路径。不可恢复错误（也称为致命错误）是一种严重到程序无法继续运行的错误。良好的处理错误情况的程序是健壮的。

缓冲区是为在数据从一个位置移动到另一个位置时临时存储数据而预留的内存。

检查用户输入是否符合程序期望的过程称为输入验证。

cerr是一个输出流（如std::cout），旨在用于输出错误消息。

先决条件是在执行某些代码段之前必须始终为true的任何条件。不变量是在执行某个组件时必须为true的条件。后置条件是在执行某些代码后必须始终为true的任何条件。

断言是一个表达式，除非程序中存在错误，否则该表达式将为真。在C++中，运行时断言通常使用断言预处理器宏来实现。断言通常在非调试代码中关闭。static_assert是在编译时计算的断言。

断言应该用于记录逻辑上不可能的情况。错误处理应用于处理可能发生问题的情况。

***

{{< prevnext prev="/basic/chapter9/assert/" next="/basic/chapter10/implicit-type-convert/" >}}
9.5 断言
<--->
10.0 隐式类型转换
{{< /prevnext >}}
