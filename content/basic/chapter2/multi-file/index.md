---
title: "多代码文件程序"
date: 2023-10-09T20:06:10+08:00
---

***
## 将文件添加到项目中

随着程序越来越大，为了代码组织或可重用，通常拆分为多个文件。使用IDE的优点是，处理多个文件更容易。之前已讲解创建和编译单文件项目。将新文件添加到现有项目非常容易。

{{< alert success >}}
**最佳实践**

将新代码文件添加到项目中时，使用扩展名.cpp。

{{< /alert >}}

{{< alert success >}}
**对于Visual Studio用户**

在Visual Studio中，右键单击“解决方案资源管理器”窗口中的“源文件”文件夹（或项目名称），然后选择“添加”>“新建项”。

{{< img src="./VS-AddNewItem1.webp" title="新建项">}}

确保已选择C++文件（.cpp）。指定新文件名称，添加到项目中。

{{< img src="./VS-AddNewItem1.webp" title="新建文件">}}

注意：如果从“文件”菜单而不是从解决方案资源管理器中的项目创建新文件，新文件不会自动添加到项目中。必须手动将其添加到项目中。要执行此操作，请在解决方案资源管理器中右键单击源文件，选择添加>现有项，然后选择文件。

现在，当编译程序时，会看到编译器在编译文件时列出了文件的名称。

{{< /alert >}}

{{< alert success >}}
**对于GCC/G++用户**

从命令行中，可以使用您喜爱的编辑器自己创建附加文件，并为其命名。编译程序时，需要在命令中包含所有相关的代码文件。例如：g++ main.cpp add.cpp -o main，其中main.cpp和add.cpp是代码文件的名称，main是输出文件的名称。

{{< /alert >}}

## 多文件示例

在前向声明一节中，有一个无法编译的单个文件程序：

```C++
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}

int add(int x, int y)
{
    return x + y;
}
```

当编译器在main的第5行到达add的函数调用时，不知道add是什么，因为直到第9行才定义add！解决方案是要么重新排序函数（将add放在第一位），要么使用前向声明进行add。

类似的多文件程序：

add.cpp：

```C++
int add(int x, int y)
{
    return x + y;
}
```

main.cpp：

```C++
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n'; // 编译失败
    return 0;
}
```

编译器可以先编译add.cpp或main.cpp。无论哪种方式，main.cpp都将无法编译，给出与上一示例相同的编译器错误：

原因也完全相同：当编译器到达main.cpp的第5行时，它不知道add是什么。

记住，编译器单独编译每个文件。不知道其他代码文件的内容，也不记得从以前编译的其它代码文件中看到的内容。因此，即使编译器以前见过函数add的定义（如果先编译add.cpp），也不会记住。

这种有限的可见性和短暂的记忆是有意设计的，原因有三个：

1. 一个项目中的多个文件，可以按任意顺序编译
2. 如果修改了单个文件，那么修改的文件需要编译
3. 减少了不同文件中的命名冲突的概率。

下一课中，将探索名称发生冲突时会发生什么。

解决方案选项与前面相同：将函数add的定义放在函数main之前，或者用前向声明来满足编译器。由于函数add在另一个文件中，因此无法重新排序选项。

解决方案是使用向前声明：

main.cpp（带前向声明）：

```C++
#include <iostream>

int add(int x, int y); // 让 main.cpp 知道 add() 是在其它地方定义的函数

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}
```

add.cpp（保持不变）：

```C++
int add(int x, int y)
{
    return x + y;
}
```

现在，当编译器编译main.cpp时，将知道add()是什么。链接器把对main.cpp的add()函数调用连接到add.cpp中函数的定义。

使用这种方法，可以让文件访问另一个文件中的函数。

尝试使用前向声明编译add.cpp和main.cpp。如果有链接器错误，请确保已将add.cpp正确添加到项目或编译命令中。

{{< alert success >}}
**提示**

由于编译器单独编译每个代码文件（然后忘记它看到的内容），因此使用std::cout或std:∶cin的每个代码文件都需要 #include<iostream>。

上面示例中，如果add.cpp使用了std::cout或std:∶cin，则需要 #include<iostream>。

{{< /alert >}}

{{< alert success >}}
**关键点**

在表达式中使用标识符时，标识符必须能链接到定义。

1. 如果编译器尚未看到正在编译的文件中标识符的前向声明或定义，会在使用标识符的位置报错。
2. 如果同一文件中存在定义，编译器会把标识符的使用连接到定义。
3. 否则，如果定义存在于不同文件中（并且对链接器可见），则链接器会把标识符的链接连接到定义。
4. 否则，链接器报出错。

{{< /alert >}}

***
## 遇到错误时解决方法

第一次尝试使用多个文件时，有许多可能会出错的地方。如果尝试上述示例并遇到错误，请检查以下内容：

1. 如果编译器报错main中没有定义add，那么可能是忘记在main.cpp中前向声明add函数。
2. 如果有如下链接错误

```C++
unresolved external symbol "int __cdecl add(int,int)" (?add@@YAHHH@Z) referenced in function _main
```
最有可能的是add.cpp，没有正确添加到项目中。编译时，会看到编译器列表main.cpp和add.cpp。如果只看到main.cpp，那么不会编译add.cpp。如果使用Visual Studio，则应在IDE的解决方案资源管理器/项目窗格中看到列出的add.cpp。如果没有，请右键单击项目，并添加文件，然后再尝试编译。如果在命令行上编译，不要忘记在编译命令中同时包含main.cpp和add.cpp。

或者是将add.cpp添加到了错误的项目中。

或者文件被设置为不编译或链接。检查文件属性，确保将文件配置为编译/链接。在VisualStudio中，有“从生成中排除”选项，应设置为“否”或保留为空。

3. 不要在main.cpp中加入 "#include add.cpp"。后面预处理器章节会解释原因。

***
## 总结

C++的设计使每个源文件都可以独立编译，而不需要知道其他文件中的内容。因此，文件的实际编译顺序不应相关。

一旦进入面向对象编程，会开始大量处理多个文件，因此现在是确保了解如何添加和编译多个文件项目的最佳时机。

提醒：无论何时创建新的代码（.cpp）文件，都需要添加到项目中，以便进行编译。

***

{{< prevnext prev="/basic/chapter2/forward-declare/" next="/basic/chapter2/namespace/" >}}
2.6 前向声明
<--->
2.8 命名冲突和名称空间简介
{{< /prevnext >}}
