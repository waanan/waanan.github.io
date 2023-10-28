---
title: "安装开发环境"
date: 2022-12-28T16:40:41+08:00
---

在学习时，推荐使用「IDE」来进行代码的开发。「IDE」全称是「集成开发环境」，Integrated Development Environment。
「IDE」中包含代码开发，编译，链接，调试的一切工具，可以大大提高效率。在编辑代码时，除了上一节中所述的行号与代码高亮的功能，「IDE」还会提供代码自动格式化，自动补全等其它有用的功能。

下面推荐两个好用且免费的IDE。

***

## Visual Studio Community (Windows)

在Windows环境中，强烈推荐安装「Visual Studio」。

下载地址：<https://visualstudio.microsoft.com/zh-hans/>

选择最新版本的Visual Studio Community，这里的演示的版本是2022，后续所有的操作都以该版本为例。

安装时，注意选择「使用C++的桌面开发」。如果硬盘空间不够，可以选择更换安装位置。

{{< img src="./vs.png" title="Visual Studio安装选项">}}

***

## Visual Studio Code（Windows Linux Mac）

严格来讲，「Visual Studio Code」只是一个代码编辑器，只是可以进行扩展来当作IDE来进行使用。
只是相比「Visual Studio」需要自行进行配置。

下载地址：<https://visualstudio.microsoft.com/zh-hans/>

* Windows环境配置教程：<https://code.visualstudio.com/docs/cpp/config-mingw>
* Linux环境配置教程：<https://code.visualstudio.com/docs/cpp/config-linux>
* Mac环境配置教程：<https://code.visualstudio.com/docs/cpp/config-clang-mac>

***

## 不使用IDE

只要安装好对应的编译器，不使用IDE也是可行的。大部分的linux与mac系统都自带c++编译器，使用任意的编辑器来编写代码，然后使用命令行来进行编译即可。只是调试时会相对麻烦一点。

***

## 注意事项

如果自行配置开发环境，一定要选择支持C++17以上的编译器。最低的版本需求如下：

* GCC/G++ 7
* Clang++ 8
* Visual Studio 2017 15.7

***

{{< prevnext prev="/basic/chapter0/introduction-to-development/" next="/basic/chapter0/write-first-program/" >}}
0.3 程序开发流程
<--->
0.5 第一个C++程序
{{< /prevnext >}}
