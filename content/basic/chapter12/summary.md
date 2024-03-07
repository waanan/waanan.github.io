---
title: "第12章总结"
date: 2024-02-19T14:35:47+08:00
---

***
## 章节回顾

复合数据类型是可以从基本数据类型（或其他复合数据类型）构造的数据类型。

表达式的值类别指示表达式是解析为值、函数还是某种类型的对象。

左值是计算为具有标识的函数或对象的表达式。具有标识意味着有可识别的存储器地址。左值分为两个子类型：可修改与不可修改（通常是是const或constexpr）。

右值是不是左值的表达式。这包括字面值（字符串字面值除外）和函数或运算符的返回值（按值返回时）。

引用是现有对象的别名。定义引用后，对引用的任何操作都将应用于被引用的对象。C++包含两种类型的引用：左值引用和右值引用。左值引用（通常只是称为引用）充当现有左值（例如变量）的别名。

当使用对象（或函数）初始化引用时，我们说它绑定到该对象（或函数）。

左值引用不能绑定到不可修改的左值或右值（否则，可以通过引用更改这些值，这将违反它们的常量属性）。由于这个原因，左值引用有时被称为非常量的左值引用。

一旦初始化，C++中的引用就不能重置，这意味着不能将其更改为引用另一个对象。

当被引用的对象在引用者之前被销毁时，引用将继续引用不再存在的对象。这样的引用称为悬空引用。访问悬空引用会导致未定义的行为。

通过在声明左值引用时使用const关键字，告诉左值引用将其引用的对象视为const。这样的引用称为对常量的左值引用（有时称为常量引用）。常量引用可以绑定到可修改的左值、不可修改的左值和右值。

临时对象（有时也称为未命名对象或匿名对象）是在单个表达式中创建用于临时使用（然后销毁）的对象。

当使用按引用传递参数时，需要将函数参数声明为引用（或常量引用），而不是正常变量。调用函数时，每个引用参数都绑定到适当的输入。因为引用充当输入对象的别名，所以不会制作输入的副本。

运算符（&）返回其操作数的内存地址。解引用运算符（*）将给定内存地址处的值作为左值返回。

指针是保存内存地址（通常是另一个变量的地址）作为其值的对象。这允许我们存储其他对象的地址以供以后使用。与普通变量一样，指针在默认情况下不会初始化。尚未初始化的指针有时称为野指针。悬空指针是保存不再有效的对象地址的指针。

除了内存地址，指针还可以保存一个额外值：空值。空值是一个特殊的值，表示某物没有值。当指针持有空值时，这意味着指针没有指向任何东西。这样的指针称为空指针。nullptr关键字表示空指针字面值。我们可以使用nullptr显式地初始化指针或为指针赋值。

指针应该保存有效对象的地址，或者设置为nullptr。这样，只需要测试指针是否为空，并且可以假设任何非空指针都是有效的。

常量指针是指向常量值的指针。

指针常量是其地址在初始化后不能更改的指针。

指向常量值的指针常量不能更改其地址，也不能通过指针更改它所指向的值。

通过传递地址，调用方提供对象的地址（通过指针），而不是提供对象作为参数。该指针（保存对象的地址）被复制到被调用函数的指针参数中。然后，该函数可以解引用该指针，以访问按地址被传递的对象。

函数通过引用返回，这避免了复制返回值。使用按引用返回有一个主要的警告：必须确保被引用的对象比返回引用的函数寿命长。否则，返回的引用将悬空（引用已被破坏的对象）。如果通过引用将输入传递到函数中，则通过引用返回该参数是安全的。

如果函数返回引用，并且该引用用于初始化或分配给非引用变量，则将复制返回值（就像它是按值返回的一样）。

按地址返回与按引用返回的工作原理几乎相同，只是返回的是对象的指针，而不是对象的引用。

变量的类型推导（通过auto关键字）将从推导的类型中删除任何引用或顶层const限定符。如果需要，可以将它们作为变量声明的一部分重新设置。

***