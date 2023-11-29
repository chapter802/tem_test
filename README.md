# tem_test 前端自动化测试 (基于 Selenium 和 chrome 浏览器)

### 安装 chrome driver 驱动

#### Mac 系统安装方法

1. 下载驱动程序,需要和当前安装的 chrome 浏览器主版本需要一致
chrome driver [下载地址](https://googlechromelabs.github.io/chrome-for-testing/)
https://googlechromelabs.github.io/chrome-for-testing/

2. 解压下载的文件, 把可执行文件放到 /usr/local/bin 目录
3. 提示：无法打开“chromedriver”，因为无法验证开发者
   * 进入chromedriver存放目录 cd /usr/local/bin/
   * 添加信任 xattr -d com.apple.quarantine chromedriver

### 测试
待补充


### 测试用例以及流程

#### 1. 部署全新集群

流程图:

![部署全新集群](./assets/deploy_new_cluster.svg)


#### 2. 纳管已有集群

流程图:

![纳管已有集群](./assets/takeover_cluster.svg)


#### 3.处理集群告警

流程图:

![处理集群告警](./assets/cluster_alert.svg)


#### 4.执行备份恢复

流程图:

![执行备份恢复](./assets/backup.svg)


#### 5.执行性能问题诊断

流程图:

![执行性能问题诊断](./assets/performance.svg)


#### 6.执行变更（包含扩缩容）

流程图:

![执行变更（包含扩缩容）](./assets/scale_cluster.svg)

#### 用户管理测试流程

  1. 测试admin, cluster_manager 和 cluster_reader 三个内置用户可以正常登录到TEM，并修改其初始密码，并可以通过新的密码登录。
  2. 使用 admin 用户登陆到 TEM ， 进入用户管理页面，创建用户user_test，该用户具有 admin 权限，之后退出。
  3. 使用user_test 用户登陆，之后创建新的用户user_test1, 并赋予 user manager 角色。 之后使用新创建的用户登录，并检查其能够看到的“用户管理” 菜单。 如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test1.
  4. 使用user_test 用户登陆，之后创建新的用户user_test2, 并赋予 cluster manager 角色。 之后使用新创建的用户登录，并检查其能够看到的对应的集群管理，备份恢复等菜单。如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test2.
  5. 使用user_test 用户登陆，之后创建新的用户user_test3, 并赋予 cluster reader 角色。 之后使用新创建的用户登录，并检查其能够看到的对应的集群管理菜单，并且是只读的。如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test3.
  6. 使用user_test 用户登陆，之后创建新的用户user_test4, 并赋予 alert manager 角色。 之后使用新创建的用户登录，并检查其能够看到告警管理菜单和子菜单。如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test4.
  7. 使用 user_test 用户登陆，之后创建新的用户user_test5, 并赋予 alert reader 角色。 之后使用新创建的用户登录，并检查其能够看到告警管理菜单和子菜单, 并且是只读的。如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test5.
  8. 使用 user_test 用户登陆，之后创建新的用户user_test6, 并赋予  backup manager 角色。 之后使用新创建的用户登录，并检查其能够看到备份管理菜单。如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test6.
  9. 使用 user_test 用户登陆，之后创建新的用户user_test7, 并赋予  backup reader 角色。 之后使用新创建的用户登录，并检查其能够看到备份管理菜单， 并且是只读的。如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test7.
  10. 使用 user_test 用户登陆，之后创建新的用户user_test8, 并赋予  host manager 角色。 之后使用新创建的用户登录，并检查其能够看到主机管理菜单。如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test8.
  11. 使用 user_test 用户登陆，之后创建新的用户user_test9, 并赋予  host reader 角色。 之后使用新创建的用户登录，并检查其能够看到主机管理菜单， 并且是只读的。如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test9.
  12. 使用 user_test 用户登陆，之后创建新的用户user_test10, 并赋予  audit manager 角色。 之后使用新创建的用户登录，并检查其能够看到系统审计和审计日志菜单。如果一切正常，接下来使用user_test 用户删除刚刚创建的user_test10.