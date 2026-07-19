# 材质系统

> 材质 · Material Instance · Substrate · 视觉效果。

<!--
  写作指引：
  这一章讲项目中的材质相关技术和规范。

  建议覆盖：
  ★ 材质组织方式
    - 基底材质（M_）和材质实例（MI_）的区别
    - 你的项目里材质放在哪些目录
  ★ Material Instance 模式
    - 基底材质定义哪些参数
    - 实例怎么覆写（颜色、贴图、粗糙度…）
    - 动态材质实例（运行时修改参数）
  ★ 特殊材质类型
    - 液体材质（水的折射、流动）
    - 透明/半透明材质（玻璃器皿）
    - 发光材质（加热变红）
  ★ Niagara 与材质的配合
    - Niagara 的 Sprite/Ribbon Renderer 怎么绑定材质
    - Dynamic Parameter 怎么传给材质
  ★ Substrate（如果用了）
    - 和旧版材质的区别
    - 你项目中 Substrate 的具体用法
  ★ 性能
    - 透明材质性能开销
    - 纹理分辨率建议
-->
