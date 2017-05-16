# Mini-Alphago
An AI for Reversi.

## Technical Details

本项目将蒙特卡罗树搜索中的UCT算法与黑白棋结合，创建一个黑白棋的AI。项目中主要涉及到两方面的理论知识：UCT算法和传统黑白棋及AI黑白棋的策略。

### 蒙特卡洛树搜索（MCTS）

蒙特卡洛树搜索是一种基于随机抽样的用于某些决策过程的启发式搜索算法。蒙特卡洛树搜索的每隔循环包含四个步骤：

a) 选择（Selection）：从根结点R开始，选择连续的子结点向下至叶子结点L。下面的结点有更多选择子结点的方法，使游戏树向最优点扩展移动，这是蒙特卡洛树搜索的本质。
b) 扩展（Expansion）：除非任意一方的输赢导致游戏结束，否则L会创建一个或多个子结点或从结点C中选择。
c) 仿真（Simulation）：在结点C中进行随机布局。
d) 反向传播（Backup）：使用布局结果更新从C到R的路径上的结点信息。

![](http://i.imgur.com/1ENMgIx.png)

### UCT算法（Upper Confidence Bounds on Trees）
UCT算法选择游戏树中的每个结点移动，从而使得表达式
 ![](http://i.imgur.com/J30YpS8.png)
具有最大值。在这个式子中，
a) wi代表第i次移动后取胜的次数；
b) ni代表第i次移动后仿真的次数；
c) c为探索参数—理论上等于√2；在实际中通常可凭经验选择；
d) t代表仿真总次数，等于所有ni的和。

### 传统黑白棋策略
传统黑白棋策略包括以下几类：
a) 贪心策略。每一步走子都选择使得棋盘上子最多的一步，而不考虑最终的胜负；
b) 确定子策略。某些子一旦落子后就再也不会被翻回对方的子，最典型的是四个角上的子，这类子被称为确定子(Stable Discs)。每一步走子都选择使得棋盘上己方的确定子最多的一部。
c) 位置优先策略。考虑到角点的重要性，把棋盘上的每一个子都赋予一个优先级，每一步从可走子里选择优先级最高的一个子。
d) 机动性策略(mobility)。黑白棋每一步的可走子都是有限的，机动性策略是指走子使得对手的可走子较少，从而逼迫对手不得不走出差的一步(bad move)，使得自己占据先机。
e) 消失策略(evaporation, less is more)。在棋盘比试的前期，己方的子越少往往意味着局势更优。因此在前期可采用使己方的子更少的走子。
f) 奇偶策略(parity)。走子尽量走在一行或一列有奇数个空子的位置。
以上只列举了一些常见的黑白棋策略或原则，事实上还有很多更为复杂的策略，此处不进行列举。

### 蒙特卡洛黑白棋
经过策略的实践发现，单一的贪心策略和消失策略效果并不理想，确定子策略的算法比较复杂，程序效率较低，而机动性策略难以用程序体现，奇偶策略的效果也不佳，而位置优先策略在UCT算法中表现优异。
程序中采用两种优先级策略。
第一种优先级如下图：
![](http://i.imgur.com/3W6ExJC.png)
这个优先级表的首要策略是占据角点，所有优先级的设置都为此服务。
第二种优先级如下图：
![](http://i.imgur.com/4x0qk5d.png)
这个优先级表由Roxanne提出，结合了多种策略，同时也结合了Mobility的特性，因为中间子的优先级较高，会提高自己的Mobility而限制对手的可走步数。

### 示例
一次典型的循环可用如下示意图表示：

1. Selection & expansion:
![](http://i.imgur.com/eM9zYGZ.png)

2. Default Policy Simulation:

![](http://i.imgur.com/k72tpzm.png)

3. BACKUP

![](http://i.imgur.com/5dBbGin.png)

### reference
https://www.wikiwand.com/zh-cn/%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B%E6%A0%91%E6%90%9C%E7%B4%A2
http://www.samsoft.org.uk/reversi/strategy.htm
Cameron Browne, et.al., Survey of Monte Carlo Tree Search Methods, IEEE Transactions on Computational Intelligence and AI in Games, 4(1):1-49,2012
Ryan Archer, Analysis of Monte Carlo Techniques in Othello 
