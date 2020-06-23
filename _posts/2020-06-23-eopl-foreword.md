---
layout: post
title:  EOPL,前言
date:   2020-06-23 22:00:00 +0800
categories: eopl
---

* content
{:toc}


前言			{#foreword}
====================================
作者: Hal Abelson

本书主要着重讲述如下基本概念:

*一个编程语言的解释器只是另外一段程序而已。*

听起来是否显而易见？但是却隐藏着深刻的逻辑。如果你是一个计算机理论学家，解释器的概念会让你想起「哥德尔」的不完备定律，「图灵」的通用计算器理论，又或是「冯·诺伊曼」的程序存储的思想。如果你是程序员，掌握解释器的思想会是一种巨大的力量源泉，会对你头脑中关于程序的认识有一个真正的改变。

在我学习解释器之前，我编写过大量的语言，其中的一些相当巨大。例如，其中一个，我用「PL/I」语言编写数据存取和管理系统。当我编程时，我将「PL/I」语言当作语言设计者建立的不可更改的规则集合。我的工作不是去更改这些规则，甚至不是去理解这些规则，而是从厚厚的编程手册中，挑选出这个或那个特性。我从来没想过程序语言的底层数据结构是什么，是否我也可以去修改语言设计者选择的一些特性。我也不知道如和创造嵌入的子语言来帮助我组织代码，所以整个程序像是一个大大的拼图一样，每一片都必须恰好拼对地方，而不是像一组语言集合，可以有机的结合在一起。如果你不明白解释器，你仍然可以编程，可以成为一个不错的程序员，但是永远也无法成为大师。

作为程序员的你，有如下三个原因应该去学习解释器：

首先，你可能会在一定程度上实现一个解释器，可能并不是那种通用的解释器。几乎所有人与复杂系统(绘图程序，信息存取系统)的交互，都包含了类似解释器的结构。这些程序可能包含复杂的单独的操作-在屏幕上渲染一块区域，或者执行数据库查询-解释器是你将负责的操作组合成有用的模式的胶水。能否将一个操作的结果当作另外一个操作的输入？能否对一系列的操作命名？名称是全局的还是局部的？能否向一系列的操作传递参数，并给输入命名？诸如此类。不论单独的指令多么复杂，多么炫目，通常是将这些指令组合起来的胶水的质量决定了系统的能力。很容易就能发现单独的指令质量很高，但是代码的组织方式很糟糕的程序。可以说，我的「PL/I」数据库程序就是这样的。

其次，那些不是解释器的程序都有一些类似解释器的重要部分。如果你去看一个负责的计算机救援系统，你会发现一个地理位置识别语言，一个图像解释器，一个规则控制解释器，一个面向对象语言解释器组合在一起。管理复杂程序的一个有力的手段，就是将程序作为一些程序语言的的集合，不同的语言提供了我们对程序中不同元素的管理。选择合适的语言去做合适的事情，理解不同语言的实现的权衡。这是我们研究解释器的意义。

最后，显式的去修改语言的结构是一种越来越重要的编程技术。在面向对象语言中设计并且操作的类的继承结构就是这样一种趋势。可能一个不可避免的结果是我们的程序正在越来越复杂 - 更加的对语言进行理解可能能帮助我们面对这种复杂度。考虑如下一个基本概念，一个解释器是一个程序。但是这个程序是用其它语言写的，其它语言的解释器又是用来另外一个语言写的，最后的这个语言的解释器是这个语言自己。。。可能程序和编程语言的区别只是一种错误的划分，未来的程序员并不会特别的觉得他们在写程序，而是再为每个应用创建一个新的语言。


Friedman and Wand have done a landmark job, and their book will change the landscape of programming-language courses. They don’t just tell you about interpreters; they show them to you. The core of the book is a tour de force sequence of interpreters starting with an abstract high-level language and progressively making linguistic features explicit until we reach a state machine. You can actually run this code, study and modify it, and change the way these interpreters handle scoping, parameter-passing, control structure, etc.

Having used interpreters to study the execution of languages, the authors show how the same ideas can be used to analyze programs without run- ning them. In two new chapters, they show how to implement type checkers and inferencers, and how these features interact in modern object-oriented languages.

Part of the reason for the appeal of this approach is that the authors have chosen a good tool—the Scheme language, which combines the uniform syn- tax and data-abstraction capabilities of Lisp with the lexical scoping and block structure of Algol. But a powerful tool becomes most powerful in the hands of masters. The sample interpreters in this book are outstanding mod- els. Indeed, since they are runnable models, I’m sure that these interpreters and analyzers will find themselves at the cores of many programming sys- tems over the coming years.

This is not an easy book. Mastery of interpreters does not come easily, and for good reason. The language designer is a further level removed from the end user than is the ordinary application programmer. In designing an application program, you think about the specific tasks to be performed, and consider what features to include. But in designing a language, you consider the various applications people might want to implement, and the ways in which they might implement them. Should your language have static or dynamic scope, or a mixture? Should it have inheritance? Should it pass parameters by reference or by value? Should continuations be explicit or implicit? It all depends on how you expect your language to be used, which kinds of programs should be easy to write, and which you can afford to make more difficult.

Also, interpreters really are subtle programs. A simple change to a line of code in an interpreter can make an enormous difference in the behavior of the resulting language. Don’t think that you can just skim these programs— very few people in the world can glance at a new interpreter and predict from that how it will behave even on relatively simple programs. So study these programs. Better yet, run them—this is working code. Try interpreting some simple expressions, then more complex ones. Add error messages. Modify the interpreters. Design your own variations. Try to really master these programs, not just get a vague feeling for how they work.

If you do this, you will change your view of your programming, and your view of yourself as a programmer. You’ll come to see yourself as a designer of languages rather than only a user of languages, as a person who chooses the rules by which languages are put together, rather than only a follower of rules that other people have chosen.

Postscript to the Third Edition
The foreword above was written only seven years ago. Since then, informa- tion applications and services have entered the lives of people around the world in ways that hardly seemed possible in 1990. They are powered by an ever—growing collection of programming languages and programming frameworks—all erected on an ever-expanding platform of interpreters.

Do you want to create Web pages? In 1990, that meant formatting static text and graphics, in effect, creating a program to be run by browsers exe- cuting only a single “print” statement. Today’s dynamic Web pages make full use of scripting languages (another name for interpreted languages) like Javascript. The browser programs can be complex, and including asyn- chronous calls to a Web server that is typically running a program in a com- pletely different programming framework possibly with a host of services, each with its own individual language.

Or you might be creating a bot for enhancing the performance of your avatar in a massive online multiplayer game like World of Warcraft. In that case, you’re probably using a scripting language like Lua, possibly with an object-oriented extension to help in expressing classes of behaviors.

Or maybe you’re programming a massive computing cluster to do index- ing and searching on a global scale. If so, you might be writing your pro- grams using the map-reduce paradigm of functional programming to relieve you of dealing explicitly with the details of how the individual processors are scheduled.

Or perhaps you’re developing new algorithms for sensor networks, and exploring the use of lazy evaluation to better deal with parallelism and data aggregation. Or exploring transformation systems like XSLT for controlling Web pages. Or designing frameworks for transforming and remixing multi- media streams. Or . . .

So many new applications! So many new languages! So many new inter- preters!

As ever, novice programmers, even capable ones, can get along viewing each new framework individually, working within its fixed set of rules. But creating new frameworks requires skills of the master: understanding the principles that run across languages, appreciating which language features are best suited for which type of application, and knowing how to craft the interpreters that bring these languages to life. These are the skills you will learn from this book.