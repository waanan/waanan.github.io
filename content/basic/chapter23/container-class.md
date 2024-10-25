---
title: "容器类"
date: 2024-10-08T17:40:35+08:00
---

在现实生活中，我们一直在使用容器。你的早餐装在一个盒子里，书中的书页放在一个封面和装订物内，你可以在家中的容器中存放任何数量的物品。如果没有容器，那么使用这些对象将非常不方便。想象一下，试着读一本没有任何装订的书，或者在不使用碗的情况下吃菜。那将是一片混乱。容器提供的价值主要在于它能够帮助组织和存储放入其中的项。

类似地，容器类是一个设计用于保存和组织另一类型（另一个类或基本类型）的多个实例的类。有许多不同类型的容器类，每个容器类在使用中都有各种优点、缺点和限制。到目前为止，编程中最常用的容器是数组，您已经看到了许多这样的例子。尽管C++具有内置的数组功能，但程序员通常会使用数组容器类（std::array或std:∶vector），因为它们提供了额外的好处。与内置数组不同，数组容器类通常提供动态调整大小的能力（当添加或删除元素时），能知道存储元素的量，并执行边界检查。这不仅使数组容器类比普通数组更方便，而且也更安全。

容器类通常实现相当标准化的最小功能集。大多数定义良好的容器将包括以下功能：

1. 创建空容器（通过构造函数）
2. 将新对象插入容器
3. 从容器中移除对象
4. 查看容器中当前对象的数量
5. 清空所有对象的容器
6. 提供对存储对象的访问
7. 对元素排序（可选）

有时，某些容器类将省略某些此功能。例如，数组容器类通常省略insert和remove函数，因为它们很慢，并且类设计者不希望鼓励使用它们。

容器类实现“成员”关系。例如，数组的元素是（属于）数组的成员。注意，这里是传统意义上的“成员”，而不是C++类成员。

***
## 容器分类

容器类通常有两种不同的分类。值容器，按值存储所持有的对象，是组合关系（因此负责创建和销毁这些对象）。引用容器，存储指向其他对象的指针或引用，是聚合关系（因此不负责创建或销毁这些对象）。

现实生活中容器可以保存任何类型的对象，但在C++中，容器通常只保存一种类型的数据。例如，如果有一个整数数组，它将只保存整数。与其他一些语言不同，大部分C++容器不允许您任意混合类型。如果需要容器来保存整数和双精度数，通常必须编写两个单独的容器来完成这项工作（或使用模板，这是一个高级C++功能）。尽管它们的使用受到限制，但容器非常有用，它们使编程更容易、更安全和更快。

***
## 数组容器类

在这个例子中，将从头开始编写一个整数数组类，该类实现容器应该具有的大多数常见功能。这个数组类将是一个值容器，它将保存元素的副本。顾名思义，容器将保存一个整数数组，类似于std::vector\<int\>。

首先，让我们创建IntArray.h文件：

```C++
#ifndef INTARRAY_H
#define INTARRAY_H

class IntArray
{
};

#endif
```

IntArray需要跟踪两个值：数据本身和数组的大小。因为我们希望数组能够改变大小，所以必须进行一些动态分配，这意味着必须使用指针来存储数据。

```C++
#ifndef INTARRAY_H
#define INTARRAY_H

class IntArray
{
private:
    int m_length{};
    int* m_data{};
};

#endif
```

现在，我们需要添加一些允许创建IntArrays的构造函数。将添加两个构造函数：一个构造空数组，另一个允许构造预定大小的数组。

```C++
#ifndef INTARRAY_H
#define INTARRAY_H

#include <cassert> // for assert()

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:
    IntArray() = default;

    IntArray(int length):
        m_length{ length }
    {
        assert(length >= 0);

        if (length > 0)
            m_data = new int[length]{};
    }
};

#endif
```

我们还需要一些函数来帮助清理IntArrays。首先，将编写一个析构函数，它只是释放动态分配的数据。然后，将编写一个名为erase()的函数，它将擦除数组并将长度设置为0。

