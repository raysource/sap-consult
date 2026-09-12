sap.ui.define([
  "sap/ui/core/UIComponent",
  "sap/ui/Device"
], function (UIComponent, Device) {
  "use strict";

  // 应用组件: UIComponent + manifest 描述 (见 manifest.json)
  return UIComponent.extend("com.training.products.Component", {

    metadata: {
      manifest: "json",
      // 紧凑/舒适模式的自动适配(移动端舒适, 桌面紧凑)
      properties: {
        contentDensityMode: {
          type: "string",
          defaultValue: Device.system.desktop ? "Compact" : "Cozy"
        }
      }
    },

    init: function () {
      // 调用父类 init -> 解析 manifest, 实例化根视图等
      UIComponent.prototype.init.apply(this, arguments);
      // 主题/密度: 让所有控件感知 (sapUiSizeCompact 样式类)
      this.getRootControl().addStyleClass(this.getContentDensityMode());
    }
  });
});
