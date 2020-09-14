---
layout: post
title:  并行数据结构
date:   2020-09-14 21:00:00 +0800
categories: 并行算法
---

* content
{:toc}

并行数据结构分为两大类，并行查找数据结构（Concurrent Search Data Structure, CSDS）和非查找数据结构。并行数据结构的实现可以基于锁，也可以基于无锁算法，但是目标是一样的：高性能。

CSDS 包括链表（linked list），跳表（skip list），哈希表（hash table）和查找树（search tree）。CSDS 可以抽象为 key-value 容器，提供三个接口：查找，插入和删除。查找就是找到用户指定的 key，返回对应的 value 或者返回一个布尔值表示 key 是否存在。查找操作的核心是对数据结构进行搜索，比如遍历链表。插入和删除操作可以分为两阶段：首先也是对数据结构进行搜索，找到正确的位置，然后完成插入或者删除的动作。一个好的 CSDS 应该具有如下特征 [David15]：

    搜索快。对数据结构的搜索不仅仅是查找操作的核心，也是插入和删除操作的第一阶段，是插入和删除操作的瓶颈。搜索快意味着：搜索过程应该尽量避免（最好完全避免）耗时的操作（写操作，memory barrier，原子操作），等待和重试。

    细粒度。如果插入或者删除操作进入第二阶段，需要对数据结构进行修改，修改应该尽可能涉及较小范围。如果 CSDS 采用锁来实现，就意味着细粒度锁。这样，不同的插入和删除操作可以打散到数据结构的不同部分，彼此不影响，提高并行性。

非查找数据结构包括队列（queue）和栈（stack），它们有比较固定的冲突点，冲突不能打散到数据结构的不同部分，因此特性和 CSDS 不同。

