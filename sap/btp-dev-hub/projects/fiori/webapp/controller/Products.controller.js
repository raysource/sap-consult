sap.ui.define([
  "sap/ui/core/mvc/Controller",
  "sap/ui/model/Filter",
  "sap/ui/model/FilterOperator",
  "sap/m/MessageToast",
  "sap/m/MessageBox"
], function (Controller, Filter, FilterOperator, MessageToast, MessageBox) {
  "use strict";

  return Controller.extend("com.training.products.controller.Products", {

    // ---------------- 搜索(列表过滤) ----------------
    onSearch: function (oEvent) {
      var sQuery = (oEvent.getParameter("query") || "").trim();
      var aFilters = [];
      if (sQuery) {
        aFilters.push(new Filter({
          filters: [
            new Filter("name", FilterOperator.Contains, sQuery),
            new Filter("category", FilterOperator.Contains, sQuery)
          ],
          and: false   // 名称 OR 分类 命中即可
        }));
      }
      this.byId("productsList").getBinding("items").filter(aFilters);
    },

    // ---------------- 按单价排序(切换升降序) ----------------
    onToggleSort: function () {
      var oBinding = this.byId("productsList").getBinding("items");
      var oSorter = oBinding.getSorter()[0];
      var bDesc = !(oSorter && oSorter.bDescending);
      oBinding.sort(new sap.ui.model.Sorter("price", bDesc));

      // 同步按钮图标/提示
      var oBtn = this.byId("sortButton");
      oBtn.setIcon(bDesc ? "sap-icon://sort-descending" : "sap-icon://sort-ascending");
      oBtn.setTooltip(bDesc ? "按单价从高到低" : "按单价从低到高");
      MessageToast.show(bDesc ? "已按单价 高 → 低 排序" : "已按单价 低 → 高 排序");
    },

    // ---------------- 重新加载本地数据 ----------------
    onRefresh: function () {
      var oModel = this.getView().getModel("products");
      if (oModel) { oModel.refresh(); }
      MessageToast.show("已刷新");
    },

    // ---------------- 点击某行 ----------------
    onItemPress: function (oEvent) {
      var oCtx = oEvent.getParameter("listItem").getBindingContext("products");
      if (!oCtx) { return; }
      var oProduct = oCtx.getObject();
      var bLow = oProduct.stock <= oProduct.reorderLevel;

      MessageBox.show(
        "产品: " + oProduct.name + "\n" +
        "单价: " + oProduct.price + " " + oProduct.currency + "\n" +
        "库存: " + oProduct.stock + (bLow ? "  ⚠ 低于补货阈值 " + oProduct.reorderLevel : ""),
        { title: "产品详情", icon: bLow ? MessageBox.Icon.WARNING : MessageBox.Icon.INFORMATION }
      );
    },

    // ---------------- 页脚帮助 ----------------
    onShowHelp: function () {
      MessageBox.information(
        "这是一个 Freestyle SAPUI5 应用示例。\n\n" +
        "数据来源: data/products.json (JSONModel)。\n" +
        "生产形态: 把 JSONModel 换成 ODataModel 指向 CAP/ RAP/ S/4HANA 服务即可。\n" +
        "参考本站 Fiori / CAP 页面获得更多指引。",
        { title: "关于本示例" }
      );
    }
  });
});
