---
title: "模板类"
date: 2025-01-22T20:47:14+08:00
---

在前一章中，我们介绍了函数模板（11.6——函数模板），它允许我们泛化函数以处理许多不同的数据类型。虽然这是广义编程道路上的一个伟大开端，但它并不能解决我们所有的问题。让我们来看一个这样的问题的例子，看看模板可以为我们做些什么。

模板和容器类

在23.6的课程——容器类中，您学习了如何使用组合来实现包含其他类的多个实例的类。作为这种容器的一个例子，我们看了IntArray类。下面是该类的一个简化示例：

#ifndef INTARRAY_H#define INTARRAH_H#include<cassert>class INTARRAY{private:int m_length{}；整数*m_data{}；public:IntArray（int length）{assert（length>0）；m_data=new int[length]{}；m_length=长度；}//我们不希望允许创建IntArray的副本。IntArray（const IntArray&）=删除；IntArray&operator=（const IntArrary&）=删除~IntArray（）{delete[]m_data；}void erase（）{delete[]m_data；//我们需要确保在此处将m_data.设置为0，否则它将//左指向已释放的内存！m_data=nullptr；m_length=0；}int&operator[]（int index）{assert（index>=0&&index<m_Lenging）；return m_data[index]；}int getLength（）const{return m_length；}}#endif

虽然这个类提供了一种创建整数数组的简单方法，但如果我们想创建一个双精度数组，该怎么办？使用传统的编程方法，我们必须创建一个全新的类！这里是DoubleArray的一个例子，这是一个用于保存双精度数的数组类

#ifndef DOUBLEARRAY_H#define DOUBLEARRAY_H#include<cassert>class DOUBLEARRAY{private:int m_length{}；双*m_data{}；public:DoubleArray（int length）{assert（length>0）；m_data=new double[length]{}；m_length=长度；}DoubleArray（const DoubleArray&）=删除；DoubleArray&operator=（const DoubleArray&）=删除~DoubleArray（）{delete[]m_data；}void erase（）{delete[]m_data；//我们需要确保在此处将m_data.设置为0，否则它将//左指向已释放的内存！m_data=nullptr；m_length=0；}double&operator[]（int index）{assert（index>=0&&index<m_length）；return m_data[index]；}int getLength（）const{return m_length；}}}#endif

尽管代码清单很长，但您会注意到这两个类几乎是相同的！事实上，唯一的实质性区别是所包含的数据类型（int与double）。正如您可能已经猜到的，这是另一个可以很好地使用模板的领域，使我们不必创建绑定到一个特定数据类型的类。

创建模板类的工作方式与创建模板函数的工作方式几乎相同，所以我们将通过示例继续。

这是我们的数组类，模板化版本：

array.h:#ifndef array_h#define array_ h#include<cassert>template<typename T>//添加了类array{private:int m_length{}；T*m_data{}；//将类型更改为T public:Array（int length）{assert（length>0）；m_data=new T[length]{}；//分配了T m_length=length；}类型的对象数组数组（const Array&）=删除；Array&operator=（const Array&）=删除~Array（）{delete[]m_data；}void erase（）{delete[]m_data。//我们需要确保在这里将m_data设置为0，否则它将//左指向已释放的内存！m_data=nullptr；m_length=0；}//模板化操作符[]函数定义在T&operator[]（int index）下面；//现在返回T&int getLength（）常量{return m_length；}}；//在类外部定义的成员函数需要自己的模板声明模板<typename T>T&Array<T>：：operator[]（int index）//现在返回T&{assert（index>=0&&index<m_length）；return m_data[index]；}#endif

如您所见，该版本几乎与IntArray版本相同，只是我们添加了模板声明，并将包含的数据类型从int更改为T。

请注意，我们还在类声明外部定义了operator[]函数。这不是必要的，但由于语法的原因，新程序员在第一次尝试这样做时通常会出错，因此一个例子很有启发性。在类声明外部定义的每个模板化成员函数都需要自己的模板声明。此外，请注意模板化数组类的名称是array<T>，而不是array——array将引用名为array的类的非模板化版本，除非在类内部使用array。例如，复制构造函数和复制赋值运算符使用Array，而不是Array<T>。当类名称在类内部没有模板参数的情况下使用时，参数与当前实例化的参数相同。

下面是一个使用上述模板化数组类的简短示例：

#include<iostream>#incl包括“array.h”intmain（）{constint-length{12}；数组<int>intArray{length}；数组<double>doubleArray{length}；对于（int count{0}；count<length；++count）{intArray[count]=count；doubleArray[count]=coount+0.5；}对于（int计数{length-1}；计数>=0；--count；返回0；}

此示例打印以下内容：

11 11.5 10 10.5 9 9.5 8 8.5 7 7.5 6 6.5 5 5 4 4.5 3 3.5 2 2.5 1 1.5 0 0.5

模板类的实例化方式与模板函数相同--编译器根据需要模版输出副本，用用户需要的实际数据类型替换模板参数，然后编译副本。如果不使用模板类，编译器甚至不会编译它。

模板类是实现容器类的理想选择，因为容器在各种数据类型上工作是非常理想的，模板允许您在不复制代码的情况下这样做。尽管语法很难看，错误消息也可能很神秘，但模板类确实是C++最好、最有用的功能之一。

拆分模板类

模板不是类或函数——它是用于创建类或函数的模具。因此，它的工作方式与普通函数或类的工作方式不完全相同。在大多数情况下，这不是什么大问题。然而，有一个领域通常会给开发人员带来问题。

