# [aa] · 技术文档

> 基于UE5 5.4.4全蓝图的虚拟仿真化学实验的教学软件，写给自己回顾总结以及后来的接手本项目的新人学习



## 文档导航

| 章节 | 说明 |
|------|------|
| [快速入门](getting-started/project-overview.md) | 怎么打开项目、目录结构、环境配置 |
| [关卡序列动画](animation/level-sequence.md) | Sequencer 制作、蓝图交互、步骤跳转 |
| [Widget UI](ui/widget-overview.md) | UMG 控件、数据绑定、事件处理 |
| [UI 动画](ui/widget-animation.md) | Widget 动效、入场退场、缓动 |
| [蓝图架构](blueprints/game-mode.md) | GameInstance/GameMode、蓝图通信 |
| [蓝图模式](blueprints/common-patterns.md) | 实用代码片段、常见写法 |
| [AI 对话](systems/ai-dialog.md) | API 接入、对话面板、TTS |
| [关卡加载](systems/level-streaming.md) | 流式加载、加载界面 |
| [材质](assets/materials.md) | 材质系统、实例化、VFX |
| [模型](assets/models.md) | 模型导入、命名规范、碰撞 |
| [插件](plugins/third-party.md) | 第三方插件清单与用法 |

<!--
  上面是文档总导航。你可以随时在 nav 里增删章节。
  如果你后续想生成网页，MkDocs 会根据这个表格自动生成导航。
-->

## 如何编写

1. **每个 .md 文件只负责一个主题**，不要太长（200-500 行为宜）
2. **多用代码块**展示蓝图逻辑、配置段落——比纯文字直观
3. **截图放在 `docs/images/`** 目录下，用相对路径引用
4. **中文文档**，变量名/函数名保留英文

<!-- TODO: 环境要求、依赖、外部链接等写在下面 -->
