package com.training.catalog;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * CAP Java 应用入口 (Spring Boot)
 *
 * <p>启动后自动完成: 装配 CDS 模型 -> 生成 OData V4 端点 ->
 * 事件处理器注册 -> 安全配置(此处为 mock 用户)。
 */
@SpringBootApplication
public class Application {

  public static void main(String[] args) {
    SpringApplication.run(Application.class, args);
  }
}