对于非模板类，常见的过程是将类定义放在头文件中，将成员函数定义放在类似命名的代码文件中。这样，成员函数定义被编译为单独的项目文件。然而，对于模板，这不起作用。

请考虑以下内容：

Array.h:

#ifndef Array_h#define Array_ h#include<cassert>template<typename T>//添加了类Array{private:int m_length{}；T*m_data{}；//将类型更改为T public:Array（int length）{assert（length>0）；m_data=new T[length]{}；//分配了T m_length=length；}类型的对象数组数组（const Array&）=删除；Array&operator=（const Array&）=删除~Array（）{delete[]m_data；}void erase（）{delete[]m_data。//我们需要确保在这里将m_data设置为0，否则它将//左指向已释放的内存！m_data=nullptr；m_length=0；}//模板化操作符[]函数定义在T&operator[]（int index）下面；//现在返回T&int getLength（）常量{return m_length；}}；//数组的定义<T>：：operator[]移动到#endifArray下面的

Array.cpp:

#include“Array.h”//在类之外定义的成员函数需要自己的模板声明模板<typename T>T&Array<T>:：operator[]（int index）//现在返回T&{assert（index>=0&&index<m_length）；return m_data[index]；}

main.cpp:

#include<iostream>#incl包括“Arrary.h”int main（）{const int length{12}；数组<int>intArray{length}；数组<double>doubleArray{length}；对于（int count{0}；count<length；++count）{intArray[count]=count；doubleArray[count]=coount+0.5；}对于（int计数{length-1}；计数>=0；--count；返回0；}

上述程序将编译，但会导致链接器错误：

未定义对`Array<int>：：operator[]（int）'的引用

就像函数模板一样，如果在翻译单元中使用类模板（例如，作为intArray等对象的类型），编译器将仅实例化类模板。为了执行实例化，编译器必须同时看到完整的类模板定义（不仅仅是声明）和所需的特定模板类型。

还要记住，C++单独编译文件。编译main.cpp时，Array.h标头的内容（包括模板类定义）被复制到main.cpp中。当编译器发现我们需要两个模板实例Array<int>和Array<double>时，它将实例化这些实例，并将它们编译为main.cpp翻译单元的一部分。由于运算符[]成员函数具有声明，编译器将接受对它的调用，假设它将在其他地方定义。

单独编译Array.cpp时，Array.h标头的内容被复制到Array.cpp中，但编译器在Array.copp中找不到任何需要实例化Array类模板或Array<int>：：operator[]函数模板的代码——因此它不会实例化任何内容。

因此，当程序被链接时，我们将得到一个链接器错误，因为main.cpp调用了Array<int>：：operator[]，但该模板函数从未实例化！

有许多方法可以解决这个问题。

最简单的方法是将所有模板类代码放在头文件中（在本例中，将Array.cpp的内容放在类下面的Array.h中）。这样，当您#包含标头时，所有模板代码都将位于一个位置。这种解决方案的好处是它很简单。这里的缺点是，如果模板类在许多文件中使用，您将得到模板类的许多本地实例，这可能会增加编译和链接时间（链接器应该删除重复的定义，因此它不应该膨胀您的可执行文件）。这是我们的首选解决方案，除非编译或链接时间开始成为问题。

如果您认为将Array.cpp代码放入Array.h标头会使标头过长/混乱，则另一种方法是将Array.cpp的内容移动到名为Array.inl（.inl表示内联）的新文件中，然后在Array.h标头的底部（标头保护内）包括Array.inl。这产生了与将所有代码放在头中相同的结果，但有助于使事情更有条理。

Tip

如果使用.inl方法，然后得到关于重复定义的编译器错误，则编译器很可能将.inl文件作为项目的一部分进行编译，就像它是代码文件一样。这导致.inl的内容被编译两次：一次是编译器编译.inl时，另一次是编译包含.inl的.cpp文件时。如果.inl文件包含任何非内联函数（或变量），那么我们将运行一个定义规则中的一个。如果发生这种情况，则需要将.inl文件排除在编译过程中。通常可以通过在项目视图中右键单击.inl文件，然后选择属性来从构建中排除.inl。设置将在那里的某个地方。在Visual Studio中，将“从生成中排除”设置为“是”。在代码：：块中，取消选中“编译文件”和“链接文件”。

其他解决方案涉及#include.cpp文件，但我们不建议使用这些文件，因为#include的使用是非标准的。

另一种替代方法是使用三文件方法。模板类定义在标题中。模板类成员函数放在代码文件中。然后添加第三个文件，其中包含您需要的所有实例化类：

templates.cpp:/

/确保可以看到完整的Array模板定义#include“Array.h”#include“Arrary.cpp”//我们在这里打破了最佳实践，但仅在这一处//#包括此处所需的其他.h和.cpp模板定义template class Array<int>；//显式实例化模板Array<int>模板类Array<double>；//显式实例化模板Array<double>//在此处实例化其他模板

“template class”命令使编译器显式实例化模板类。在上述情况下，编译器将在templates.cpp内模板化Array<int>和Array<double>的定义。想要使用这些类型的其他代码文件可以包括Array.h（以满足编译器），链接器将从template.cpp链接这些显式类型定义。

这种方法可能更有效（取决于编译器和链接器处理模板和重复定义的方式），但需要为每个程序维护templates.cpp文件。

***
