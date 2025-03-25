// wx docs: https://mp.weixin.qq.com/wxopen/plugindevdoc?appid=wxaed5ace05d92b218&token=&lang=zh_CN

const shareImageToGameCenter = (config) => {
  return new Promise((resolve) => {
    console.log("MiniGameCommon: shareImageToGameCenter resolve", JSON.stringify(config));
    setTimeout(() => {
      resolve('Mock shareImageToGameCenter Success Response');
    }, 500);
  });
};

const miniGameCommon = {
  // 只有 快来当领主 直接通过miniGameCommon.gameClub调用shareImageToGameCenter
  gameClub:{
    shareImageToGameCenter
  },

  createGameClub:()=>{
    console.log("MiniGameCommon: createGameClub");
    return {
      shareImageToGameCenter
    };
  },

  canIUse:(str)=>{
    console.log("MiniGameCommon: canIUse",str);
    return true;
  },

  createGameTimeLine: () => {
    console.log("MiniGameCommon: createGameTimeLine");
    const timeline = {
      authorized: false, // 属性应该属于返回的对象
      on: (str, func) => {
        console.log("MiniGameCommon: timeLine on", str);
        if (func) {
          setTimeout(() => {
            func();
          }, 500);
        }
      },
      authorize: () => {
        return new Promise((resolve) => {
          console.log("MiniGameCommon: timeLine authorize");
          setTimeout(() => {
            timeline.authorized = true; // 修改返回对象的属性
            resolve();
          }, 500);
        });
      },
      pushFeed: (data) => {
        return new Promise((resolve) => {
          console.log("MiniGameCommon: timeLine pushFeed", data);
          setTimeout(() => {
            resolve();
          }, 500);
        });
      },
    };
    return timeline;
  },
  
  // createGameRewarded错误代码表
  // enum ErrorCode {
  //   OK = 0,
  //   NETWORK_FAILED = 1001,            // 网络失败
  //   INNER_ERROR = 1002,               // 其他错误，详见 res.errInfo 字段
  //   NOT_LOAD = 1005,                  // 还未 load 即执行 show
  //   ENV_UNSUPPORT = 1007,             // 当前运行环境不支持，目前仅支持安卓设备
  //   // 订单相关
  //   ORDER_TIMEOUT = 1101,             // 订单超时，需要重新 load
  //   ORDER_NO_AVAILABLE = 1102,        // 无订单可用，UI关闭入口
  //   ORDER_DONE = 1103,                // 支付完成
  //   ORDER_CANCEL = 1104,              // 用户取消支付
  //   ORDER_WAITING = 1105,             // 支付结果等待，可轮询数秒等待结果
  // }
  createGameRewarded:()=>{
    console.log("MiniGameCommon: createGameRewarded");  
    return {
      load:({obj})=>{
        console.log("MiniGameCommon: createGameRewarded load",obj.signData);
        setTimeout(() => {
          const mockRes = {
            errCode: 1105, // mock实现，也许不合适
            message: "Illegal mocked fail response"
          };
          obj.fail&&obj.fail(mockRes);
          obj.complete&&obj.complete(mockRes);
        }, 500);
      },
      show:({success,fail,complete})=>{
        console.log("MiniGameCommon: createGameRewarded show");  
        setTimeout(() => {
          const mockRes = {
            errCode: 1001, // mock实现，也许不合适: 1103是支付成功，1104是取消支付，1105是订单超时
            errMsg: "Illegal mocked fail response",
            errInfo:{}
          };
          fail&&fail(mockRes);
          complete&&complete(mockRes);
        }, 500);
      },
      destroy:()=>{
        console.log("MiniGameCommon: createGameRewarded destroy");  
      },
      onLoad:(func)=>{ 
        console.log("MiniGameCommon: createGameRewarded onLoad");  
        const mockRes = {
          errCode:1001,
          errMsg:"Illegal Mock Message",
          errInfo:{}
        }
        func(mockRes);
      },
      onError:(func)=>{
        console.log("MiniGameCommon: createGameRewarded.onError");  
        const mockRes = {
          errCode: 1000, // mock实现，也许不合适
        }
        func(mockRes);
        return "MiniGameCommon.createGameRewarded.onErrormock message";
      },
    }
  },

  // createPopupActivity 错误代码表
  //   0	用户关闭弹窗
  // 10001	已显示弹窗，请勿重复调用
  // 10002	弹窗接口返回错误数据，或者用户已购买完
  // 10003	弹窗接口返回错误数据
  // 10004	网络错误，弹窗数据接口访问失败
  // 10005	弹窗渲染失败
  // 10006	支付异常
  // 10007	没有权限
  // 10008	暂不支持
  // -1	支付系统失败
  // -2	支付取消
  // -15001	虚拟支付接口错误码，缺少参数
  // -15002	虚拟支付接口错误码，参数不合法
  // -15003	虚拟支付接口错误码，订单重复
  // -15004	虚拟支付接口错误码，后台错误
  // -15005	虚拟支付接口错误码，appId 权限被封禁
  // -15006	虚拟支付接口错误码，货币类型不支持
  // -15007	虚拟支付接口错误码，订单已支付
  // -15009	虚拟支付接口错误码，由于健康系统限制，本次支付已超过限额（这种错误情况会有默认弹窗提示）
  // -15010	虚拟支付接口错误码，正式版小游戏不允许在沙箱环境支付
  // 1	虚拟支付接口错误码，用户取消支付
  // 2	虚拟支付接口错误码，客户端错误，判断到小程序在用户处于支付中时，又发起了一笔支付请求
  // 3	虚拟支付接口错误码，Android 独有错误:用户使用 GooglePlay 支付，而手机未安装 GooglePlay
  // 4	虚拟支付接口错误码，用户操作系统支付状态异常
  // 5	虚拟支付接口错误码，操作系统错误
  // 6	虚拟支付接口错误码，其他错误
  // 7	虚拟支付接口错误码，支付取消
  // 1000	参数错误
  // 1001	分区未发布
  // 1003	米大师 Portal 错误
  createPopupActivity: () => {
    console.log("MiniGameCommon: createPopupActivity");
    return {
      showPopup: (data) => {
        console.log("MiniGameCommon: showPopup", data.actId);
        return new Promise((resolve, reject) => {
          console.log("MiniGameCommon: showPopup reject");
          setTimeout(() => {
            reject({
              errCode: 1001, // 模拟错误码
              message: "Mocked showPopup fail response"
            });
          }, 500);
        });
      },
      requestMidasPayment: (data) => {
        console.log("MiniGameCommon: requestMidasPayment", data);
        return new Promise((resolve, reject) => {
          console.log("MiniGameCommon: requestMidasPayment reject");
          setTimeout(() => {
            reject({
              errCode: 2001, // 模拟错误码
              message: "Mocked requestMidasPayment fail response"
            });
          }, 500);
        });
      }
    };
  },
  

  createGameReport:()=>{
    console.log("MiniGameCommon: createGameReport");  
    return {
      start:()=>{
        console.log("MiniGameCommon: createGameReport start");  
      },
      on:(str,func)=>{
        console.log("MiniGameCommon: createGameReport on",str);  
        if(func)
          setTimeout(() => {
            func();
          }, 500);
      },
      reportEvent:(eventId,data)=>{
        console.log("MiniGameCommon: createGameReport reportEvent",eventId,data);  
      },
      stop:()=>{
        console.log("MiniGameCommon: createGameReport stop");  
      }
    };
  },

  // 仅仅在穿越火线-枪战王者中出现过对此接口的调用 官方文档中未提及
  createPrivacy:()=>{ 
    return {
      launch:()=>{
        console.log("MiniGameCommon: createPrivacy launch");  
        return new Promise((resolve) => { 
          console.log("MiniGameCommon: createPrivacy launch resolve"); 
          setTimeout(() => {
            resolve();
          }, 500);
        })
      }
    }
  },
};
  
// 导出 miniGameCommon 为默认导出
module.exports = { 
  default: () => miniGameCommon 
};