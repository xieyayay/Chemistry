# 关卡序列动画

> Sequencer · Level Sequence · 实验步骤动画编排。

<!--
  写作指引：
  如果你的项目大量使用 Level Sequence 来做实验步骤的动画，
  这一章集中讲 Sequencer 相关的一切。

  建议覆盖：
  ★ 动画资源的目录结构（Anim/ 下面怎么组织的）
  ★ 一个 Sequence 的典型 Track 组成
    - Transform：移动器材
    - Material Parameter：颜色变化（化学反应）
    - Visibility：器材出现/消失
    - Event：触发蓝图回调
    - Camera Cut：镜头切换
  ★ Sequencer 和蓝图的交互方式
    - 怎么在蓝图中播放/暂停/跳转 Sequence
    - 怎么在 Sequence 中触发蓝图事件（Event Track）
    - 怎么传递数据（比如当前步骤编号）
  ★ 步骤跳转的实现方案
    - 怎么存储每个步骤的时间点
    - 怎么从 UI 按钮跳到指定步骤
  ★ 子序列（Sub-Sequence）的使用
  ★ 常见坑
    - 动画播完物体没复位
    - 事件不触发
    - 关卡切换后引用失效
    - 打包后动画资源丢失
-->
