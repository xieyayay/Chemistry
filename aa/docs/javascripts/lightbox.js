/* ==========================================================================
   图片点击放大
   --------------------------------------------------------------------------
   正文里的截图点一下就能全屏看。原生 JS，不依赖任何库，也不需要额外的
   pip 插件（团队只要装 mkdocs-material 就够了）。

   行为：
     · 点正文图片 → 打开遮罩层显示原图
     · 点遮罩 / 关闭按钮 / 按 Esc → 关闭
     · 键盘：图片可 Tab 聚焦，Enter 或空格打开
     · 关闭后焦点回到原来那张图上
     · 图片本身在链接里（<a><img></a>）时不拦截，照常跳转

   样式在 stylesheets/extra.css 第 12 节。
   ========================================================================== */

(function () {
  "use strict";

  var IMG_SELECTOR = ".md-typeset img:not([class])";
  var ZOOMABLE = "aa-zoomable";

  var root = null;
  var imgEl = null;
  var closeBtn = null;
  var lastFocused = null;

  /* --- 遮罩层按需创建，没图片的页面不会产生多余 DOM --------------------- */
  function build() {
    root = document.createElement("div");
    root.className = "aa-lightbox";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-label", "图片预览");
    root.hidden = true;

    closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "aa-lightbox__close";
    closeBtn.setAttribute("aria-label", "关闭图片预览");
    // 复用图标系统（icons.css 里的 CSS 遮罩类）
    closeBtn.innerHTML = '<span class="aa-i aa-i-x"></span>';

    imgEl = document.createElement("img");
    imgEl.className = "aa-lightbox__img";
    imgEl.alt = "";

    root.appendChild(imgEl);
    root.appendChild(closeBtn);
    document.body.appendChild(root);

    // 点图片本身不关，点周围任意地方都关
    root.addEventListener("click", function (e) {
      if (e.target !== imgEl) close();
    });
  }

  function open(source) {
    if (!root) build();

    lastFocused = document.activeElement;
    imgEl.src = source.currentSrc || source.src;
    // 预览图沿用原图的替代文字，读屏软件能念出这是什么
    imgEl.alt = source.alt || "";

    root.hidden = false;
    // 强制一次重排，让 opacity 过渡能从 0 开始
    void root.offsetWidth;
    root.classList.add("is-open");
    document.body.classList.add("aa-lightbox-open");

    closeBtn.focus();
  }

  function close() {
    if (!root || root.hidden) return;

    root.classList.remove("is-open");
    document.body.classList.remove("aa-lightbox-open");

    var finish = function () {
      root.hidden = true;
      imgEl.removeAttribute("src");
    };

    // 等淡出动画结束再真正隐藏；动画被禁用时直接收尾
    var duration = parseFloat(getComputedStyle(root).transitionDuration) || 0;
    if (duration > 0.01) {
      root.addEventListener("transitionend", finish, { once: true });
      // 兜底：过渡事件万一没来，也要收干净
      window.setTimeout(finish, duration * 1000 + 80);
    } else {
      finish();
    }

    if (lastFocused && document.contains(lastFocused)) lastFocused.focus();
    lastFocused = null;
  }

  /* --- 把正文图片变成可点击、可聚焦的控件 ------------------------------- */
  function decorate() {
    var images = document.querySelectorAll(IMG_SELECTOR);

    Array.prototype.forEach.call(images, function (img) {
      // 已经是链接的图片：点击应该跳转，不抢
      if (img.closest("a")) return;
      if (img.classList.contains(ZOOMABLE)) return;

      img.classList.add(ZOOMABLE);
      img.setAttribute("tabindex", "0");
      img.setAttribute("role", "button");
      img.setAttribute("aria-label", img.alt ? "放大图片：" + img.alt : "放大图片");
    });
  }

  document.addEventListener("click", function (e) {
    var img = e.target.closest && e.target.closest("." + ZOOMABLE);
    if (!img) return;
    e.preventDefault();
    open(img);
  });

  document.addEventListener("keydown", function (e) {
    // Esc：无论焦点在哪都能关
    if (e.key === "Escape" || e.key === "Esc") {
      if (root && !root.hidden) {
        e.preventDefault();
        close();
      }
      return;
    }

    // Enter / 空格：聚焦在图片上时打开
    if (e.key !== "Enter" && e.key !== " " && e.key !== "Spacebar") return;

    var img = document.activeElement;
    if (!img || !img.classList || !img.classList.contains(ZOOMABLE)) return;

    e.preventDefault();
    open(img);
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", decorate);
  } else {
    decorate();
  }

  // Material 用的是「即时导航」，切换页面不会重新加载，
  // 所以每次内容替换后都要重新扫一遍图片。
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(decorate);
  }
})();
