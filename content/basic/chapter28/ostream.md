---
title: "使用ostream和ios输出"
date: 2025-03-02T00:53:53+08:00
---

在本节中，我们将研究iostream输出类（ostream）的各个方面。

***
## 插入运算符

插入运算符（<<）用于将信息放入输出流中。C++为所有内置数据类型预定义了插入操作，并且您已经看到了如何为自定义的类重载插入操作符。

在关于流的课程中，您看到istream和ostream都派生自一个名为ios的类。ios（和ios_base）的任务之一是控制输出的格式选项。

***
## 格式化

有两种方法可以更改格式选项：标志和操纵器。您可以将标志视为可以打开和关闭的布尔变量。操纵器是放置在流中的对象，影响事物的输入和输出方式。

要打开标志，请使用setf()函数，并将适当的标志作为参数。例如，默认情况下，C++不会在正数之前打印+号。然而，通过使用std::ios::showpos标志，我们可以更改此行为：

```C++
std::cout.setf(std::ios::showpos); // 打开 std::ios::showpos 标志
std::cout << 27 << '\n';
```

这将产生以下输出：

```C++
+27
```

可以使用 OR（|）运算符一次打开多个ios标志：

```C++
std::cout.setf(std::ios::showpos | std::ios::uppercase); // 打开 std::ios::showpos 和 std::ios::uppercase 标志
std::cout << 1234567.89f << '\n';
```

输出：

```C++
+1.23457E+06
```

要关闭标志，请使用unsetf()函数：

```C++
std::cout.setf(std::ios::showpos); // 打开 std::ios::showpos 标志
std::cout << 27 << '\n';
std::cout.unsetf(std::ios::showpos); // 关闭 std::ios::showpos 标志
std::cout << 28 << '\n';
```

这将产生以下输出：

```C++
+27
28
```

在使用setf()时，还有一点需要注意的技巧。许多标志属于同一组，称为格式组。格式组是一组执行类似（有时互斥）格式选项的标志。例如，名为“basefield”的格式组包含标志“oct”（八进制）、“dec”（十进制）和“hex”（十六进制），这些标志控制整数值的基数。默认情况下，设置“dec”标志。因此，如果我们这样做：

```C++
std::cout.setf(std::ios::hex); // 按16进制输出数字
std::cout << 27 << '\n';
```

我们得到以下输出：

```C++
27
```

这不工作！原因是因为setf()仅打开标志——它不够聪明，无法关闭互斥标志。因此，当我们打开std::hex时，std::ios::dec仍处于打开状态，而std:∶ios::dec显然优先级更高。有两种方法可以解决这个问题。

首先，我们可以关闭std::ios::dec，以便仅设置std::hex：

```C++
std::cout.unsetf(std::ios::dec); // 关闭十进制格式输出
std::cout.setf(std::ios::hex); // 打开十六进制格式输出
std::cout << 27 << '\n';
```

现在我们得到了预期的输出：

```C++
1b
```

第二种方法是使用不同形式的setf()，它接受两个参数：第一个参数是要设置的标志，第二个参数是它所属的格式化组。当使用这种形式的setf()时，属于该组的所有标志都被关闭，只有传入的标志被打开。例如：

```C++
// 设置 std::ios::hex 作为 std::ios::basefield 中的唯一标志
std::cout.setf(std::ios::hex, std::ios::basefield);
std::cout << 27 << '\n';
```

这也会产生预期的输出：

```C++
1b
```

使用setf()和unsetf()往往会很尴尬，因此C++提供了第二种更改格式选项的方法：操纵器。操纵器的好处是它们足够聪明，可以打开和关闭适当的标志。下面是使用一些操纵器更改基础的示例：

```C++
std::cout << std::hex << 27 << '\n'; // 按十六进制打印 27
std::cout << 28 << '\n'; // 任然在16进制模式下
std::cout << std::dec << 29 << '\n'; // 切换回10进制
```

该程序生成输出：

```C++
1b
1c
29
```

通常，使用操纵器比设置和取消设置标志容易得多。许多选项通过标志和操纵器都可用，然而，有些选项仅通过标志或操纵器可用，因此了解如何同时使用这两个选项非常重要。

***
## 有用的格式化方式

下面是一些更有用的标志、操纵器和成员函数的列表。标志存在于std::ios类中，操纵器存在于std命名空间中，成员函数存在于std::ostream类中。

| 标记  |  效果 |
| ----  | ----  |
| std::ios::boolalpha | 如果设置，则bool被打印为“true” 或 “false”，否则打印为 0 或 1 |


|  操纵器 | 效果  |
|  ----  | ----  |
| std::boolalpha | bool被打印为“true” 或 “false” |
| std::noboolalpha | bool被打印为 0 或 1 |

示例：

```C++
std::cout << true << ' ' << false << '\n';

std::cout.setf(std::ios::boolalpha);
std::cout << true << ' ' << false << '\n';

std::cout << std::noboolalpha << true << ' ' << false << '\n';

std::cout << std::boolalpha << true << ' ' << false << '\n';
```

结果：

```C++
1 0
true false
1 0
true false
```

