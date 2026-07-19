# 蓝图架构

> GameInstance · GameMode · 蓝图通信 · 架构设计。

<!--
  写作指引：
  这一章讲你项目的"骨架"——GameInstance、GameMode 这些核心蓝图
  怎么组织、怎么通信。

  建议覆盖：
  ★ 你的 GameInstance（比如 BP_ChemistryGameInstance）
    - 存了哪些全局数据
    - 怎么跨关卡传递数据
  ★ 你的 GameMode（比如 NewGameMode）
    - 定义了哪些游戏规则
    - 有哪些模式/状态（演示模式 / 练习模式 / 考试模式…）
  ★ 蓝图之间的通信方式
    - 直接引用 → 什么时候用
    - Event Dispatcher → 什么时候用（推荐）
    - Blueprint Interface → 什么时候用
    - 各写一个实际例子
  ★ 初始化顺序
    - BeginPlay 里按什么顺序初始化各个系统
  ★ 状态机
    - 实验有哪些状态（未开始/运行中/暂停/完成）
    - 状态切换的逻辑
-->

## 命名规范

<!--
TODO: 列出你项目的命名约定
- BP_ → Blueprint Actor
- WBP_ → Widget Blueprint
- MI_ → Material Instance
- E_ → Enum
- S_ → Structure
... 等等
-->
