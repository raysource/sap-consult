sap.ui.define([], function () {
  "use strict";

  // 视图格式化工具 (通过 XML 视图里的 core:require 引用)
  return {
    // 示例: 金额本地化(留作扩展点, 演示格式化器写法)
    formatCurrency: function (fValue, sCurrency) {
      if (fValue == null) { return ""; }
      var sSymbol = (sCurrency === "CNY") ? "¥" : (sCurrency === "USD" ? "$" : sCurrency + " ");
      return sSymbol + Number(fValue).toLocaleString("zh-CN", { minimumFractionDigits: 2 });
    }
  };
});