单链表		{#SinglyLinkedList}
====================================

单链表要解决五个问题：1）插入和删除冲突；2）删除和删除冲突；3）内存管理问题（节点从链表摘除后还在被访问）；4）ABA 问题；5）线性化。关于线性化，我们只要求单链表提供三个操作（符合 CSDS 的定义）：任意位置的插入、任意位置的删除和全链表范围内的查找，并且保证这三个操作是线性化的。我们不要求单链表对外提供线性化的链表遍历操作（因为做不到）。线性化是正确性的基础，下面这些单链表都是线性化的。

    Pugh List [Pugh90b] 是一个基于细粒度锁的实现，解决上述问题1和2，没有讨论问题3和4。论文中给出了推理，但是比较难懂。后续使用这种方法的人很少。[Herlihy07] 指出 [Pugh90b] 不仅非常复杂，而且没有被证明是正确的。

    [Valois95a, Valois95b] 首次提出无锁单链表，指出无锁单链表要解决的五个问题，可以作为学习的起点。但是该算法需要增加很多辅助节点，既消耗内存，又带来复杂性，不是好的解决方法。[Michael02a] 干脆认为 [Valois95a] 不是无锁的。另外 [Harris01] 指出 [Valois95a] 提出的算法存在若干错误，后来被修正。

    Harris List [Harris01] 是解决上述问题1和2比较实用的方法。Harris List 采用"两阶段"的方法删除节点：1）标记被删除节点的 next 指针（不允许 next 指针被修改）；2）修改前驱节点的 next 指针，使之指向后继节点。Harris List 在指针中取1比特作为标志（pointer marking），由于指针和标志位于同一个整数中，对指针和标志的读写可以做到原子。但是 Harris List 对上述问题3和4没有贡献。它只是简单地采用类似 RCU 的方法（论文 Section 6 尾部）来解决问题3。问题4则没有讨论。Harris List 不是无锁单链表的完整解。参考 [Michael02a] 对 Harris List 的评论。

    Michael List [Michael02a] 是 Harris List 的改进版，解决上述问题3和4。它有两个算法：1）使用 tagged pointer 来解决问题4。采用 freelist 解决问题3，实际上就是永远不释放内存。如果内存永远不释放，节点从链表摘除后依然可以访问，这时就只需要解决 ABA 问题。2）采用风险指针来解决问题3和4（不需要 tagged pointer）。

    Fomitchev List [Fomitchev04] 也是 Harris List 的改进版，它解决在插入和删除冲突中，插入节点得从链表头重新开始搜索的问题，解决的方法是被删除的节点要记住它原来的前驱节点，由此提出了三阶段删除法。 

    Lazy List [Heller05] 是一个基于细粒度锁的实现，实现简单，易于推理。它在 Harris List 两阶段删除的基础上又添加了两个阶段，形成四阶段删除：1）对被删除节点和它的前驱节点加锁；2）检查被删除节点和它的前驱节点没有被标记，且前驱节点的 next 指针指向被删除节点；3）标记被删除节点的 next 指针；4）修改前驱节点的 next 指针，使之指向后继节点。后两步和 Harris List 相同。锁和标记一起解决上述问题1、2和4。内存管理利用 Java 的 GC；如果没有 GC，论文作者建议采用风险指针。

    Shared_ptr List [Sutter14a, Sutter14b, Sutter14c (第5章Appendix)] 是一个基于 atomic shared_ptr 的实现，它是否无锁，取决于 atomic shared_ptr 能否做到无锁。Shared_ptr List 每个节点的 next 指针是一个 atomic shared_ptr。在给出的版本里，要求插入和删除只发生在链表头部，因此不符合 CSDS 的定义，但是猜想 Shared_ptr List 可以结合 Harris List，扩展到符合 CSDS 定义的程度。对 Shared_ptr List 的批评有三点：1）在遍历链表时，每走过一个节点，都需要引用计数加1，离开时需要引用计数减1，而原子操作比较慢，违反了 CSDS 要求搜索快的原则。2）采用递归方式释放整个链表，或者链表中的一段，有可能导致栈溢出。3）如果一个线程获得一个节点的引用计数，但是被卡住，等了好久才释放这个引用计数，那么该节点的所有后继节点都会被延迟释放。

总结：

    在不考虑内存管理的情况下，Lazy List 是目前最好的并行单链表 [David15, David16]，基于 tagged pointer 的 Michael List 是最好的无锁单链表。最好的并行单链表是有锁的（操作可以打散，细粒度锁的实际冲突率很低），这给我们一个启示：简单的算法其实很好。这里传递了一个正确的价值观。这个结论可以用在如下场景：用户指定链表最大长度，链表创建时一次性分配这么多空间，之后不再分配和释放内存；或者用户允许链表节点只分配，不释放。由于内存不释放，就没有内存管理的问题。

    在考虑内存管理的情况下，目前没有工程上比较实用的解法：RCU 和风险指针实现复杂，使用也不友好。我们等待它们被标准化到 C++ 标准库，并且采用 sys_membarrier 优化，这样才具备在工程上广泛使用的基础。引用计数虽然使用方便，但是性能不好，违反了搜索快的原则。我们等待引用计数将来能够采用类似"weighted reference counting"之类的优化，解决性能问题。内存管理是个共性问题，所有 CSDS 都有这个问题，而且结论是一样的。所以在后续的讨论中，我们不再单独讨论各个算法的内存管理问题。


松散链表		{#UnrolledLinkedList}
====================================

松散链表是把普通链表中多个相邻节点聚合成一个大节点，从而减少链表长度，提高搜索速度。汇聚在一个大节点中的 key-value 不必按照 key 的顺序摆放，这样有利于插入。同时，在一个大节点中的 key-value 由于连续存放，可以较好的利用 cache locality（要求每个 key 占用的内存空间小）。在插入和删除的过程中，大节点需要进行分裂和合并，这是松散链表特有的动作。本文主要关心单链表在多线程环境下的实现，即如何解决上述提到的5个问题，松散链表不是我们关心的重点。但是有些研究工作把并行链表和松散链表相结合，实现并行松散链表，这里简单罗列一下。

    Locality-Conscious List [Braginsky11] 是基于 Michael List 实现的松散链表。

    Platz List [Platz14] 是基于 Lazy List 实现的松散链表。

跳表		{#SkipList}
====================================

并行跳表有两种实现：第一种是直面并行性的问题，硬解各种冲突。由于跳表可以看成是多个链表的集合，所以每种并行单链表算法都能衍生出一个并行跳表算法。代表算法是：Fraser Skip List, Fomitchev Skip List 和 Lazy Skip List；第二种是规避并行性，把塔的升降交给单独线程来管理，代表算法是：No-Hot-Spot Skip List 和 Rotating Skip List。

    [Pugh89, Pugh90a, Pugh90c] 最早提出跳表，只支持单线程。[Pugh90b] 支持多线程，是基于 Pugh List 的跳表。[Herlihy07] 指出 [Pugh90b] 不仅非常复杂，而且没有被证明是正确的。
     
    Fraser Skip List [Fraser04] 是基于 Harris List 的跳表，它是无锁的。Java SE 6 中的 ConcurrentSkipListMap 是基于 Fraser Skip List [Herlihy07]。因此，Fraser Skip List 是一个优秀的算法。

    Fomitchev Skip List [Fomitchev04] 是基于 Fomitchev List 的跳表。

    Herlihy Skip List [Herlihy06, Herlihy07] 是基于 Lazy List 的跳表，它采用细粒度锁，性能和 Fraser Skip List 相当，但是实现简单，易于推理。

    No-Hot-Spot Skip List [Crain12, Crain13] 的思路是：新节点只插入到最底层，塔升高和降低由单独线程完成，避免线程间冲突。但是，引入额外的线程是有开销的。另外，跳表通常用数组来实现塔，No-Hot-Spot Skip List 用链表来实现塔，很费内存，而且不利于提高 CPU cache 命中率，参考 [Dick16] 的评论。

    Rotating Skip List [Dick16] 是 No-Hot-Spot Skip List 的简单改进版，解决了 No-Hot-Spot Skip List 用链表实现塔结构的问题，改用循环数组替代了链表。

    Platz Skip List [Platz19] 是基于 Platz List 的跳表，采用了松散链表技术，不是我们关心的重点。

总结：在第一种实现方法中（不引入额外线程），Herlihy Skip List 是最好的并行跳表 [David15, David16]，Fraser Skip List 是最好的无锁跳表。

树		{#Tree}
====================================

Bw-tree 
[Levandoski16]

先进先出队列		{#FIFO_queue}
====================================

先进先出队列的基本功能是从一头插入和从另外一头取出，严格保序。队列的实现可以基于数组、链表或者混合两者。基于数组的实现需要在创建队列时指明队列的最大容量，队列在初始化时会在内部创建一个足够大的数组用于存储队列中的元素。基于数组的实现比较简单，而且性能高（不需要在插入时创建节点，不需要在取出时释放节点），但是比较浪费内存（必须预分配数组）。基于链表的实现可以较为灵活的管理内存，但是实现难度相对较大。如果实现的好（比如采用内存池），基于链表的队列也可以避免在插入和取出时的内存分配和释放，因此也可以实现高性能，但相比基于数组的队列，获得这种高性能需要付出更多的编码代价。混合使用数组和链表难度更大。

队列的性能是不可扩展的（多线程不提升性能），因为队列头和尾是固定的冲突点。学术界有些研究通过绕道走的方法来使得队列性能可扩展，比如：不严格保序，采用消除的方法（elimination，插入和取出直接在队列外部解决，不进入队列），对操作进行批处理等，这些不是本文关心的重点。

1）基于数组

    [Valois94] 提出了基于数组的队列实现。

2）基于链表

基于链表的队列需要解决2个问题：1）空队列；2）ABA 问题。队列都是线性化的（因为功能简单），而且由于不涉及查找操作，没有内存管理的问题。

    [Valois94] 提出了一种基于链表的无锁队列，[Michael95] 修改了 [Valois94] 的错误，[Michael96] 又进一步指出 [Valois94] 的缺陷，最终发展成为 MS-queue。MS-queue 和 [Valois94] 的主干代码很像，区别是 MS-queue 在 dequeue 时做了检查，防止 head 超过 tail 的情况；另外 MS-queue 用 tagged pointer 防止 ABA 问题，而 [Valois94] 采用引用计数的方法。

    MS-queue [Michael96, Michael98] 是一种基于链表的无锁队列，已经由 boost library 实现，并且包含在 Java Concurrency Package 中 [Mozes08]，它是一个优秀的算法。MS-queue 通过保留一个 dummy node 来解决空队列问题，通过 tagged pointer 来防止 ABA 问题。Tagged pointer 不能彻底解决 ABA 问题（tag rolling-over problem，参考 [Mozes08] 章节 3.4 对 rolling-over 问题的讨论），只能让 ABA 发生的可能性变小。为了减少 ABA 的可能性，需要增加 tag 所占用的比特位，这样指针中用于表示地址的比特位就会减少，指针就越不可能直接指向一个真实的内存地址。Boot library 提供两种方法：1）tag 用 16 位，地址用 48 位，地址指向真实的内存地址，要求新分配的节点的地址必须小于 2^48。这勉强能够办到，但是 16 位的 tag 显得有些少，ABA 的风险并非足够小。2）使用更多位用于 tag，剩下的位不用于地址，而是作为一个下标，在一个预分配的节点池中定位节点。但是这样一来就退化成基于数组的队列了。另外，[Morrison13] 指出 MS-queue 依赖 CAS，而 CAS 重试导致性能损失很大。

    Two-Lock Queue [Michael96, Michael98] 是一种基于链表的有锁队列，实现简单，易于推理，在中等负载强度下性能也不错。如果综合考虑复杂度和性能，Two-Lock Queue 是不错的选择。[Michael98] 指出，Two-Lock Queue 的主要问题是线程切换可能发生在临界区内，导致 spinlock 被长时间抓住。如果排除这个问题，Two-Lock Queue 的性能和 MS-queue 是接近的（"two safe locks" in Fig.6 of [Michael98]）。

    Mozes Queue [Mozes08] 是一种基于双向链表的无锁队列。它赋予 tagged pointer 新含义，其中的 tag 记录链表的“总长度”。这里“总长度”是包含目前已经在链表中的节点，也包含之前被删除的节点，因此“总长度”只增不减。相比 MS-queue，Mozes Queue 花了很大力气少用了一个 CAS 操作。但是链表修复操作需要遍历链表，引入了内存管理的问题（队列本来是没有内存管理问题的）。最后，Mozes Queue 走上了不释放内存的老路。所以，Mozes Queue 在工程上的意义不大，但是利用 tag 来记录“总长度”和对反向（prev）指针的分析可见作者对该问题理解是有深度的。

3）混合型

    LCRQ [Morrison13] 把多个数组链起来，链接的方式还是 MS-queue，但是每个单元是数组。大部分插入在数组内部完成，用 fetch-and-add（F&A） 替代 CAS。因为 F&A 不会失败重试，避免了 MS-queue 因为 CAS 重试带来的性能损失。

总结：MS-queue 是目前最好的基于链表的无锁队列。

内存管理		{#Memory}
====================================

内存管理有三种方法：Reference Counting, Hazard Pointers 和 RCU-like solutions [Mckenney13] 。Java 程序有自动 GC 功能，也是一种内存管理方法。由于 C++ 没有自动 GC 功能，因此自动 GC 不在本文中讨论。

    Paul E. Mckenney and John D. Slingwine. "Read-copy update: using execution history to solve concurrency problems." 

    风险指针（hazard pointers）[Michael02b, Michael04, Michael17]。风险指针最大的问题是很难用，用户需要标记正在被访问的对象，即：风险指针侵入用户逻辑。C++ 委员会在讨论风险指针标准化的问题 [Michael17]，这有助于提高风险指针的易用性，但是用户依然需要去标记对象。性能问题依赖于 sys_membarrier [Michael17]。如果没有 sys_membarrier，读者在设置风险指针时需要添加 memory barrier，影响 CSDS 搜索性能，违反了 CSDS 要求搜索快的原则。总之，如果 C++ 标准库能支持风险指针，并且基于 sys_membarrier 实现，风险指针是可用的。

    RCU-like solutions 把一个节点移除数据结构后并不马上释放其内存，而是等到所有相关线程达到一个安全点，即：所有相关线程都不再访问被移除的节点，然后再删除该节点。一个简单的实现是基于 epoch 或者 timestamp。节点移除时记住当前的 epoch 或者 timestamp，称为移除时刻。每个线程在开始访问数据结构时记住当前的 epoch 或者 timestamp，称为该线程的起始时刻。线程不再访问该数据结构时清空自己的起始时刻。一个节点的内存可以被释放的条件是它的移除时刻小于所有线程的起始时刻。

参考文献		{#Refs}
====================================
    [Braginsky11] Anastasia Braginsky, et al. "Locality-conscious lock-free linked lists", ICDCN'11, pp. 107–118.
    [Crain12] Tyler Crain, Vincent Gramoli and Michel Raynal. "A contention-friendly, non-blocking skip list", Technical Report RR-7969, IRISA, May 2012.
    [Crain13] Tyler Crain, Vincent Gramoli and Michel Raynal. "No hot spot non-blocking skip list", ICDCS'13, July 2013.
    [David15] Tudor David, et al. "Asynchronized concurrency: the secret to scaling concurrent search data structures", ASPLOS'15, March 2015, Turkey.
    [David16] Tudor David, et al. "Concurrent Search Data Structures Can Be Blocking and Practically Wait-Free", SPAA'16, July 11-13, 2016, California.
    [Dick16] Ian Dick, Alan Fekete and Vincent Gramoli. "A skip list for multicore", Concurrency and Computation: Practice and Experience, 29(4), 1-20. 27 May 2016.
    [Fomitchev04] Mikhail Fomitchev, et al. "Lock-free linked lists and skip lists", PODC'04, July 25-28, 2004, Canada.
    [Fraser04] Keir Fraser. "Practical lock-freedom", Technical Report UCAM-CL-TR-579, Cambridge University Computer Laboratory, 2004. (Section 4.3.3) http://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf
    [Harris01] Tim Harris. "A pragmatic implementation of non-blocking linked lists", DISC'01, pp. 300-314, October 2001.
    [Heller05] Steve Heller, et al. "A lazy concurrent list-based set algorithm", OPODIS'05, pp. 3-16, Dec. 12-14, 2005, Italy.
    [Herlihy06] Maurice Herlihy, et al. "A provably correct scalable concurrent skip list", OPODIS'06.
    [Herlihy07] Maurice Herlihy, et al. "A simple optimistic skiplist algorithm”, SIROCCO, pp. 124-138, 2007.
    [Levandoski16] Justin J. Levandoski, et al. "The Bw-Tree: A B-tree for New Hardware Platforms", ICDE'13, pp. 302-313, Apr. 8-11, 2013, Australia.
    [Mckenney13] Paul E. McKenney. "Structured deferral: synchronization via procrastination", Communications of the ACM, 56(7):40–49, July 2013. 
    [Michael95] Maged M. Michael, et al. "Correction of a Memory Management Method for Lock-Free Data Structures", TR599, University of Rochester, 1995.
    [Michael96] Maged M. Michael, et al. "Simple, fast, and practical non-blocking and blocking concurrent queue algorithms", PODC'96
    [Michael98] Maged M. Michael, et al. "Non-blocking algorithms and preemption-safe locking on multiprogrammed shared memory multiprocessors", Journal of Parallel and Distributed Computing, 51(1), 1-26, May 1998.
    [Michael02a] Maged M. Michael. "High performance dynamic lock-free hash tables and list-based sets", SPAA'02, pp. 73-82, August 2002, Canada.
    [Michael02b] Maged M. Michael. "Safe memory reclamation for dynamic lock-free objects using atomic reads and writes", PODC'02, pp. 21-30, July 2002, California.
    [Michael04] Maged M. Michael. "Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects", IEEE Transactions on Parallel and Distributed Systems, vol. 15, no. 6, June 2004.
    [Michael17] Maged M. Michael, et al. "Hazard pointers: safe resource reclamation for optimistic concurrency", P0233R6, 2017. http://open-std.org/JTC1/SC22/WG21/docs/papers/2017/p0233r6.pdf
    [Morrison13] Adam Morrison, et al. "Fast Concurrent Queues for x86 Processors". PPoPP'13, pp. 103-112, Feb. 23-27, 2013, China.
    [Mozes08] Edya Ladan Mozes, et al. "An optimistic approach to lock-free FIFO queues", Distributed Computing, 20(5), Feb. 2008.
    [Platz14] Kenneth Platz, et al. "Practical Concurrent Unrolled Linked Lists Using Lazy Synchronization", POPDIS'14, pp. 388-403.
    [Platz19] Kenneth Platz, et al. "Concurrent Unrolled Skiplist", ICDCS'19, pp. 1579-1589.
    [Pugh89] William Pugh. "Skip lists: a probabilistic alternative to balanced trees", Algorithms and Data Structures: Workshop WADS ’89, Ottawa, Canada, August 1989, Springer-Verlag Lecture Notes in Computer Science 382, 437-449. (revised version to appear in Comm. ACM).
    [Pugh90a] William Pugh. "Skip list: a probabilistic alternative to balanced trees", Communications of the ACM, 33(6), 668-676, June 1990. 
    [Pugh90b] William Pugh. "Concurrent maintenance of skip list", Technical Report CS-TR-2222, Department of Computer Science, University of Maryland, June 1990.
    [Pugh90c] William Pugh. "A skip list cookbook", Technical Report CS-TR-2286.1, Department of Computer Science, University of Maryland, June 1990.
    [Sutter14a] Herb Sutter. “Lock-Free Programming (or, Juggling Razor Blades), Part I”, 2014. https://www.youtube.com/watch?v=c1gO9aB9nbs (58:30)
    [Sutter14b] Herb Sutter. “Lock-Free Programming (or, Juggling Razor Blades), Part II”, 2014. https://www.youtube.com/watch?v=CmxkPChOcvw (18:15) 
    [Sutter14c] Herb Sutter. “Atomic Smart Pointers, rev. 1”, N4162, 2014. http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4162.pdf
    [Valois94] John D. Valois. "Implementing lock-free queues", PDCS'94.
    [Valois95a] John D. Valois. "Lock-free linked lists using compare-and-swap". PODC'95, pp. 214-222, August 1995, Canada.
    [Valois95b] John D. Valois. "ERRATA Lock-free linked lists using compare-and-swap", 1995.