| 标记  |  效果 |
| ----  | ----  |
| std::ios::showpos | 如果设置，正数前面会有一个 + 号 |

|  操纵器 | 效果  |
|  ----  | ----  |
| std::showpos | 正数前面会有一个 + 号  |
| std::noshowpos | 正数前面不会带 + 号 |


示例：

```C++
std::cout << 5 << '\n';

std::cout.setf(std::ios::showpos);
std::cout << 5 << '\n';

std::cout << std::noshowpos << 5 << '\n';

std::cout << std::showpos << 5 << '\n';
```

结果：

```C++
5
+5
5
+5
```

| 标记  |  效果 |
| ----  | ----  |
| std::ios::uppercase | 如果设置，使用大写字母 |

|  操纵器 | 效果  |
|  ----  | ----  |
| std::uppercase | 使用大写字母  |
| std::nouppercase | 使用小写字母 |

示例：

```C++
std::cout << 12345678.9 << '\n';

std::cout.setf(std::ios::uppercase);
std::cout << 12345678.9 << '\n';

std::cout << std::nouppercase << 12345678.9 << '\n';

std::cout << std::uppercase << 12345678.9 << '\n';
```

结果：

```C++
1.23457e+007
1.23457E+007
1.23457e+007
1.23457E+007
```

| 组 | 标记  |  效果 |
| ----  | ----  | ----  |
| std::ios::basefield | std::ios::dec | 按10进制打印数字（默认） |
| std::ios::basefield | std::ios::hex | 按16进制打印数字 |
| std::ios::basefield | std::ios::oct | 按8进制打印数字 |
| std::ios::basefield | (none) | 数字前导的格式打印 |

|  操纵器 | 效果  |
|  ----  | ----  |
| std::dec | 按10进制打印数字  |
| std::hex | 按16进制打印数字 |
| std::oct | 按8进制打印数字 |

示例：

```C++
std::cout << 27 << '\n';

std::cout.setf(std::ios::dec, std::ios::basefield);
std::cout << 27 << '\n';

std::cout.setf(std::ios::oct, std::ios::basefield);
std::cout << 27 << '\n';

std::cout.setf(std::ios::hex, std::ios::basefield);
std::cout << 27 << '\n';

std::cout << std::dec << 27 << '\n';
std::cout << std::oct << 27 << '\n';
std::cout << std::hex << 27 << '\n';
```

结果：

```C++
27
27
33
1b
27
33
1b
```

现在，您应该能够看到通过标志和通过操纵器设置格式之间的关系。在未来的示例中，我们将使用操纵器，除非它们不可用。

***
## 精度、符号和小数点

使用操纵器（或标志），可以更改显示浮点数的精度和格式。有几个格式选项以某种复杂的方式组合在一起，因此我们将更仔细地看一看。

如果使用固定或科学记数法，则精度决定分数中显示的小数位数。请注意，如果精度小于有效位数，则数字将四舍五入。

| 组 | 标记  |  效果 |
| ----  | ----  | ----  |
| std::ios::floatfield | std::ios::fixed | 按10进制打印浮点数 |
| std::ios::floatfield | std::ios::scientific | 按科学计数法打印浮点数 |
| std::ios::floatfield | (none) | 位数少，使用10进制打印，位数多，使用科学计数法 |
| std::ios::floatfield | std::ios::showpoint | 永远展示小数点 |

|  操纵器 | 效果  |
|  ----  | ----  |
| std::fixed | 按10进制打印  |
| std::scientific | 按科学计数法打印 |
| std::showpoint | 永远展示小数点 |
| std::noshowpoint | 取消showpoint选项 |
| std::setprecision(int) | 设置打印精度 |

| 成员函数 | 效果  |
|  ----  | ----  |
| std::ios_base::precision() | 返回当前设置的打印精度 |
| std::ios_base::precision(int) | 设置新的打印精度，并返回旧的打印精度 |

```C++
std::cout << std::fixed << '\n';
std::cout << std::setprecision(3) << 123.456 << '\n';
std::cout << std::setprecision(4) << 123.456 << '\n';
std::cout << std::setprecision(5) << 123.456 << '\n';
std::cout << std::setprecision(6) << 123.456 << '\n';
std::cout << std::setprecision(7) << 123.456 << '\n';

std::cout << std::scientific << '\n';
std::cout << std::setprecision(3) << 123.456 << '\n';
std::cout << std::setprecision(4) << 123.456 << '\n';
std::cout << std::setprecision(5) << 123.456 << '\n';
std::cout << std::setprecision(6) << 123.456 << '\n';
std::cout << std::setprecision(7) << 123.456 << '\n';
```

产生结果：

```C++
123.456
123.4560
123.45600
123.456000
123.4560000

1.235e+002
1.2346e+002
1.23456e+002
1.234560e+002
1.2345600e+002
```

如果既不使用fixed数字，也不使用科学数字，则精度决定应显示多少有效数字。同样，如果精度小于有效位数，则该数字将四舍五入。

```C++
std::cout << std::setprecision(3) << 123.456 << '\n';
std::cout << std::setprecision(4) << 123.456 << '\n';
std::cout << std::setprecision(5) << 123.456 << '\n';
std::cout << std::setprecision(6) << 123.456 << '\n';
std::cout << std::setprecision(7) << 123.456 << '\n';
```

