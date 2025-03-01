---
title: "异常的风险和缺点"
date: 2025-02-12T14:07:59+08:00
---

与几乎所有有好处的东西一样，例外也有一些潜在的缺点。本文并不全面，只是指出在使用异常（或决定是否使用它们）时应该考虑的一些主要问题。

***
## 清理资源

新程序员在使用异常时遇到的最大问题之一是在发生异常时如何清理资源。考虑以下示例：

```C++
#include <iostream>

try
{
    openFile(filename);
    writeFile(filename, data);
    closeFile(filename);
}
catch (const FileException& exception)
{
    std::cerr << "Failed to write to file: " << exception.what() << '\n';
}
```

如果WriteFile()失败并引发FileException，会发生什么情况？此时，我们已经打开了文件，现在控制流跳转到FileException处理程序，该处理程序打印错误并退出。请注意，该文件从未关闭！该示例应重写如下：

```C++
#include <iostream>

try
{
    openFile(filename);
    writeFile(filename, data);
}
catch (const FileException& exception)
{
    std::cerr << "Failed to write to file: " << exception.what() << '\n';
}

// 确保文件被关闭
closeFile(filename);
```

在处理动态分配的内存时，这种错误通常以另一种形式出现：

```C++
#include <iostream>

try
{
    auto* john { new Person{ "John", 18, PERSON_MALE } };
    processPerson(john);
    delete john;
}
catch (const PersonException& exception)
{
    std::cerr << "Failed to process person: " << exception.what() << '\n';
}
```

如果processPerson()引发异常，控制流将跳到catch处理程序。因此，john从未被释放！这个例子比前一个例子稍微复杂一些——因为john是try块的局部变量，所以当try块退出时，它就超出了作用域。这意味着异常处理程序根本不能访问john（它已经被销毁），因此它没有办法释放内存。

然而，有两种相对简单的方法来解决这个问题。首先，在try块之外声明john，以便在try块结束时它不会超出作用域：

```C++
#include <iostream>

Person* john{ nullptr };

try
{
    john = new Person("John", 18, PERSON_MALE);
    processPerson(john);
}
catch (const PersonException& exception)
{
    std::cerr << "Failed to process person: " << exception.what() << '\n';
}

delete john;
```

因为john是在try块外部声明的，所以它在try块和catch处理程序中都是可访问的。这意味着catch处理程序可以正确地进行清理。

第二种方法是使用类的局部变量，该变量知道当它超出作用域时如何清理自身（通常称为“智能指针”）。标准库提供了一个名为std::unique_ptr的类，可以用于此目的。unique_ptr是一个模板类，它保存指针，并在指针超出作用域时释放它。

```C++
#include <iostream>
#include <memory> // for std::unique_ptr

try
{
    auto* john { new Person("John", 18, PERSON_MALE) };
    std::unique_ptr<Person> upJohn { john }; // upJohn 现在保存着 john

    ProcessPerson(john);

    // 当 upJohn 超出了作用域, 它就会删除 john
}
catch (const PersonException& exception)
{
    std::cerr << "Failed to process person: " << exception.what() << '\n';
}
```

最好的选择（只要可能）是实现RAII的对象（在构造时自动分配资源，在销毁时释放资源）。这样，当管理资源的对象由于任何原因超出作用域时，它将根据需要自动释放！


***
## 异常和析构函数

与构造函数不同，在构造函数中抛出异常是指示对象创建未成功的有用方法，异常永远不应该在析构函数中抛出。

当进行调用栈展开时，如果栈上对象的析构函数抛出了异常。这时编译器将处于这样一种情况：它不知道是继续调用栈展开过程，还是处理新的异常。最终结果是您的程序将立即终止。

因此，最好的做法就是完全避免在析构函数中使用异常。而是将消息写入日志文件。


***
## 性能问题

异常机制需要付出一点性能代价。它们增加了可执行文件的大小，并且由于必须执行额外的检查，它们还可能导致程序运行得较慢。异常的主要性能惩罚发生在实际抛出异常时。在这种情况下，必须展开调用栈并找到适当的异常处理程序，这是一个相对昂贵的操作。

请注意，一些现代计算机体系结构支持称为零成本异常的异常模型。零成本异常（如果支持）在无错误情况下没有额外的运行时成本（这是我们最关心性能的情况）。然而，在发现异常的情况下，它们会招致更大的惩罚。

***
## 应该何时使用异常呢？

当满足以下所有条件时，最好使用异常处理：

1. 正在处理的错误可能只是偶尔发生。
2. 错误严重，无法继续执行。
3. 无法在错误发生的地方处理错误。
4. 没有一种好的替代方法可以将错误码返回给调用者。

作为一个例子，让我们考虑这样的情况：您编写了一个函数，期望用户传入磁盘上文件的名称。您的函数将打开该文件，读取一些数据，关闭该文件，并将一些结果传回给调用者。现在，假设用户传入了一个不存在的文件名，或者一个空字符串。这是使用异常的好时机吗？

在这种情况下，上面的前两点基本满足。一般情况下不太会发生错误。或者当用户传出错误的参数时，编写的函数无法正确执行。对于第三点，这个函数的职责也不应该负责处理错误（比如重新提示用户输入正确的文件名）。第四条比较关键，是否有更好的替代方式将错误码返回给调用者？这取决于您的计划（例如可以返回空指针或者一些错误码），如果没有更好的方式，使用异常是合理的。

***