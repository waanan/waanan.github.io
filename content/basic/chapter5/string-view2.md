---
title: "std::string_view（第2部分）"
date: 2023-11-28T13:19:42+08:00
---

在前面的课程中，我们介绍了两种字符串类型: std::string 和 std::string_view。

因为std::string_view是我们第一次遇到view类型，所以我们将花费一些额外的时间来进一步讨论它。我们将重点介绍如何安全地使用std::string_view，并提供一些示例来说明如何错误地使用它。最后，我们将给出一些关于何时使用std::string vs std::string_view的准则。

***
## 所有者和查看者

让做一个类比。假设你决定画一幅自行车的画。但你没有自行车！你该怎么办？

嗯，你可以去当地的自行车商店买一辆。你会拥有那辆自行车的。这有一些好处:你现在有一辆自行车，你可以骑。你可以保证自行车在你想要的时候随时可用。你可以装饰它，或者移动它。这种选择也有一些缺点。自行车很贵。如果你买了一个，你现在就要对它负责。你必须定期维护它。当你最终决定不再需要它时，你必须妥善处理它。

所有权可能很昂贵。作为所有者，您有责任获取、管理和正确处置您拥有的对象。

在你走出房子的路上，你瞥了一眼窗前。你注意到你的邻居把自行车停在你窗户对面。你可以只画一张你邻居的自行车的照片（从你的窗户看）。这种选择有许多好处。你节省了购买自己自行车的费用。你不必维护它。你也不负责处理它。当你看完后，你可以关上窗帘，继续你的生活。这将结束对象的查看，但对象本身不受此影响。这种选择也有一些潜在的缺点。你不能油漆或定制你的邻居的自行车。当你观看自行车时，你的邻居可能会决定改变自行车的外观，或者将其完全移出你的视野。你可能最终会看到一些意想不到的东西。

观看成本较低。作为查看器，您对正在查看的对象没有责任，但您也不能控制这些对象。

***
## std::string是所有者

您可能想知道为什么std::string会构造其初始值设置项的昂贵副本。实例化对象时，为该对象分配内存，以存储其整个生命周期中需要使用的任何数据。该内存是为对象保留的，并保证只要对象存在，该内存就会存在。这是一个安全的空间。string（和大多数其他对象）将它们被赋予的初始化值复制到此内存中，以便它们可以有自己的独立值供以后访问和操作。一旦复制了初始化值，对象就不再以任何方式依赖于初始值设定项。

这是一件好事，因为初始化完成后，初始化设定值通常不能被信任。如果将初始化过程想象为初始化对象的函数调用，那么谁在传递初始化设定值？函数调用方。初始化完成后，控制逻辑返回给调用方。此时，初始化语句已完成，通常会发生以下两种情况之一:

1. 如果初始值设定项是临时值或对象，则该临时值将立即销毁。
2. 如果初始值设定项是变量，则调用方仍然可以访问该对象。然后，调用者可以对象上执行任何他们想要的操作，包括修改或销毁它。


因为std::string自己制作值的副本，所以它不必担心初始化完成后会发生什么。可以销毁或修改初始值设定项，它不会影响std::string。缺点是这种独立性伴随着昂贵的副本成本。

在我们的类比中，std::string是所有者。它有自己管理的数据。当它被摧毁时，它会自己清理。

***
## 我们并不总是需要副本

让我们重新回顾上一课中的示例:

```C++
#include <iostream>
#include <string>

void printString(std::string str) // str 拷贝了传入的值
{
    std::cout << str << '\n';
}

int main()
{
    std::string s{ "Hello, world!" };
    printString(s);

    return 0;
}
```

当调用printString(s) 时，str生成s的昂贵副本。该函数打印复制的字符串，然后销毁它。

请注意，s已经保存了要打印的字符串。我们可以只使用保存的字符串，而不是复制吗？我们需要评估三个条件:

1. 在str仍在使用时，是否可以销毁s？不，str在函数的末尾死亡，s存在于调用方的作用域中，并且不能在函数返回之前销毁。
2. 在str仍在使用时能否修改s？不，str在函数末尾死亡，并且调用方在函数返回之前没有机会修改s。
3. str是否以调用方不期望的方式修改字符串？不，该函数根本不会修改字符串。

由于所有这三个条件都是 否，因此制作副本没有风险。既然字符串副本很昂贵，为什么要为我们不需要的副本付费呢？

***
## std::string_view是查看器

string_view采用不同的初始化方法。std::string_view创建字符串的廉价视图，而不是制作字符串的昂贵副本。初始化完成后，可以使用std::string_view来访问对应的字符串。

