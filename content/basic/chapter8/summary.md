---
title: "第八章总结"
date: 2024-01-02T10:33:49+08:00
---

***
## 章节回顾

CPU在程序中执行的特定语句序列称为程序的执行路径。直线运行程序每次运行时都采用相同的路径。

控制流语句允许更改正常的执行路径。当控制流语句导致程序开始执行某个非顺序指令序列时，这称为分支。

条件语句是指定是否应执行某些关联语句的语句。

If语句允许基于某个条件是否为真来执行关联的语句。如果关联的条件为false，则执行else语句。可以将多个if和else语句链接在一起。

当else语句连接到哪个if语句时不明确，就会出现悬空else。悬空else语句与同一块中最后一个无匹配的if语句匹配。可以通过将嵌套的if语句放置在代码块中来避免悬空的else语句。

空语句是仅由分号组成的语句。它什么也不做，并且在语言标准需要存在语句，但程序员不需要该语句来执行任何操作时使用。

Switch语句为在多个匹配项之间进行选择提供了一种更干净、更快的方法。Switch语句仅适用于整型。case标签用于标识要匹配的条件的值。如果找不到匹配的case标签，则执行default标签下的语句。

当从标签下的语句延续到后续标签下的语句时，这称为fallthrough。break语句（或return语句）可用于防止fallthrough。[[fallthrough]]属性可用于标记有意的fallthrough。

Goto语句允许程序向前或向后跳转到代码中的其他位置。通常应该避免使用它，因为这会创建出意大利面条代码，意味着程序的执行路径类似于一碗意大利面条。

只要给定的条件计算为true，循环允许程序重复执行某些语句。在循环执行之前会判断是否满足循环条件。

无限循环的循环条件始终为true。除非使用另一个控制流语句来停止，否则将永远循环。

循环变量（也称为计数器）是一个整数变量，用于计算循环已执行的次数。循环的每次执行都称为迭代。

Do-while循环类似于while循环，但条件是在循环执行之后进行判断的。

For循环是最常用的循环，当需要循环特定次数时，它是理想的。要注意，不要多迭代或少迭代一次。

Break语句允许中断switch、while、do-while或for循环。Continue语句允许立即移动到下一次循环迭代。

退出允许我们终止程序。正常终止是指程序以预期的方式退出（状态代码将指示它是否成功）。在main的末尾会自动调用std::exit()。或者也可以显式调用它来终止程序。它执行一些清理，但不清理任何局部变量，以及调用堆栈。

当程序遇到某种意外错误并必须关闭时，会发生异常终止。异常终止会调用std::abort。

算法是一个有限的指令序列，可以遵循它来解决某些问题或产生一些有用的结果。如果算法在调用之间保留了一些信息，则认为该算法是有状态的。相反，无状态算法不存储任何信息（并且必须在调用它时提供它所需的所有信息）。当应用于算法时，术语“状态”是指保存在有状态变量中的当前值。

如果对于给定的输入（为启动提供的值），算法始终产生相同的输出序列，则该算法被认为是确定性的。

伪随机数生成器（PRNG）是一种模拟随机数序列生成的算法。当实例化PRNG时，可以提供称为随机种子（或简称种子）的初始值（或一组值）来初始化PRNG的状态。当用种子初始化PRNG时，我们说它已经被播种。种子值的大小可以小于PRNG状态的大小。当这种情况发生时，我们说PRNG的种子不足。PRNG的输出结果开始自我重复之前的序列长度称为其周期。

随机数分布将PRNG的输出转换为其他一些数字分布。均匀分布是在两个数字X和Y（包括X和Y）之间以相等概率产生输出的随机数分布。

***

{{< prevnext prev="/basic/chapter8/random-global/" next="/basic/chapter9/intro/" >}}
8.14 全局随机数
<--->
9.0 代码测试简介
{{< /prevnext >}}
