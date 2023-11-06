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

![处理集群告警](./assets/backup.svg)


#### 5.执行性能问题诊断

流程图:

![执行性能问题诊断](./assets/performance.svg)


#### 6.执行变更（包含扩缩容）

流程图:

![执行变更（包含扩缩容）](./assets/scale_cluster.svg)