在我们的类比中，std::string_view是一个查看器。它查看已存在于其他位置的对象，并且不能修改该对象。当视图被销毁时，正在查看的对象不受影响。

需要注意的是，std::string_view在其生存期内仍然依赖于初始值设定项。如果正在查看的字符串在查看器仍在使用时被修改或销毁，则将导致意外或未定义的行为。

无论何时使用查看器，都要确保这些可能性不会发生。

查看已销毁的字符串的std::string_view有时称为悬空视图（dangling view）。

{{< alert success >}}
**警告**

视图查看的结果取决于正在查看的对象。如果正在查看的对象在视图在使用时被修改或销毁，将导致意外或未定义的行为。

{{< /alert >}}

***
## std::string_view最好用作只读函数参数

std::string_view的最佳用途是作为只读函数参数。这允许我们在不进行复制的情况下传入C样式的字符串、std::string或std::string_view参数，因为std::string_view将创建该参数的视图。

```C++
#include <iostream>
#include <string>
#include <string_view>

void printSV(std::string_view str) // std::string_view, 只是传入参数的一个视图
{
    std::cout << str << '\n';
}

int main()
{
    printSV("Hello, world!"); // 使用c样式字符串调用

    std::string s2{ "Hello, world!" };
    printSV(s2); // 使用 std::string 调用

    std::string_view s3 { s2 };
    printSV(s3); // 使用 std::string_view 调用
       
    return 0;
}
```

由于str函数参数是在返回调用方之前创建、初始化、使用和销毁的，因此str参数，不会有正在查看的字符串修改或销毁的风险。

***
## 错误使用std::string_view

让我们看一看滥用std::string_view会给我们带来麻烦的一些情况。

下面是我们的第一个示例:

```C++
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string_view sv{};

    { // 创建了一个嵌套的代码块
        std::string s{ "Hello, world!" }; // 创建了一个局部的 std::string
        sv = s; // sv 现在是s 的一个视图
    } // s 被销毁, sv 目前查看的是非法的 字符串

    std::cout << sv << '\n'; // 未定义的行为

    return 0;
}
```

在这个例子中，我们在嵌套块中创建std::string s 。然后将sv设置为s的视图，变量s在代码块的末尾被销毁。sv不知道s已经被摧毁了。当使用sv时，我们访问的是无效的对象，以及未定义的行为结果。

这是同一问题的另一个变体，使用函数的返回值初始化std::string_view

```C++
#include <iostream>
#include <string>
#include <string_view>

std::string getName()
{
    std::string s { "Alex" };
    return s;
}

int main()
{
  std::string_view name { getName() }; // name 使用函数的返回值初始化
  std::cout << name << '\n'; // 未定义的行为

  return 0;
}
```

这与前面的示例类似。getName() 函数返回包含字符串“Alex”的std::string。返回值是临时对象，在包含函数调用的完整表达式的末尾被销毁。我们必须立即使用该返回值，或者复制它以供以后使用。

但std::string_view不会进行复制。相反，它为临时返回值创建一个视图。这使得std::string_view悬而未决（查看无效对象），并且打印视图会导致未定义的行为。

以下是上述的不太明显的变体:

```C++
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    using namespace std::string_literals;
    std::string_view name { "Alex"s }; // "Alex"s 创建了一个临时的 std::string
    std::cout << name << '\n'; // 未定义的行为

    return 0;
}
```

string字面值（通过s后缀创建）创建临时std::string对象。因此在本例中，"Alex"s 创建了一个临时的std::string，然后将其用作name的初始值设定项。然后销毁临时std::string，留下悬空的name。当使用name变量时，会得到未定义的行为。

{{< alert warning >}}
**警告**

不要使用std::string字面值来初始化std::string_view。使用c样式字符串变量或字面值，std::string变量,std::string_view变量或字面值均可。

{{< /alert >}}

当修改正在查看的字符串时，也会获得未定义的行为:

```C++
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string s { "Hello, world!" };
    std::string_view sv { s }; // sv 正在查看 s

    s = "Hello, universe!";    // 修改 s, 会使 sv 无效 (s 仍然有效)
    std::cout << sv << '\n';   // 未定义的行为

    return 0;
}
```

在本例中，sv设置为s的视图。然后修改s。当修改std::string时，该std::string中的所有视图都将无效。使用无效的视图将导致未定义的行为。因此，当打印sv时，会产生未定义的行为。

{{< alert success >}}
**关键点**

修改std::string会使该std::string中的所有视图无效。

{{< /alert >}}

***
## 使失效的std::string_view恢复正常

