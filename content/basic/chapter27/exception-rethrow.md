---
title: "重新抛出异常"
date: 2025-02-12T14:07:59+08:00
---

有时，您可能会遇到这样的情况，即您希望捕获异常，但不希望（或没有能力）在捕获它的时候完全处理它。当您希望记录错误，但将问题传递给更上层调用者来实际处理。这些都是是常见的需求。

在有些使用函数返回码的场景，这很简单。考虑以下示例：

```C++
Database* createDatabase(std::string filename)
{
    Database* d {};

    try
    {
        d = new Database{};
        d->open(filename); // 假设失败时，抛出 int exception 
        return d;
    }
    catch (int exception)
    {
        // 数据库创建失败
        delete d;
        // log文件中进行记录
        g_log.logError("Creation of Database failed");
    }

    return nullptr;
}
```

在上面的代码片段中，函数的任务是创建Database对象、打开数据库并返回Database对象。在出现错误的情况下（例如，传入了错误的文件名），异常处理程序会记录错误，然后合理地返回空指针。

现在考虑以下函数：

```C++
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // 假设失败时，抛出 int exception 
    }
    catch (int exception)
    {
        // log文件中进行记录
        g_log.logError("getIntValueFromDatabase failed");

        // 然而，我们还没有真正的处理异常
        // 应该怎么做呢?
    }
}
```

在该函数成功的情况下，它返回一个整数值——任何整数值都可以是有效值。

但getIntValue()出现问题的情况呢？在这种情况下，getIntValue()将抛出整数异常，该异常将被getIntValueFromDatabase()中的catch块捕获，然后将记录错误。但是，我们如何告诉getIntValueFromDatabase()的调用方出现了问题？与上面的示例不同，这里没有一个好的返回码可以使用（因为任何整数返回值都可以是有效的）。

***
## 抛出新的异常

一个明显的解决方案是抛出新的异常。

```C++
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // 假设失败时，抛出 int exception 
    }
    catch (int exception)
    {
        // log文件中进行记录
        g_log.logError("getIntValueFromDatabase failed");

        // 抛出字符 'q' exception
        throw 'q'; 
    }
}
```

在上面的示例中，程序从getIntValue()捕获int异常，记录错误，然后抛出一个字符值“q”的新异常。尽管从catch块抛出异常似乎很奇怪，但这是允许的。请记住，只有在try块中引发的异常才有资格被捕获。这意味着在catch块中引发的异常将不会被它所在的catch块捕获。相反，它将向上传播到调用栈中的调用方。

从catch块抛出的异常可以是任何类型的异常——它不需要与刚刚捕获的异常的类型相同。

***
## 抛出新的异常（错误的方式）

另一个选项是重新引发相同的异常。这样做的一种方法如下：

```C++
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // 假设失败时，抛出 int exception 
    }
    catch (int exception)
    {
        // log文件中进行记录
        g_log.logError("getIntValueFromDatabase failed");

        throw exception;
    }
}
```

尽管这种方法有效，但它有几个缺点。首先，这不会抛出与捕获的异常完全相同的异常——相反，它抛出捕获异常的副本。尽管编译器有可能会优化掉这次拷贝，单也有可能不会优化，因此这可能会降低性能。

但值得注意的是，考虑在以下情况下会发生什么：

```C++
int getIntValueFromDatabase(Database* d, std::string table, std::string key)
{
    assert(d);

    try
    {
        return d->getIntValue(table, key); // 失败时抛出 Derived exception
    }
    catch (Base& exception)
    {
        // log文件中进行记录
        g_log.logError("getIntValueFromDatabase failed");

        throw exception; // 危险: 这里抛出了 Base 对象, 而不是 Derived 对象
    }
}
```

在这种情况下，getIntValue()抛出Derived对象，但catch块捕获的是Base引用。这很好，因为Derived对象可以有Base引用。然而，当我们再次抛出异常时，抛出的异常是从捕获的异常拷贝初始化的。被捕获异常的类型为Base，因此拷贝的异常的类型也为Base（而不是Derived！）。换句话说，我们的派生对象已经被切片！

您可以在以下程序中看到这一点：

```C++
#include <iostream>
class Base
{
public:
    Base() {}
    virtual void print() { std::cout << "Base"; }
};

class Derived: public Base
{
public:
    Derived() {}
    void print() override { std::cout << "Derived"; }
};

int main()
{
    try
    {
        try
        {
            throw Derived{};
        }
        catch (Base& b)
        {
            std::cout << "Caught Base b, which is actually a ";
            b.print();
            std::cout << '\n';
            throw b; // Derived 对象这里被切片了
        }
    }
    catch (Base& b)
    {
        std::cout << "Caught Base b, which is actually a ";
        b.print();
        std::cout << '\n';
    }

    return 0;
}
```

这将打印：

```C++
Caught Base b, which is actually a Derived
Caught Base b, which is actually a Base
```

第二行指示b实际上是Base而不是Derived，事实证明Derived对象已被切片。

***
## 抛出新的异常（正确的方式）

幸运的是，C++提供了一种重新抛出与刚刚捕获的异常完全相同的方法。为此，只需在catch块中使用throw关键字（没有关联的变量），如下所示：

```C++
#include <iostream>
class Base
{
public:
    Base() {}
    virtual void print() { std::cout << "Base"; }
};

class Derived: public Base
{
public:
    Derived() {}
    void print() override { std::cout << "Derived"; }
};

int main()
{
    try
    {
        try
        {
            throw Derived{};
        }
        catch (Base& b)
        {
            std::cout << "Caught Base b, which is actually a ";
            b.print();
            std::cout << '\n';
            throw; // 注: 这里重新抛出捕获的对象
        }
    }
    catch (Base& b)
    {
        std::cout << "Caught Base b, which is actually a ";
        b.print();
        std::cout << '\n';
    }

    return 0;
}
```

这将打印：

```C++
Caught Base b, which is actually a Derived
Caught Base b, which is actually a Derived
```

这个似乎没有抛出任何特定内容的throw关键字，实际上重新抛出了刚刚捕获的完全相同的异常。没有制作拷贝副本，这意味着我们不必担心性能降低或对象切片。

如果需要重新抛出异常，则应首选此方法而不是其他方法。

{{< alert success >}}
**规则**

重新抛出相同的异常时，请单独使用throw关键字

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter27/exception-and-class/" next="/basic/chapter27/function-try/" >}}
27.4 异常、类和继承
<--->
27.6 函数try块
{{< /prevnext >}}
