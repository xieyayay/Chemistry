# 常用蓝图模式

> 实用代码片段 · 常见写法 · 踩坑记录。

<!--
  写作指引：
  这一章是"速查手册"——你写过一次、以后会反复用到的蓝图写法。

  不用追求完整性，想到什么写什么。积累式的文档。

  可以放的内容：
  ★ 数据持久化
    - SaveGame 的用法
    - 怎么存/读实验数据
  ★ 定时器
    - Set Timer by Event vs Set Timer by Function
    - 循环 vs 单次
  ★ 异步加载
    - 关卡异步加载
    - 资源异步加载
  ★ 材质参数动态修改
    - Create Dynamic Material Instance
    - Set Scalar/Vector Parameter
    - 实际例子：试剂颜色变化、液体填充
  ★ Widget 之间的通信
    - 通过 GameInstance 中转
    - 通过 Event Dispatcher
  ★ Timeline 节点
    - 和 Tick 插值的对比
    - 实际例子：平滑过渡
  ★ 输入处理
    - Enhanced Input（UE5 新方式）
    - Legacy Input（旧方式）
  ★ 你踩过的坑
    - Cast 返回 null → 可能是类型不匹配
    - Delay 之后变量被改了 → 缓存到局部变量
    - 关卡切换后引用没了 → 数据放 GameInstance
-->
