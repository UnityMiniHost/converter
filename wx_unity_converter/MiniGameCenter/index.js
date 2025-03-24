// wx docs: https://mp.weixin.qq.com/wxopen/plugindevdoc?appid=wx2ea687f4258401a9&token=&lang=zh_CN
class MinigameCenter {
  constructor({ y, autoShow, logoUrl }) {
    this.y = y || window.screenHeight * 0.3;
    this.autoShow = autoShow || true;
    this.logoUrl = logoUrl || "";
    this.x = 8; // 默认值
    this.backgroundColor = 'rgba(0,0,0,0.5)';
    this.strokeColor = 'rgba(255,255,255,0.2)';
    this.movable = true;
    this.enableSnap = true;
    this.scale = 1;

    console.log("MinigameCenter: Initialized with", { y, autoShow, logoUrl });
  }

  show({ x, y }) {
    console.log("MinigameCenter: show on x:", x, "y:", y);
  }

  hide() {
    console.log("MinigameCenter: hide");
  }

  open(str) {
    console.log("MinigameCenter: open", str);
  }

  close() {
    console.log("MinigameCenter: close");
  }

  setTabs(strs) {
    console.log("MinigameCenter: setTabs");
    for (const item in strs) {
      console.log("setTabs item:", item);
    }
  }

  sendInteract(sendInteractData) {
    console.log("send interact content:", sendInteractData.content);
    return new Promise((resolve, reject) => {
      console.log("MinigameCenter: sendInteract start");
      setTimeout(() => {
        if (sendInteractData.content === "error") {
          console.log("MinigameCenter: reject");
          reject(new Error("Mocked sendInteract error"));
        } else {
          console.log("MinigameCenter: resolve");
          resolve();
        }
      }, 500);
    });
  }

  setChatSignature(data) {
    console.log("MinigameCenter: setChatSignature", data.signature);
  }

  setChatEnable(isEnable, data) {
    console.log("MinigameCenter: setChatEnable", isEnable, data.msg);
  }

  setLiveStickyOpenIds(openIds) {
    console.log("MinigameCenter: setLiveStickyOpenIds", openIds);
    for (const item in openIds) {
      console.log("setTabs item:", item);
    }
  }

  on(str, callback) {
    console.log("MinigameCenter: on", str);
    setTimeout(() => {
      console.log("MinigameCenter: callback");
      let params = {};
      if (str === "authorize") {
        params.rawData = "mocked Raw Data";
        callback(params);
      } else if (str === "interact") {
        params.interactID = -1;
        params.is_self = false;
        params.content = "mocked content";
        callback(params);
      } else {
        callback(); // 模拟事件参数
      }
    }, 500);
  }
}

// 导出为默认构造函数
module.exports = {
  default: MinigameCenter
};

  