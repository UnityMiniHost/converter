//wx docs: https://mp.weixin.qq.com/wxopen/plugindevdoc?appid=wxbd990766293b9dc4&token=&lang=zh_CN
// index.js
const LoadingManager = {
  isMainCanvas: true,
  ScaleMode: "NO_BORDER",
  create: function (config) {
    return new Promise((resolve) => {
      console.log("开始加载资源:", config.images);

      // 模拟加载过程
      setTimeout(() => {
        console.log("资源加载完成");
        resolve();
      }, 1000); // 假设加载需要1秒
    });
  },
  destroy: () =>
    new Promise((resolve) => {
      console.log("MinigameLoading: destroy");
      resolve();
    }),
  startProgress: () => console.log("MinigameLoading: startProgress"),
  stopProgress: () => console.log("MinigameLoading: stopProgress"),
  setDuration: (duration) =>
    console.log(`MinigameLoading: setDuration ${duration}`),
  setProgress: (progress) =>
    console.log(`MinigameLoading: setProgress ${progress}`),
  setLoadingText: (text) =>
    console.log(`MinigameLoading: setLoadingText ${text}`),
  setLoadingTextStyle: (style) =>
    console.log("MinigameLoading: setLoadingTextStyle", style),
  setScaleMode: (scaleMode) =>
    console.log(`MinigameLoading: setScaleMode ${scaleMode}`),
  setDesignSize: (size) => console.log("MinigameLoading: setDesignSize", size),
};

// 导出 LoadingManager 为默认导出
module.exports = { default: LoadingManager };