```C++
    ~IntArray()
    {
        delete[] m_data;
        // 这里没有将 m_data 设为 null，m_length 设置为 0，因为对象被销毁，没有任何人可以使用
    }

    void erase()
    {
        delete[] m_data;

        // 需要将 m_data 设置为 nullptr
        // 不然它指向的是被销毁的内存!
        m_data = nullptr;
        m_length = 0;
    }
```

现在让我们重载 operator[]，以便可以访问数组的元素。应该确保index参数具有有效的值，这可以通过使用assert()函数来实现。我们还将添加一个访问函数来返回数组的长度。到目前为止，一切都在这里：

```C++
#ifndef INTARRAY_H
#define INTARRAY_H

#include <cassert> // for assert()

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:
    IntArray() = default;

    IntArray(int length):
        m_length{ length }
    {
        assert(length >= 0);

        if (length > 0)
            m_data = new int[length]{};
    }

    ~IntArray()
    {
        delete[] m_data;
        // 这里没有将 m_data 设为 null，m_length 设置为 0，因为对象被销毁，没有任何人可以使用
    }

    void erase()
    {
        delete[] m_data;
        // 需要将 m_data 设置为 nullptr
        // 不然它指向的是被销毁的内存!
        m_data = nullptr;
        m_length = 0;
    }

    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }

    int getLength() const { return m_length; }
};

#endif
```

此时，我们已经有了一个可以使用的IntArray类。可以分配给定大小的IntArrays，并且可以使用 操作符[] 来检索或更改元素的值。

然而，仍然有一些事情是我们无法使用IntArray完成的。仍然无法更改其大小，仍然无法插入或删除元素，并且仍然无法对其进行排序。复制数组也会导致问题，因为会发生浅层复制，只复制数据指针。

首先，让我们编写一些代码，允许调整数组的大小。我们将编写两个不同的函数来实现这一点。第一个函数reallocate()将在调整数组大小时销毁数组中的现有元素，它将很快。第二个函数resize()在调整数组大小时将保留数组中的任何现有元素，它将比较慢。

```C++
#include <algorithm> // for std::copy_n

    // reallocate 重新设置数组大小.  任何现有的元素都被销毁. 这个函数运行较快.
    void reallocate(int newLength)
    {
        // 首先删除现有元素
        erase();

        // 如果设置为空，那么什么也不做
        if (newLength <= 0)
            return;

        // 分配新内存
        m_data = new int[newLength];
        m_length = newLength;
    }

    // 重新设置数组大小.  老元素会被保留  这个函数会慢一些.
    void resize(int newLength)
    {
        // 如果数组长度已经符合预期，就不需要操作了
        if (newLength == m_length)
            return;

        // 如果设置为空，清除现有数据，然后返回
        if (newLength <= 0)
        {
            erase();
            return;
        }

        // 这里能确定至少有一个元素
        // 先分配新的数组
        // 再拷贝数据
        // 然后销毁旧的数组
        // 最后m_data指向新的数组

        // 首先分配新的数组
        int* data{ new int[newLength] };

        // 判断有多少元素要拷贝
        // 拷贝两个数组，长度小的对应个数的元素
        if (m_length > 0)
        {
            int elementsToCopy{ (newLength > m_length) ? m_length : newLength };
            std::copy_n(m_data, elementsToCopy, data); // 进行实际拷贝
        }
 
        // 不再需要老的数组，进行销毁
        delete[] m_data;

        // 现在开始，可以使用新的数组 And use the new array instead!  Note that this simply makes m_data point
        // 这里只需要将 m_data 指向新分配的数组即可
        // IntArray销毁时，数据会自动销毁
        m_data = data;
        m_length = newLength;
    }
```

呼！确实稍微有些绕！

现在再添加一个拷贝构造函数和赋值运算符，以便可以复制数组。

```C++
    IntArray(const IntArray& a): IntArray(a.getLength()) // 拷贝构造函数，调用普通的构造函数
    {
        std::copy_n(a.m_data, m_length, m_data); // 拷贝数据
    }

    IntArray& operator=(const IntArray& a)
    {
        // 自赋值检查
        if (&a == this)
            return *this;

        // 设置合适的存储空间
        reallocate(a.getLength());
        std::copy_n(a.m_data, m_length, m_data); // 拷贝数据

        return *this;
    }
```