产生以下结果：

```C++
123
123.5
123.46
123.456
123.456
```

使用showpoint操纵器或标志，可以使流写入小数点和尾随零。

```C++
std::cout << std::showpoint << '\n';
std::cout << std::setprecision(3) << 123.456 << '\n';
std::cout << std::setprecision(4) << 123.456 << '\n';
std::cout << std::setprecision(5) << 123.456 << '\n';
std::cout << std::setprecision(6) << 123.456 << '\n';
std::cout << std::setprecision(7) << 123.456 << '\n';
```

产生以下结果：

```C++
123.
123.5
123.46
123.456
123.4560
```

下面是一个包含更多示例的汇总表：

|  选项 | 精度  | 12345.0 | 	0.12345  |
|  ----  | ----  |  ----  | ----  |
| Normal | 3 | 1.23e+004 | 0.123 |
| Normal | 4 | 1.235e+004 | 0.1235 |
| Normal | 5 | 12345 | 0.12345 |
| Normal | 6 | 12345 | 0.12345 |
| Showpoint | 3 | 1.23e+004 | 0.123 |
| Showpoint | 4 | 1.235e+004 | 0.1235 |
| Showpoint | 5 | 12345. | 0.12345 |
| Showpoint | 6 | 12345.0 | 0.123450 |
| Fixed | 3 | 12345.000 | 0.123 |
| Fixed | 4 | 12345.0000 | 0.1235 |
| Fixed | 5 | 12345.00000 | 0.12345 |
| Fixed | 6 | 12345.000000 | 0.123450 |
| Scientific | 3 | 1.235e+004 | 1.235e-001 |
| Scientific | 4 | 1.2345e+004 | 1.2345e-001 |
| Scientific | 5 | 1.23450e+004 | 1.23450e-001 |
| Scientific | 6 | 1.234500e+004 | 1.234500e-001 |

***
## 宽度、填充字符和对齐

通常，在打印数字时，不考虑其周围的空间。然而，可以向左或向右调整数字的打印，来让上下对齐。为了做到这一点，我们必须首先定义字段宽度，它定义了值将具有的输出空间。如果实际打印的数字小于字段宽度，则它将左对齐或右对齐（按规定）。如果实际数字大于字段宽度，则不会截断它——它将溢出。

| 组 | 标记  |  效果 |
| ----  | ----  | ----  |
| std::ios::adjustfield | std::ios::internal | 符号左对齐，数字右对齐 |
| std::ios::adjustfield | std::ios::left | 左对齐 |
| std::ios::adjustfield | std::ios::right | 右对齐 |

|  操纵器 | 效果  |
|  ----  | ----  |
| std::internal | 符号左对齐，数字右对齐  |
| std::left | 左对齐 |
| std::right | 右对齐 |
| std::setfill(char) | 将参数，设置为填充字符 (在 iomanip 头文件定义) |
| std::setw(int) | 设置输入输出宽度（在 iomanip 头文件定义） |

|  成员函数 | 效果  |
|  ----  | ----  |
| std::basic_ostream::fill() | 返回当前填充字符  |
| std::basic_ostream::fill(char) | 设置填充字符，并返回之前的填充字符 |
| std::ios_base::width() | 返回字段宽度 |
| std::ios_base::width(int) | 设置字段宽度，并返回之前的字段宽度 |

为了使用这些格式化程序中的任何一个，我们首先必须设置字段宽度。这可以通过width(int)成员函数或setw()操纵器来完成。请注意，默认设置为右对齐。

```C++
std::cout << -12345 << '\n'; // 未设置字段宽度
std::cout << std::setw(10) << -12345 << '\n'; // 设置字段宽度
std::cout << std::setw(10) << std::left << -12345 << '\n'; // 左对齐
std::cout << std::setw(10) << std::right << -12345 << '\n'; // 右对齐
std::cout << std::setw(10) << std::internal << -12345 << '\n'; // internally 对齐
```

这将产生以下结果：

```C++
-12345
    -12345
-12345
    -12345
-    12345
```

需要注意的一点是setw()和width()仅影响下一个输出语句。它们不像其他一些标志/操纵器那样是持久的。

现在，让我们设置填充字符并执行相同的示例：

```C++
std::cout.fill('*');
std::cout << -12345 << '\n'; // 未设置字段宽度
std::cout << std::setw(10) << -12345 << '\n'; // 设置字段宽度
std::cout << std::setw(10) << std::left << -12345 << '\n'; // 左对齐
std::cout << std::setw(10) << std::right << -12345 << '\n'; // 右对齐
std::cout << std::setw(10) << std::internal << -12345 << '\n'; // internally 对齐
```

这将产生输出：

```C++
-12345
****-12345
-12345****
****-12345
-****12345
```

请注意，字段中的所有空格都已用填充字符填充。

ostream类和iostream库包含其他可能有用的输出函数、标志和操纵器，具体取决于您需要执行的操作。与istream类一样，这些适合使用时查找对应的手册。

***