# 可复用蓝图

> 下次做同样功能，直接来这里搬。

<!--
  写作格式（每个蓝图一段）：
  ### [蓝图名]
  - **文件路径**: Content/xxx/xxx.uasset
  - **做什么**: 一句话
  - **怎么用**: 搬到新项目后改哪几个参数
  - **依赖**: 需要什么插件、什么数据表
-->

---

## 任务系统

详见 [任务系统文档](../systems/task-system.md)。

- **文件路径**: `Content/main_UI/RenWu_UI/BP_rw/`
- **做什么**: DataTable 驱动的实验步骤管理，支持单步/多步点击，自动播关卡序列
- **怎么用**: 复制整文件夹 → 改 `DT_Tasks` 数据表的步骤 → 配置仪器子类的 ID
- **依赖**: `BP_SequenceManager`、`DT_Tasks`、仪器父类

---

## 倒计时

- **文件路径**: `Content/JiaZai_ui/WBP_SYG.uasset`
- **做什么**: 秒的倒计时
- **怎么用**: 复制相关“倒计时”节点，miao设置倒计时多少秒
- **依赖**: 无


---

## 人称切换

- **文件路径**: `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset`（change view）
- **做什么**: 切换一、三人称
- **怎么用**: 复制相关蓝图节点，按快捷键切换人称
- **依赖**: 无


---

## 登入界面

- **文件路径**: `Content/UI/UMG/Logon.uasset`
- **做什么**: 登入注册界面
- **怎么用**: 复制整个文件，调成登入成功后切换的关卡即可，或作别调成
- **依赖**: 无

---

## 设置界面  

- **文件路径**: `Content/UI/UMG/WBP_setting.uasset` 与 `Content/UI/UMG/setting.uasset`
- **做什么**: 
  - 主菜单设置页：分辨率、音量、全屏
  - 场景设置页：分辨率、音量、全屏、人称切换、返回主菜单、退出游戏
- **怎么用**: 
  - 复制两个 Widget 文件 → 拖到新项目的关卡或主菜单里
  - 接上 `打开关卡`（返回主菜单）和 `退出游戏` 节点
  - 音量用 Sound Mix + SaveGame 同步（见下方注意）
  - 分辨率/全屏用 `获取游戏用户设置` → `设置屏幕分辨率` / `设置全屏模式`
- **依赖**: `CMX_allsound`（SoundMix，相当于音量旋钮）、`SCL_allsound`（SoundClass，相当于"所有音效"这个分组）、`SG_Settings`（SaveGame，存音量值）、`CMX_allsound`（SoundMix，相当于音量旋钮）、`change view`（切换人称函数）
> **注意**：音量跨关卡同步必须用 SaveGame，不能只靠 SoundMix。每个 Widget 的 Event Construct 里读存档恢复音量，OnValueChanged 时存到 SaveGame。详见 [蓝图笔记 - SaveGame](blueprint-notes.md)。
<!--
  TODO: 以后每做一个可复用的蓝图，在这里加一段。格式照上面的模板。
  不用追求一次写完，积累式的，想到了就加。
-->
