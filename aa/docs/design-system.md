# 设计系统

文档站用的是 **Aether** —— 一套磨砂玻璃材质的设计系统（Apple 亮色语言）。
规范原文在项目根目录的 `DESIGN.md`，本页是所有组件的实际渲染效果，改样式时以这里为准。

<div class="aa-note" markdown>
**给写文档的人：** 你不需要懂 HTML。正文里能直接用的是
[按钮](#按钮)、[徽章](#徽章)、[提示框](#提示框) 和 [图标](#图标)，
下面的写法照抄即可。其余组件（命令坞、标签页、开关等）属于站点框架的一部分，
由样式表统一控制，正文里用不到。
</div>

## 颜色

整站的颜色只有下面这些，全部定义在 `stylesheets/system.css` 里。
**写新样式时请引用变量，不要写死色值。**

<div class="aa-swatches">
<div class="aa-swatch"><span class="aa-swatch__chip" style="background: var(--color-bg)"></span><b>页面底</b><code>--color-bg</code></div>
<div class="aa-swatch"><span class="aa-swatch__chip" style="background: var(--color-surface-glass-strong)"></span><b>玻璃面</b><code>--color-surface-glass-strong</code></div>
<div class="aa-swatch"><span class="aa-swatch__chip" style="background: var(--color-ink)"></span><b>石墨（墨色）</b><code>--color-ink</code></div>
<div class="aa-swatch"><span class="aa-swatch__chip" style="background: var(--color-ink-secondary)"></span><b>石板（次级）</b><code>--color-ink-secondary</code></div>
<div class="aa-swatch"><span class="aa-swatch__chip" style="background: var(--color-ink-tertiary)"></span><b>雾（三级）</b><code>--color-ink-tertiary</code></div>
<div class="aa-swatch"><span class="aa-swatch__chip" style="background: var(--color-accent)"></span><b>系统蓝（强调）</b><code>--color-accent</code></div>
<div class="aa-swatch"><span class="aa-swatch__chip" style="background: var(--color-success)"></span><b>成功</b><code>--color-success</code></div>
<div class="aa-swatch"><span class="aa-swatch__chip" style="background: var(--color-warning)"></span><b>警告</b><code>--color-warning</code></div>
<div class="aa-swatch"><span class="aa-swatch__chip" style="background: var(--color-danger)"></span><b>危险</b><code>--color-danger</code></div>
</div>

!!! warning "强调色的用法有严格限制"

    系统蓝只用于**焦点环、链接、开关的开启态**。不要拿它当按钮底色或装饰色 ——
    设计规范里写得很明确：玻璃材质上加彩色填充会直接破坏质感。
    同理，石墨 `--color-ink` 只用于主操作、选中态和文字，不能拿来做大面积背景。

## 排版

字体是 **Inter**（正文）+ **JetBrains Mono**（代码、键盘按键、数字）。
中文没有对应字形时回落到系统黑体（苹方 / 微软雅黑），不会出现方块。

<div class="aa-type">
<p class="display">Display 48 / 600</p>
<p class="h1">标题 32 / 600</p>
<p class="h2">小标题 24 / 600</p>
<p class="text-body">正文 15 / 400 —— 这是文档正文的默认字号，行高 1.6，字距 -0.002em。</p>
<p class="text-label">标签 13 / 500 —— 用于次级说明</p>
<p class="text-micro">Micro 11 / 600 / 大写</p>
<p class="text-mono">JetBrains Mono 0123456789</p>
</div>

!!! tip "标题不要超过 600 字重"

    `700` 及以上的粗体会破坏系统的冷静语气。正文里用 `**加粗**` 会被渲染成 600，
    这是上限。

## 按钮

正文里直接写 Markdown 就能生成按钮：

```markdown
[次要按钮](design-system.md){ .md-button }
[主要按钮](design-system.md){ .md-button .md-button--primary }
```

实际效果：

[次要按钮](#按钮){ .md-button }
[主要按钮](#按钮){ .md-button .md-button--primary }

设计系统还定义了更细的按钮层级（玻璃药丸 + 炭黑图标圆片），
用于首页 hero 那种强调场景：

<div class="row-wrap">
<button class="btn btn-primary">开始阅读<span class="chip"><span class="aa-i aa-i-arrow-right"></span></span></button>
<button class="btn btn-secondary">次要操作</button>
<button class="btn btn-tertiary">文字按钮</button>
<button class="btn btn-solid">高优先级</button>
<button class="btn btn-icon"><span class="aa-i aa-i-settings"></span></button>
</div>

悬停会微微上浮，按下会向内收紧 —— 这是「玻璃被按过边缘」的触感，
不是简单的变色。

## 徽章

```markdown
<span class="badge">草稿</span>
<span class="badge badge-accent">已验证</span>
```

<span class="badge">草稿</span>
<span class="badge badge-accent">已验证</span>
<span class="badge">UE 5.4.4</span>

徽章是小号大写字母 + 宽字距，用来标状态或版本，不承担主要信息。

## 提示框

用 MkDocs 原生的 admonition 语法，圆角和材质已经按设计系统调好：

```markdown
!!! note "标题"
    内容

!!! warning "注意"
    内容
```

!!! note "普通说明"

    用于补充信息，不打断阅读节奏。

!!! tip "技巧"

    用于「这样做更好」的建议。

!!! warning "注意"

    用于「这样做会出问题」的提醒。

!!! danger "危险操作"

    用于不可逆、会丢数据的操作。

## 卡片

容器类内容用卡片：24px 圆角玻璃板，内边距 24px。

<div class="aa-cards">
<div class="card">
<div class="card-header"><h3 class="card-title">任务系统</h3><span class="card-icon is-soft"><span class="aa-i aa-i-layers"></span></span></div>
<div class="card-body">DataTable 驱动，按步骤推进。任务状态存在 SaveGame 里，切关卡不丢。</div>
<div class="card-footer"><span class="badge badge-accent">已完成</span><span class="text-label">12 页</span></div>
</div>
<div class="card card-raised">
<div class="card-header"><h3 class="card-title">AI 对话系统</h3><span class="card-icon"><span class="aa-i aa-i-zap"></span></span></div>
<div class="card-body">接入外部 API，带对话面板与 TTS 语音合成。API Key 走配置文件，不要提交到仓库。</div>
<div class="card-footer"><span class="badge">进行中</span><span class="text-label">8 页</span></div>
</div>
</div>

## 表单控件

<div class="aa-form">
<label class="field">
<span class="field-label">搜索文档</span>
<span class="input"><span class="aa-i aa-i-search"></span><input type="text" placeholder="输入关键词…"></span>
</label>
<label class="field">
<span class="field-label">备注（多行）</span>
<span class="input input-area"><textarea placeholder="多行输入用 24px 圆角，给内容留出呼吸空间"></textarea></span>
</label>
<div class="row-wrap">
<label class="checkbox"><input type="checkbox" checked><span class="checkbox-box"></span>记住这个选择</label>
<label class="switch"><input type="checkbox" checked><span class="switch-track"><span class="switch-thumb"></span></span>启用语音</label>
</div>
</div>

键盘按键用 `<kbd>`：

按 <kbd>Ctrl</kbd> + <kbd>S</kbd> 保存，按 <kbd>F5</kbd> 重新构建。

## 标签页

<div class="tabs">
<button class="tab is-active"><span class="aa-i aa-i-user"></span>概览</button>
<button class="tab"><span class="aa-i aa-i-layers"></span>结构</button>
<button class="tab"><span class="aa-i aa-i-settings"></span>配置</button>
<button class="tab"><span class="aa-i aa-i-bell"></span>通知</button>
</div>

选中态是炭黑药丸，未选中是雾色文字 —— 像一枚卡进凹槽的筹码。

## 命令坞

这是整套设计系统的招牌组件：搜索药丸 + 玻璃图标片 + 竖分隔线 + 主按钮，
全部叠在一层带折射高光的玻璃上。

<div class="dock">
<span class="dock-search"><span class="aa-i aa-i-search"></span>搜索文档、蓝图、插件…</span>
<button class="dock-chip is-active"><span class="aa-i aa-i-layers"></span></button>
<button class="dock-chip"><span class="aa-i aa-i-zap"></span></button>
<button class="dock-chip"><span class="aa-i aa-i-bell"></span></button>
<span class="dock-divider"></span>
<button class="btn btn-primary">开始<span class="chip"><span class="aa-i aa-i-arrow-right"></span></span></button>
</div>

!!! note "文档站里为什么看不到它"

    命令坞是 App 界面的组件（全局搜索 + 快捷操作），文档站的导航由 MkDocs 的
    侧边栏承担，没有它的位置。上方的搜索框用的是同一套材质语言（玻璃药丸 +
    聚焦换系统蓝描边），只是形态更简单。

## 图标

图标全部来自 **Lucide**，统一 `1.75` 描边、继承当前文字颜色。
不要在页面里手写 SVG 路径，也不要引入别的图标库。

正文里插图标写成这样：

```markdown
<span class="aa-i aa-i-check"></span>
```

`aa-i` 是基础类，`aa-i-<名字>` 选具体图标。图标颜色自动跟随周围文字颜色，
所以放在标题里就是标题色，放在链接里就是系统蓝，不用单独设色。

图标类由 `tools/build_icons_css.py` 从 `overrides/.icons/lucide/` 生成。
**要加新图标**：把 SVG 放进那个目录，然后重跑一次脚本：

```bash
python tools/build_icons_css.py
```

<span class="aa-i aa-i-search"></span>
<span class="aa-i aa-i-sun"></span>
<span class="aa-i aa-i-moon"></span>
<span class="aa-i aa-i-layers"></span>
<span class="aa-i aa-i-zap"></span>
<span class="aa-i aa-i-check"></span>
<span class="aa-i aa-i-bell"></span>
<span class="aa-i aa-i-settings"></span>
<span class="aa-i aa-i-user"></span>

## 玻璃与层级

所有玻璃面都由三层叠成：**填充 + 发丝线描边 + 内倒角高光 + 外悬浮阴影**。
四者缺一不可 —— 发丝线是浏览器不支持背景模糊时唯一还存在的边缘。

<div class="aa-glass-demo">
<div class="glass">普通玻璃<br><span class="text-label">--color-surface-glass · 0.55</span></div>
<div class="glass-strong">加厚玻璃<br><span class="text-label">--color-surface-glass-strong · 0.75</span></div>
<div class="card card-raised">抬升卡片<br><span class="text-label">--color-surface-raised · 0.85 + 更强的外阴影</span></div>
</div>

!!! warning "玻璃不要叠超过两层"

    背景模糊是靠「透过玻璃看到后面的东西」制造错觉的。叠到第三层之后，
    后面的东西已经被前面的玻璃糊掉了，质感会塌掉变成一块灰板。

## 无障碍

以下三条是硬性要求，改样式时不能破坏：

1. **焦点环不能删。** 每个可交互元素都必须有 `:focus-visible` 的
   3px 系统蓝焦点环。用键盘 <kbd>Tab</kbd> 走一遍页面，焦点必须始终可见。
2. **发丝线不能删。** 见上文，它是玻璃面在降级环境下的唯一边缘。
3. **尊重「减少动态效果」。** 系统在 `prefers-reduced-motion` 下会自动把
   所有过渡压到 1ms，这是 `system.css` 里统一处理的，不要覆盖。