无效的对象通常可以通过将其设置回已知的良好状态来重新生效。对于无效的std::string_view，我们可以为无效的std::string_view对象分配一个有效的字符串。

下面是与前面相同的示例，但我们将使sv重新生效:

```C++
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string s { "Hello, world!" };
    std::string_view sv { s }; // sv 现在查看 s

    s = "Hello, universe!";    // 修改 s, 会使 sv 无效 (s 仍然有效)
    std::cout << sv << '\n';   // 未定义的行为

    sv = s;                    // 使 sv 重新生效: sv 再次查看 s
    std::cout << sv << '\n';   // 打印 "Hello, universe!"

    return 0;
}
```

在通过修改s使sv无效后，我们通过语句 sv = s，使得sv再次成为s的有效视图。当我们第二次打印sv时，它会打印“Hello，universe！”。

***
## 请小心返回std::string_view

std::string_view可以用作函数的返回值。然而，这通常是危险的。

由于局部变量在函数末尾被销毁，如果std::string_view是局部变量的一个视图，返回的std::string_view是无效的，并且进一步使用该std::string_view将导致未定义的行为。例如:

```C++
#include <iostream>
#include <string>
#include <string_view>

std::string_view getBoolName(bool b)
{
    std::string t { "true" };  // 局部变量
    std::string f { "false" }; // 局部变量

    if (b)
        return t;  // 返回变量t的视图

    return f; // 返回变量f的视图
} // t与f在函数结束失效

int main()
{
    std::cout << getBoolName(true) << ' ' << getBoolName(false) << '\n'; // 未定义的行为

    return 0;
}
```

在上面的示例中，当调用getBoolName(true)时，函数返回正在查看t的std::string_view。然而，t在函数末尾被销毁。这意味着返回的std::string_view正在查看已销毁的对象。因此，当打印返回的std::string_view时，会产生未定义的行为。

编译器可能会警告您此类情况，也可能不会警告您。

在两种主要情况下，可以安全地返回std::string_view。

首先，因为C样式的字符串在整个程序执行期间均有效，因此可以从返回类型为std::string_view的函数中返回C样式的串文本。

```C++
#include <iostream>
#include <string_view>

std::string_view getBoolName(bool b)
{
    if (b)
        return "true";  // 返回 "true" 的视图

    return "false"; // 返回 "false" 的视图
} // "true" and "false" 在函数结尾不会失效

int main()
{
    std::cout << getBoolName(true) << ' ' << getBoolName(false) << '\n'; // ok

    return 0;
}
```

这将打印:

```C++
true false
```

当调用getBoolName(true) 时，函数将返回一个std::string_view，查看C样式的字符串“true”。因为整个程序都存在“true”，所以当我们使用返回的std::string_view在main() 中打印“true“时没有问题。

其次，通常可以返回类型为std::string_view的函数参数

```C++
#include <iostream>
#include <string>
#include <string_view>

std::string_view firstAlphabetical(std::string_view s1, std::string_view s2)
{
    if (s1 < s2)
        return s1;
    return s2;
}

int main()
{
    std::string a { "World" };
    std::string b { "Hello" };

    std::cout << firstAlphabetical(a, b) << '\n'; // 打印 "Hello"

    return 0;
}
```

可能不太明显为什么代码ok。首先，注意参数a和b存在于调用者的作用域中。调用函数时，函数参数s1是a的视图，函数参数s2是b的视图。当函数返回s1或s2时，它将视图返回到a或b，并返回给调用者。由于此时a和b仍然存在，因此返回的std::string_view可能正在查看a或b。

这里有一个重要的微妙之处。如果参数是临时对象（将在包含函数调用的完整表达式末尾销毁），则函数返回的std::string_view值则必须在同一表达式中使用。在表达式结束之后，临时对象会被销毁，std::string_view处于悬空状态。

{{< alert success >}}
**警告**

如果参数是临时参数，并且在包含函数调用的完整表达式的末尾被销毁，则必须立即使用返回的std::string_view，因为在临时参数被销毁后，它将保持悬空状态。

{{< /alert >}}

***
## 查看修改功能

考虑一下你家的窗户，看着一辆停在街上的汽车。你可以透过窗户看到汽车，但你不能触摸或移动汽车。您的车窗仅提供汽车的视图，这是一个完全独立的对象。

许多窗户都有窗帘，这使我们可以修改我们的视野。我们可以关闭左侧或右侧帘幕，以减少我们可以看到的内容。我们不会改变外面的东西，我们只是减少可见区域。

因为std::string_view是一个视图，所以它包含一些函数，可以让我们通过“关闭窗帘”来修改视图。这不会以任何方式修改正在查看的字符串，只会修改视图本身。

