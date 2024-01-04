---
title: "Constexpr if语句"
date: 2024-01-02T10:33:49+08:00
---

通常，if语句的条件在运行时求值。

然而，考虑条件是常量表达式的情况，例如在下面的示例中：

```C++
#include <iostream>

int main()
{
	constexpr double gravity{ 9.8 };

	// 提醒: 低精度的浮点数常量可以直接比较是否相等
	if (gravity == 9.8) // 常量表达式，结果永远为true
		std::cout << "Gravity is normal.\n";   // 永远会执行
	else
		std::cout << "We are not on Earth.\n"; // 不会执行到

	return 0;
}
```

由于gravity是constexpr，并用值9.8初始化，因此条件gravity==9.8的计算结果必须为true。因此，else语句将永远不会执行。

在运行时计算constexpr条件表达式是浪费的（因为结果永远不会变化）。将代码编译为永远无法执行的可执行文件也是浪费的。

***
## Constexpr if语句（C++17）

C++17引入了constexpr if语句，该语句要求条件是常量表达式。将在编译时计算constexpr if语句的条件表达式的结果。

如果constexpr条件的计算结果为true，则整个If-else将替换为true语句。如果constexpr条件的计算结果为false，则整个If-else将替换为false语句（如果存在else）或直接删除（如果没有else）。

要使用constexpr if语句，如下:

```C++
#include <iostream>

int main()
{
	constexpr double gravity{ 9.8 };

	if constexpr (gravity == 9.8) // 现在使用 constexpr if
		std::cout << "Gravity is normal.\n";
	else
		std::cout << "We are not on Earth.\n";

	return 0;
}
```

编译上述代码时，编译器将在编译时计算条件表达式，确认它始终为true，并仅保留单个语句std::cout << "Gravity is normal.\n";。

换句话说，它将编译以下内容：

```C++
int main()
{
	std::cout << "Gravity is normal.\n";

	return 0;
}
```

{{< alert success >}}
**最佳实践**

当条件表达式是常量表达式时，优先使用constexpr if语句。

{{< /alert >}}

***
## 现代编译器，与语句常量条件表达式的if语句（C++17）

出于优化目的，现代编译器通常将具有常量条件的非constexpr-if语句视为constexpr-if语句。然而，这并不意味着一定会这样做。

遇到具有常量条件的非constexpr-if语句，编译器可能会发出警告，建议您改用constexpr-if语句。这将确保发生编译时计算（即使禁用编译优化）。

***

{{< prevnext prev="/basic/chapter8/if-problem/" next="/" >}}
8.2 常见的if语句问题
<--->
主页
{{< /prevnext >}}