许多数组容器类将在此不再提供新的接口。然而，如果您希望了解如何实现插入和删除功能，我们也将继续编写这些功能。这两个算法都非常类似于resize()。

```C++
   void insertBefore(int value, int index)
    {
        // 检查index值有效
        assert(index >= 0 && index <= m_length);

        // 创建一个比老数组大一个的空间
        int* data{ new int[m_length+1] };

        // 拷贝index之前的数据
        std::copy_n(m_data, index, data); 

        // 将value插入新数组对应的位置
        data[index] = value;

        // 拷贝插入位置之后的数据
        std::copy_n(m_data + index, m_length - index, data + index + 1);

        // 最后，销毁老数组，用新数组替代
        delete[] m_data;
        m_data = data;
        ++m_length;
    }

    void remove(int index)
    {
        // 检查index值有效
        assert(index >= 0 && index < m_length);

        // 如果要移除的是数组最后一个元素，直接清空数组
        if (m_length == 1)
        {
            erase();
            return;
        }

        // 创建比老数组少一个的新空间
        int* data{ new int[m_length-1] };

        // 拷贝index之前的数据
        std::copy_n(m_data, index, data); 

        // 拷贝被移除的index之后的数据
        std::copy_n(m_data + index + 1, m_length - index - 1, data + index); 

        // 最后，销毁老数组，用新数组替代
        delete[] m_data;
        m_data = data;
        --m_length;
    }
```

下面是完整的IntArray容器类。

IntArray.h:

```C++
#ifndef INTARRAY_H
#define INTARRAY_H

#include <algorithm> // for std::copy_n
#include <cassert> // for assert()

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:
    IntArray() = default;

    IntArray(int length):
        m_length{ length }
    {
        assert(length >= 0);

        if (length > 0)
            m_data = new int[length]{};
    }

    ~IntArray()
    {
        delete[] m_data;
        // 这里没有将 m_data 设为 null，m_length 设置为 0，因为对象被销毁，没有任何人可以使用
    }

    IntArray(const IntArray& a): IntArray(a.getLength()) // 拷贝构造函数，调用普通的构造函数
    {
        std::copy_n(a.m_data, m_length, m_data); // 拷贝数据
    }

    IntArray& operator=(const IntArray& a)
    {
        // 自赋值检查
        if (&a == this)
            return *this;

        // 设置合适的存储空间
        reallocate(a.getLength());
        std::copy_n(a.m_data, m_length, m_data); // 拷贝数据

        return *this;
    }

    void erase()
    {
        delete[] m_data;
        // 需要将 m_data 设置为 nullptr
        // 不然它指向的是被销毁的内存!
        m_data = nullptr;
        m_length = 0;
    }

    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }


    // reallocate 重新设置数组大小.  任何现有的元素都被销毁. 这个函数运行较快.
    void reallocate(int newLength)
    {
        // 首先删除现有元素
        erase();

        // 如果设置为空，那么什么也不做
        if (newLength <= 0)
            return;

        // 分配新内存
        m_data = new int[newLength];
        m_length = newLength;
    }

    // r重新设置数组大小.  老元素会被保留  这个函数会慢一些.
    void resize(int newLength)
    {
        // 如果数组长度已经符合预期，就不需要操作了
        if (newLength == m_length)
            return;

        // 如果设置为空，清除现有数据，然后返回
        if (newLength <= 0)
        {
            erase();
            return;
        }

        // 这里能确定至少有一个元素
        // 先分配新的数组
        // 再拷贝数据
        // 然后销毁旧的数组
        // 最后m_data指向新的数组

        // 首先分配新的数组
        int* data{ new int[newLength] };

        // 判断有多少元素要拷贝
        // 拷贝两个数组，长度小的对应个数的元素
        if (m_length > 0)
        {
            int elementsToCopy{ (newLength > m_length) ? m_length : newLength };
            std::copy_n(m_data, elementsToCopy, data); // copy the elements
        }
 
        // 不再需要老的数组，进行销毁
        delete[] m_data;

        // 现在开始，可以使用新的数组 And use the new array instead!  Note that this simply makes m_data point
        // 这里只需要将 m_data 指向新分配的数组即可
        // IntArray销毁时，数据会自动销毁
        m_data = data;
        m_length = newLength;
    }

    void insertBefore(int value, int index)
    {
        // 检查index值有效
        assert(index >= 0 && index <= m_length);

        // 创建一个比老数组大一个的空间
        int* data{ new int[m_length+1] };

        // 拷贝index之前的数据
        std::copy_n(m_data, index, data); 

        // 将value插入新数组对应的位置
        data[index] = value;

        // 拷贝插入位置之后的数据
        std::copy_n(m_data + index, m_length - index, data + index + 1);

        // 最后，销毁老数组，用新数组替代
        delete[] m_data;
        m_data = data;
        ++m_length;
    }

    void remove(int index)
    {
        // 检查index值有效
        assert(index >= 0 && index < m_length);

        // 如果要移除的是数组最后一个元素，直接清空数组
        if (m_length == 1)
        {
            erase();
            return;
        }

        // 创建比老数组少一个的新空间
        int* data{ new int[m_length-1] };

        // 拷贝index之前的数据
        std::copy_n(m_data, index, data); 

        // 拷贝被移除的index之后的数据
        std::copy_n(m_data + index + 1, m_length - index - 1, data + index); 

        // 最后，销毁老数组，用新数组替代
        delete[] m_data;
        m_data = data;
        --m_length;
    }

    // 额外的函数，提供简化的接口
    void insertAtBeginning(int value) { insertBefore(value, 0); }
    void insertAtEnd(int value) { insertBefore(value, m_length); }

    int getLength() const { return m_length; }
};

#endif
```