1. remove_prefix() 成员函数从视图的左侧删除字符。
2. remove_suffix() 成员函数从视图的右侧删除字符。


```C++
#include <iostream>
#include <string_view>

int main()
{
	std::string_view str{ "Peach" };
	std::cout << str << '\n';

	// 从视图左侧移除一个字符
	str.remove_prefix(1);
	std::cout << str << '\n';

	// 从视图右侧移除一个字符
	str.remove_suffix(2);
	std::cout << str << '\n';

	str = "Peach"; // 重置视图
	std::cout << str << '\n';

	return 0;
}
```

该程序产生以下输出:

```C++
Peach
each
ea
Peach
```

与真实的窗帘不同，一旦调用了remove_prefix() 和remove_suffix() ，重置视图的唯一方法是再次将源字符串重新分配给它。

***
## std::string_view可以查看子字符串

这带来了std::string_view的一个重要用法。虽然std::string_view可以用于查看整个字符串而不制作副本，但当我们希望查看子字符串而不进行副本时，它们也很有用。子字符串是现有字符串中的连续字符序列。例如，给定字符串“snowball”，一些子字符串是“snow”、“all”和“now”。“owl”不是“snowball”的子字符串，因为这些字符在“snowball”中不会连续出现。

***
## std::string_view可能是或不是以null结尾

查看子字符串的能力带来了一个值得注意的后果，std::string_view可以以null结尾，也可以不以null结束。考虑字符串“snowball”，它以null结尾。如果std::string_view查看整个字符串，则它正在查看以null结尾的字符串。然而，如果std::string_view仅查看“now”子串，则该子串不是以null结尾的（下一个字符是“b”）。

在几乎所有情况下，这都无关紧要——std::string_view跟踪它正在查看的字符串或子字符串的长度，因此它不需要空终止符。无论std::string_view是否以null结尾，都可以将std::string_view转换为std::string。

{{< alert success >}}
**关键点**

C样式字符串文本和std::string始终以null结尾。std::string_view可以以null结尾，也可以不以null结束。

{{< /alert >}}

{{< alert success >}}
**警告**

注意不要编写任何假设std::string_view以null结尾的代码。

{{< /alert >}}

{{< alert success >}}
**提示**

如果您有一个非null终止的std::string_view，并且由于某种原因需要一个以null结尾的字符串，请将std::string_view赋值给std::string。

{{< /alert >}}

***
## 关于何时使用std::string vs std::string_view的快速指南

本指南并不全面，但旨在强调最常见的情况:

在以下情况下使用std::string变量:

1. 您需要一个可以修改的字符串。
2. 您需要存储用户输入的文本。
3. 您需要存储返回std::string的函数的返回值。


在以下情况下使用std::string_view变量:

1. 您需要对已存在于其他位置的字符串的部分或全部进行只读访问，并且在完成std::string_view的使用之前不会被修改或销毁。
2. C样式字符串需要符号常量。
3. 您需要继续查看返回C样式字符串或非悬空std::string_view的函数的返回值。


在以下情况下使用std::string函数参数:

1. 该函数需要在不影响调用方的情况下修改作为参数传入的字符串。这是比较罕见的情况。
2. 使用的语言标准早于C++17。
3. 传递左值引用（后续课程介绍引用）。


在以下情况下使用std::string_view函数参数:

1. 函数需要只读字符串。


在以下情况下使用std::string返回类型:

1. 返回值是std::string局部变量。
2. 返回值是按值返回std::string的函数调用或运算符。
3. 返回值需要按引用传递（后续课程介绍引用）。


在以下情况下使用std::string_view返回类型:

1. 返回C样式字符串文本。
2. 返回std::string_view的函数参数。


关于std::string的注意事项:

1. 初始化和复制std::string的开销很大，因此应尽可能避免这种情况。
2. 避免按值传递std::string，因为这会生成副本。
3. 如果可能，请避免创建短生命周期的std::string对象。
4. 修改std::string将使该字符串的任何视图无效。


关于std::string_view的注意事项:

1. 由于样式的字符串文本在整个程序执行周期都有效，因此可以将std::string_view设置为C样式的串文本。
2. 当字符串被销毁时，该字符串的所有视图都将无效。
3. 使用无效的视图将导致未定义的行为。
4. std::string_view可能不是以null结尾。

***

{{< prevnext prev="/basic/chapter5/string-view/" next="/basic/chapter5/summary/" >}}
5.9 std::string_view简介
<--->
5.11 第五章总结
{{< /prevnext >}}
