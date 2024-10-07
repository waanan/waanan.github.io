---
title: "右值引用"
date: 2024-08-23T14:54:42+08:00
---

在前面，我们引入了值范畴的概念（左值和右值），这是表达式的一个属性，有助于确定表达式是否解析为值、函数或对象。我们还引入了左值和右值，以便我们可以讨论左值引用。

***
## 左值引用概述

在C++11之前，C++中只存在一种类型的引用，因此它被称为“引用”。然而，在C++11中，它被称为左值引用。左值引用只能用可修改的左值初始化。

|  左值引用  |  可以被初始化  |  可以被赋值 |
|  ----  | ----  | ----  |
| 可修改的左值 | 是 | 是 |
| 不可修改的左值 | 否 | 否 |
| 右值 | 否 | 否 |

常量对象的左值引用可以用可修改和不可修改的左值和右值进行初始化。然而，不能修改这些值。

|  const左值引用  |  可以被初始化  |  可以被赋值 |
|  ----  | ----  | ----  |
| 可修改的左值 | 是 | 否 |
| 不可修改的左值 | 是 | 否 |
| 右值 | 是 | 否 |

常量对象的左值引用特别有用，因为它们允许我们将任何类型的参数（左值或右值）传递到函数中，而无需复制参数。

***
## 右值引用

C++11添加了一种新的引用类型，称为右值引用。右值引用是设计为（仅）使用右值初始化的引用。使用单个与符号创建左值引用时，使用双与符号创建右值引用：

```C++
int x{ 5 };
int& lref{ x }; // 使用左值 x 初始化左值引用
int&& rref{ 5 }; // 使用右值 5 初始化右值引用
```

右值引用不能用左值初始化。

R值引用有两个有用的属性。首先，r值引用将其初始化对象的寿命延长到r值引用的寿命（对常量对象的l值引用也可以这样做）。其次，非常量r值引用允许您修改r值！

让我们看一些例子：

```C++
#include <iostream>
 
class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };
 
public:
	Fraction(int numerator = 0, int denominator = 1) :
		m_numerator{ numerator }, m_denominator{ denominator }
	{
	}
 
	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1)
	{
		out << f1.m_numerator << '/' << f1.m_denominator;
		return out;
	}
};
 
int main()
{
	auto&& rref{ Fraction{ 3, 5 } }; // r-value reference to temporary Fraction
	
	// f1 of operator<< binds to the temporary, no copies are created.
	std::cout << rref << '\n';
 
	return 0;
} // rref (and the temporary Fraction) goes out of scope here
```

该程序打印：

作为匿名对象，Fraction（3，5）通常会在定义它的表达式末尾超出范围。然而，由于我们用它初始化r值引用，因此它的持续时间被延长到块的末尾。然后，我们可以使用该r-value引用来打印Fraction的值。

现在，让我们看一个不太直观的示例：

```C++
#include <iostream>

int main()
{
    int&& rref{ 5 }; // because we're initializing an r-value reference with a literal, a temporary with value 5 is created here
    rref = 10;
    std::cout << rref << '\n';

    return 0;
}
```

该程序打印：

虽然用文本值初始化r-value引用，然后能够更改该值似乎很奇怪，但当用文本初始化r-value引用时，临时对象是从文本构造的，因此引用引用的是临时对象，而不是文本值。

R值引用并不经常以上述任何一种方式使用。

***
## R值引用作为功能参数

R值引用通常用作函数参数。当您希望l值和r值参数具有不同的行为时，这对于函数重载最有用。

```C++
#include <iostream>

void fun(const int& lref) // l-value arguments will select this function
{
	std::cout << "l-value reference to const: " << lref << '\n';
}

void fun(int&& rref) // r-value arguments will select this function
{
	std::cout << "r-value reference: " << rref << '\n';
}

int main()
{
	int x{ 5 };
	fun(x); // l-value argument calls l-value version of function
	fun(5); // r-value argument calls r-value version of function

	return 0;
}
```

这将打印：

可以看到，当传递l值时，重载函数解析为具有l值引用的版本。当传递r-value时，重载函数解析为具有r-value引用的版本（这被认为比l-value引用与const更好的匹配）。

你为什么要这么做？我们将在下一课中更详细地讨论这一点。不用说，它是移动语义的重要组成部分。

***
## R值引用变量是左值

请考虑以下片段：

```C++
	int&& ref{ 5 };
	fun(ref);
```

您希望上面的函数称为哪个版本的fun：fun（const int&）或fun（int&&）？

答案可能会让你吃惊。这称为fun（const int&）。

尽管变量ref的类型为int&&，但在表达式中使用时，它是一个左值（与所有命名变量一样）。对象的类型及其值类别是独立的。

您已经知道，literal 5是int类型的右值，而int x是int类型中的左值。类似地，int&&ref是int&&类型中的左值。

因此，fun（ref）不仅调用fun（constint&），它甚至不匹配fun（int&&），因为rvalue引用不能绑定到左值。

***
## 返回r值引用

您几乎不应该返回r-value引用，因为同样的原因，您几乎不应返回l-value引用。在大多数情况下，当被引用对象在函数末尾超出范围时，您将最终返回挂起引用。

***
