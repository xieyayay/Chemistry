# AI 对话系统

> DeepSeek API · VaRest · TextToSpeech。

## 概述

项目接入了 DeepSeek 大模型，用户在前端输入问题，通过 VaRest 插件发 HTTP 请求到 DeepSeek API，返回的答案显示在对话面板上，同时用 TextToSpeech 语音朗读。

## 学习来源

本模块的实现全程参考 B 站视频：

https://www.bilibili.com/video/BV1EPNEeQEcM/?spm_id_from=333.337.search-card.all.click&vd_source=b8f35d6b8b01aaa29ccd685ef5fd7b18

## 架构流程

```
用户输入文字
    ↓
VaRest 构造 JSON 请求
    ↓
POST → https://api.deepseek.com/v1/chat/completions
    ↓
解析返回的 JSON → 提取 AI 回复文本
    ↓
┌─→ 显示在 UMG 对话面板
└─→ TextToSpeech 语音朗读
```

## 涉及的文件

```
Content/Deepseek/
├── UMG_dialogPanel.uasset        ← 对话面板主 Widget
├── UMG_UserContent.uasset        ← 用户消息气泡
├── UMG_servioceContent.uasset    ← AI 回复气泡
└── Sound_TS/                     ← TTS 音频缓存
```

## 用到的插件

| 插件 | 用途 |
|------|------|
| VaRest | 发 HTTP 请求、构造/解析 JSON |
| TextToSpeech | 将 AI 回复转成语音朗读 |
