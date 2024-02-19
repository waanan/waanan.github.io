---
title: "第11章总结"
date: 2024-02-10T01:33:43+08:00
---

函数模板可能看起来相当复杂，但它们是一种非常强大的方法，可以使代码与不同类型的对象一起工作。在以后的章节中，我们将看到更多的模板内容。

***
## 章节回顾

函数重载允许我们创建具有相同名称的多个函数，只要每个同名函数具有不同的参数类型集（或者可以以其他方式区分函数）。这样的函数称为重载函数（简称重载）。返回类型不在区分范围内。

在解析重载函数时，如果找不到精确匹配，编译器将更喜欢可以通过数值提升匹配的重载函数，而不是那些需要数值转换的重载函数。当对已重载的函数进行函数调用时，编译器将基于函数调用中使用的参数，尝试将函数调用与适当的重载相匹配。这称为重载决议。

当编译器发现两个或多个函数可以与重载函数的函数调用相匹配，但无法确定哪一个是最佳的时，就会发生不明确的匹配。

默认参数是为函数参数提供的默认值。具有默认参数的参数必须始终是最右边的参数，并且在解析重载函数时，它们不用于区分函数。

函数模板允许我们创建类似函数的定义，该定义用作创建相关函数的模板。在函数模板中，我们使用模板类型参数作为以后要指定的任何类型的占位符。告诉编译器我们正在定义模板并声明模板类型的语法称为模板参数声明。

从函数模板（具有模板类型）创建函数（具有特定类型）的过程简称为函数模板实例化（或实例化）。当这个过程由于函数调用而发生时，它被称为隐式实例化。实例化的函数称为函数实例（或简称为实例，有时称为模板函数）。

模板参数推导允许编译器从函数调用的参数中推导出应用于实例化函数的实际类型。模板参数推导不进行类型转换。

模板类型有时称为泛型类型，使用模板进行编程有时称为泛型编程。

在C++20中，当auto关键字用作普通函数中的参数类型时，编译器将自动将函数转换为函数模板，每个auto参数都成为独立的模板类型参数。这种用于创建函数模板的方法称为简写函数模板。

非类型模板参数是具有固定类型的模板参数，它作为模板参数传入的constexpr值的占位符。

***

{{< prevnext prev="/basic/chapter11/func-template-none-type-param/" next="/" >}}
11.8 非类型模板参数
<--->
主页
{{< /prevnext >}}