现在，来测试它，以证明它是有效的：

```C++
#include <iostream>
#include "IntArray.h"

int main()
{
    // 声明有10个元素的数组
    IntArray array(10);

    // 设置为1到10
    for (int i{ 0 }; i<10; ++i)
        array[i] = i+1;

    // 重置为8个元素
    array.resize(8);

    // 位置5之前，插入20
    array.insertBefore(20, 5);

    // 移除位置 3 对应的数据
    array.remove(3);

    // 将30 和 40 分别插入到头和尾
    array.insertAtEnd(30);
    array.insertAtBeginning(40);

    // 测试拷贝构造和赋值运算符
    {
        IntArray b{ array };
        b = array;
        b = b;
        array = array;
    }

    // 打印数组中的数据
    for (int i{ 0 }; i<array.getLength(); ++i)
        std::cout << array[i] << ' ';

    std::cout << '\n';

    return 0;
}
```

这将产生以下结果：

```C++
40 1 2 3 5 20 6 7 8 30
```

尽管编写容器类可能相当复杂，但好消息是只需编写一次。一旦容器类开始正常工作，您就可以根据需要频繁地使用和重用它，而不需要任何额外的编程工作。

可以而且应该做出的一些额外改进：

1. 可以将其作为模板类，以便它可以与任何可复制的类型一起工作，而不仅仅是int。
2. 应该添加各种成员函数的const重载，以正确支持const IntArrays。
3. 应该添加对移动语义的支持（通过添加移动构造函数和移动赋值）。
4. 在执行调整大小或插入操作时，可以移动元素，而不是复制元素。


还有一件事：如果标准库中的类满足您的需要，请使用它，而不是创建自己的类。例如，与其使用IntArray，不如使用std::vector\<int\>。它经过了各种测试，效率高，并且与标准库中的其他类配合良好。

有时您需要一个标准库中不存在的专用容器类，因此需要知道在何时以及如何创建自己的容器类。

{{< alert success >}}
**对于高级读者**

与异常处理相关的一些高级改进：

1. 执行调整大小或插入操作时，仅当元素的移动构造函数为noexcept时才移动元素，否则复制它们（参考后面讲解的 std::move_if_noexcept）。
2. 为调整大小或插入操作提供强大的异常安全保证（参考后面讲解的 异常规范和noexcept）。

{{< /alert >}}

***
