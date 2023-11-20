from selenium.webdriver.common.keys import Keys
import platform

testServer = 'http://localhost:8050/login'  # 本地测试环境
# testServer = 'http://172.16.6.62:8080/login'  # 测试环境

controlKey = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL

shortCutDateIDs = ['1', '2', '3', '4', '5',
                   '6', '7', '8', '9', '10', '11', '12']
shortCutName = 'rangePickerShortcut{id}'

# 告警管理
alertEventStatus = ['告警中', '已解决', '已忽略']

alertLevels = ['紧急', '严重', '警告']

alertTypes = ['TiKV', 'PD', 'TiDB', 'TiFlash', '主机', 'BR']

opArr = ['>', '>=', '=', '<', '<=']

alertFrequencyUnits = ['s', 'm', 'h']

alertChannelTypes = ['email', 'https']

alertChannelEnabled = ['是', '否']

# 告警通道
# SMTP服务器
SMTPAddress = 'smtp.qiye.aliyun.com:587'

# SMTP用户名
SMTPUsername = 'tem-alert-noreply@pingcap.cn'

# SMTP密码
SMTPPassword = '#LIeKu^oXB@30fT#'

# 发送者
SMTPSender = '#LIeKu^oXB@30fT#'

# 发送者邮箱
SMTPSenderEmail = 'tem-alert-noreply@pingcap.cn'

# 接收者邮箱
SMTPReceiverEmail = 'xinyi.zhang@pingcap.com.cn'


alertChannelTempStr = '''
{{ range .Alerts }}
=========start==========<br>
告警程序: TEM <br>
告警级别: {{ .Labels.severity }}  <br>
告警名称: {{ .Labels.alertname }} <br>
故障节点: {{ .Labels.instance }} <br>
告警状态: {{ .Status}} <br>
告警主题: {{ .Annotations.summary }} <br>
告警详情: {{ .Annotations.description }} <br>
触发时间: {{ .StartsAt.Format "2006-01-02 15:04:05 (MST)" }} <br>
结束时间: {{ .EndsAt.Format "2006-01-02 15:04:05 (MST)"}} <br>
=========end==========<br>
{{ end }}
'''

# 测试的告警规则名称
testAlertRuleTempName = 'TiDB_monitor_keep_alive_copy'


# 集群管理
singleMenuNameArr = ['menu.cluster.single.overview', 'menu.cluster.single.monitor', 'menu.cluster.single.performance',
                     'menu.cluster.single.backup', 'menu.cluster.single.param', 'menu.cluster.single.topology', 'menu.cluster.single.sqleditor']


perfLastTimeArr = ['5', '15', '30', '60', '180',
                   '720', '1440', '2880', '4320', '10080']

rangeStepArr = ['5', '10', '30', '60', '120', '720', '1440']

# 1:DEBUG 2:INFO 3:WARN 5 CRITICAL 6 ERROR
logLevelArr = ['1', '2', '3', '5', '6']

# 备份恢复
backupDestination = '''s3://tem/br/frontend-{}?endpoint=http://minio.pingcap.net:9000&force-path-style=true'''

backupAK = 'minioadmin'

backupSK = 'minioadmin'

backupRateLimitArr = [0, 128, 512, 1024, 2048, 1024768]

backupConcurrencyArr = [0, 4, 16, 128, 512]

backupLogFileArr = ['', '/tmp/backup.log', '/ttest/backup.log']



# 主机管理
hostIP = '172.17.0.17'  # 62 测试环境
# hostIP = '172.17.0.7'   # dev 环境
batchHostIP = '172.17.0.17'  # 批量添加主机


# 备用扩容主机
scaleHostIP = '172.17.0.2' 

hostUserName = 'root'

hostPwd = 'tem'

# 参数组模板管理
paramTemplateParamType = ['TiDB', 'TiKV', 'PD']

# 集群管理
# 纳管集群
takeoverClusterHost = '172.20.12.22'  # 纳管集群 - 中控节点地址信息
takeoverClusterPort = '22'  # 纳管集群 - 中控节点端口信息
tiupPath = '/root/.tiup'  # 纳管集群 - tiup 部署路径
# takeoverClusterHost = '172.20.12.22'  # 纳管集群 - 中控节点地址信息
# takeoverClusterPwd = 'Pingcap!@#456'  # 纳管集群 - 中控节点密码信息
takeoverClusterHost = '127.0.0.1'  # 纳管集群 - 中控节点地址信息
takeoverClusterPwd = 'tem'  # 纳管集群 - 中控节点密码信息

# 单个集群
rangeStepArr = ['5', '10', '30', '60', '120', '720', '1440']

# 1:DEBUG 2:INFO 3:WARN 5 CRITICAL 6 ERROR
logLevelArr = ['1', '2', '3', '5', '6']

scaleCompArr = ['TiDB', 'TiKV', 'PD', 'TiFlash']


# 接口 url
apiPrefix = '/ajax/api/v1/'  # 通用接口前缀

accountPrefix = '{}account/'.format(apiPrefix)  # 账户接口前缀

dmsPrefix = '{}dms/'.format(apiPrefix)  # dms接口前缀

clusterPrefix = '{}cluster/'.format(apiPrefix)  # cluster接口前缀

backupPrefix = '{}br/'.format(dmsPrefix)  # 备份恢复接口前缀

sqlEditorPrefix = '{}sqleditor/'.format(dmsPrefix)  # sql editor接口前缀

observePrefix = '{}observe/'.format(apiPrefix)  # 监控接口前缀

logSearchPrefix = '{}logsearch/'.format(observePrefix)  # 日志检索接口前缀

alertPrefix = '{}alert/'.format(observePrefix)  # 告警接口前缀

inspectPrefix = '{}inspect/'.format(observePrefix)  # 巡检接口前缀

inspectPolicyPrefix = '{}policys/'.format(inspectPrefix)  # 巡检策略接口前缀

apiDict = {
    'login': {'urlStrs': ['/ajax/login'], 'excludeStr': '', 'method': 'POST', 'remark': '登录'},
    'logout': {'urlStrs': ['/ajax/logout'], 'excludeStr': '', 'method': 'POST', 'remark': '登出'},
    'profile': {'urlStrs': ['/ajax/profile'], 'excludeStr': '', 'method': 'GET', 'remark': '获取用户信息'},
    # 用户管理
    # 修改当前账户密码
    'changePassword': {'urlStrs': ['/ajax/profile/password'], 'excludeStr': '', 'method': 'POST', 'remark': '修改密码'},
    'userList': {'urlStrs': ['{}users'.format(accountPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取用户列表'},
    'userAdd': {'urlStrs': ['{}users'.format(accountPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '添加用户'},
    'userEdit': {'urlStrs': ['{}users/'.format(accountPrefix), '/profile'], 'excludeStr': '', 'method': 'POST', 'remark': '编辑用户'},
    'roleList': {'urlStrs': ['{}rbac/roles'.format(accountPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取角色列表'},
    'deleteUser': {'urlStrs': ['{}users/'.format(accountPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除用户'},
    # 修改用户的密码
    'changeUserPwd': {'urlStrs': ['{}users/'.format(accountPrefix), '/password'], 'excludeStr': '', 'method': 'POST', 'remark': '修改用户密码'},
    # 集群管理
    'clusterTops': {'urlStrs': ['{}tidbs/tops'.format(clusterPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取集群 top 信息'},
    'clusterTopAlert': {'urlStrs': ['{}event/top/3/cluster'.format(alertPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取集群 top 告警信息'},
    'clusterList': {'urlStrs': ['{}tidbs/page'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取集群列表'},
    'clusterAdd': {'urlStrs': ['{}tidbs/create'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '添加集群'},
    'clusterDetail': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/detail'], 'excludeStr': '', 'method': 'GET', 'remark': '获取集群信息'},
    'clusterInstance': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/instances'], 'excludeStr': '', 'method': 'GET', 'remark': '获取集群实例信息'},
    'offlineCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/offline'], 'excludeStr': '', 'method': 'POST', 'remark': '下线集群'},
    'reloadCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/reload'], 'excludeStr': '', 'method': 'POST', 'remark': '重载集群'},
    'scaleCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/scale'], 'excludeStr': '', 'method': 'POST', 'remark': '扩容集群'},
    'restartCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/restart'], 'excludeStr': '', 'method': 'POST', 'remark': '重启集群'},
    'destroyCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/destroy'], 'excludeStr': '', 'method': 'POST', 'remark': '销毁集群'},
    'discardCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/discard'], 'excludeStr': '', 'method': 'POST', 'remark': '丢弃集群'},
    'startCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/start'], 'excludeStr': '', 'method': 'POST', 'remark': '启动集群'},
    'stopCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/stop'], 'excludeStr': '', 'method': 'POST', 'remark': '停止集群'},
    'retryCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/retry'], 'excludeStr': '', 'method': 'POST', 'remark': '重试集群'},
    'clusterPerfSummary': {'urlStrs': ['{}tidbs/'.format(dmsPrefix), '/query/load'], 'excludeStr': '', 'method': 'GET', 'remark': '获取集群性能概览'},
    'clusterParamList': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/config'], 'excludeStr': '', 'method': 'GET', 'remark': '获取集群参数列表'},
    'clusterParamEdit': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/config'], 'excludeStr': '', 'method': 'PUT', 'remark': '编辑集群参数'},
    'takeoverCluster': {'urlStrs': ['{}tidbs/takeover'.format(clusterPrefix)], 'excludeStr': '/remote', 'method': 'POST', 'remark': '纳管集群'},
    'takeoverRemoteClusterList': {'urlStrs': ['{}tidbs/takeover/remote/list'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取可纳管集群列表'},
    'takeoverRemoteDetail': {'urlStrs': ['{}tidbs/takeover/remote/detail'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取可纳管集群详情'},
    'clusterAlertSummary': {'urlStrs': ['{}event/cluster/summary'.format(alertPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取集群告警概览'},
    # 集群管理  SQL Editor
    'querySQLEditorMeta': {'urlStrs': ['{}clusters/'.format(sqlEditorPrefix), '/meta'], 'excludeStr': '', 'method': 'GET', 'remark': '获取元数据'},
    'querySQLEditorMetaDB': {'urlStrs': ['{}clusters/'.format(sqlEditorPrefix), '/dbs/', '/meta'], 'excludeStr': '', 'method': 'GET', 'remark': '获取数据库列表'},
    'createSQLEditorSession': {'urlStrs': ['{}clusters/'.format(sqlEditorPrefix), '/session'], 'excludeStr': '', 'method': 'POST', 'remark': '创建会话'},
    'deleteSQLEditorSession': {'urlStrs': ['{}clusters/'.format(sqlEditorPrefix), '/session'], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除会话'},
    'createSQLEditorFile': {'urlStrs': ['{}sqlFile'.format(sqlEditorPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '创建SQL文件'},
    'querySQLEditorFileList': {'urlStrs': ['{}sqlFiles'.format(sqlEditorPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取SQL文件列表'},
    'querySQLEditorFileDetail': {'urlStrs': ['{}sqlFiles/'.format(sqlEditorPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取SQL文件详情'},
    'updateSQLEditorFile': {'urlStrs': ['{}sqlFiles/'.format(sqlEditorPrefix)], 'excludeStr': '', 'method': 'PUT', 'remark': '更新SQL文件'},
    'deleteSQLEditorFile': {'urlStrs': ['{}sqlFiles/'.format(sqlEditorPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除SQL文件'},
    'executeSQLEditorStatement': {'urlStrs': ['{}statement'.format(sqlEditorPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '执行SQL语句'},
    'querySQLEditorStatementHistory': {'urlStrs': ['{}statements'.format(sqlEditorPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取SQL语句历史'},
    'querySQLEditorSearchResult': {'urlStrs': ['{}statement'.format(sqlEditorPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '查询SQL语句'},
    # 集群管理  监控指标
    'queryClusterMonitorInfo': {'urlStrs': ['{}metrics/query'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取集群监控指标信息'},
    'startClusterInspection': {'urlStrs': ['{}reports/create'.format(inspectPrefix), '/start'], 'excludeStr': '', 'method': 'POST', 'remark': '发起巡检'},
    'deleteClusterInspecReport': {'urlStrs': ['{}reports/'.format(inspectPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除巡检报告'},
    # 集群管理  性能诊断
    'queryClusterTopSqlList': {'urlStrs': ['{}topsql/list'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取集群 top sql 列表'},
    'queryClusterSlowQueryList': {'urlStrs': ['{}slowquery/lists'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取集群慢查询列表'},
    'queryClusterDiagnoseReportList': {'urlStrs': ['{}diagnose/reports'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取集群诊断报告列表'},
    'createClusterDiagnoseReport': {'urlStrs': ['{}diagnose/reports'.format(clusterPrefix)], 'excludeStr': '', 'method': 'PUT', 'remark': '创建集群诊断报告'},
    'queryClusterDiagnoseReportStatus': {'urlStrs': ['{}diagnose/reports/'.format(clusterPrefix), '/status'], 'excludeStr': '', 'method': 'GET', 'remark': '获取集群诊断报告状态'},
    'queryClusterDiagnoseReportDetail': {'urlStrs': ['{}diagnose/reports/reportInfo'.format(clusterPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取集群诊断报告详情'},
    'createClusterLogSearchTask': {'urlStrs': ['{}taskgroup'.format(logSearchPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '创建日志检索任务'},
    'queryClusterLogSearchTaskList': {'urlStrs': ['{}taskgroups/'.format(logSearchPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取日志检索任务列表'},
    'queryClusterLogSearchList': {'urlStrs': ['{}taskgroups/'.format(logSearchPrefix), '/preview'], 'excludeStr': '', 'method': 'POST', 'remark': '获取日志检索列表'},
    'cancelClusterLogSearchTask': {'urlStrs': ['{}taskgroups/'.format(logSearchPrefix), '/cancel'], 'excludeStr': '', 'method': 'POST', 'remark': '取消日志检索任务'},
    'retryClusterLogSearchTask': {'urlStrs': ['{}taskgroups/'.format(logSearchPrefix), '/retry'], 'excludeStr': '', 'method': 'POST', 'remark': '重试日志检索任务'},
    'queryClusterLogSearchTaskID': {'urlStrs': ['{}taskgroup'.format(logSearchPrefix)], 'excludeStr': '', 'method': 'PUT', 'remark': '获取日志检索任务ID'},
    'queryClusterLogSearchTopology': {'urlStrs': ['{}topology'.format(logSearchPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取日志检索拓扑'},
    # 备份恢复
    'backupCluster': {'urlStrs': ['{}backup'.format(backupPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '备份集群'},
    'queryBackupPoliciesList': {'urlStrs': ['{}policies'.format(backupPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取备份策略列表'},
    'queryBackupPolicy': {'urlStrs': ['{}policy'.format(backupPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取备份策略详情'},
    'updateBackupPolicy': {'urlStrs': ['{}policies/'.format(backupPrefix)], 'excludeStr': '', 'method': 'PUT', 'remark': '更新备份策略'},
    'deleteBackupPolicy': {'urlStrs': ['{}policies/'.format(backupPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除备份策略'},
    'createBackupPolicy': {'urlStrs': ['{}policy'.format(backupPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '创建备份策略'},
    'preCheckBackupPolicy': {'urlStrs': ['{}policy/preCheck'.format(backupPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '检测备份集群策略'},
    'restoreCluster': {'urlStrs': ['{}restore'.format(backupPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '恢复集群'},
    'queryBackupTopSummary': {'urlStrs': ['{}summary/top/'.format(backupPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取备份概览'},
    'queryBackupTaskList': {'urlStrs': ['{}tasks'.format(backupPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取备份任务列表'},
    'deleteBackupTask': {'urlStrs': ['{}tasks/'.format(backupPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除备份任务'},
    'startBackupTask': {'urlStrs': ['{}tasks/'.format(backupPrefix), '/start'], 'excludeStr': '', 'method': 'POST', 'remark': '启动备份任务'},
    'stopBackupTask': {'urlStrs': ['{}tasks/'.format(backupPrefix), '/stop'], 'excludeStr': '', 'method': 'POST', 'remark': '停止备份任务'},
    'detectRestoreCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/detect'], 'excludeStr': '', 'method': 'POST', 'remark': '集群恢复-测试'},
    'queryRestoreBackupList': {'urlStrs': ['{}/backups'.format(clusterPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取备份列表'},
    # 告警管理
    'queryAlertEventList': {'urlStrs': ['{}events'.format(alertPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取告警事件列表'},
    'queryAlertRuleList': {'urlStrs': ['{}rules'.format(alertPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取告警规则列表'},
    'createAlertRule': {'urlStrs': ['{}rule'.format(alertPrefix)], 'excludeStr': '/rules', 'method': 'POST', 'remark': '创建告警规则'},
    'updateAlertRule': {'urlStrs': ['{}rules/'.format(alertPrefix)], 'excludeStr': '', 'method': 'PUT', 'remark': '更新告警规则'},
    'switchAlertRuleStatus': {'urlStrs': ['{}rules/'.format(alertPrefix)], 'excludeStr': '', 'method': 'PUT', 'remark': '切换告警规则状态'},
    'deleteAlertRule': {'urlStrs': ['{}rules/'.format(alertPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除告警规则'},
    'queryAlertChannelList': {'urlStrs': ['{}channels'.format(alertPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取告警通道列表'},
    'createAlertChannel': {'urlStrs': ['{}channel'.format(alertPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '创建告警通道'},
    'updateAlertChannel': {'urlStrs': ['{}channels/'.format(alertPrefix)], 'excludeStr': '', 'method': 'PUT', 'remark': '更新告警通道'},
    'deleteAlertChannel': {'urlStrs': ['{}channels/'.format(alertPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除告警通道'},
    'queryAllAlertRuleList': {'urlStrs': ['{}rules'.format(alertPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取所有告警规则列表'},
    'testAlertChannelEmail': {'urlStrs': ['{}channel/test'.format(alertPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '测试告警通道邮件'},
    'queryAlertRuleDetail': {'urlStrs': ['{}rules/'.format(alertPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取告警规则详情'},
    'queryAlertRuleIndicators': {'urlStrs': ['{}rule/indicators'.format(alertPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取告警规则指标'},
    # 主机管理
    'querySpecList': {'urlStrs': ['{}resource/spec'.format(apiPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取主机规格列表'},
    'createSpec': {'urlStrs': ['{}resource/spec'.format(apiPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '创建主机规格'},
    'updateSpec': {'urlStrs': ['{}resource/spec'.format(apiPrefix)], 'excludeStr': '', 'method': 'PUT', 'remark': '更新主机规格'},
    'deleteSpec': {'urlStrs': ['{}resource/spec'.format(apiPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除主机规格'},
    'queryHostList': {'urlStrs': ['{}resource/host'.format(apiPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取主机列表'},
    'discoverHost': {'urlStrs': ['{}resource/discovery'.format(apiPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '发现主机'},
    'createHost': {'urlStrs': ['{}resource/host'.format(apiPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '创建主机'},
    'updateHost': {'urlStrs': ['{}resource/host'.format(apiPrefix)], 'excludeStr': '', 'method': 'PUT', 'remark': '更新主机'},
    'deleteHost': {'urlStrs': ['{}resource/host'.format(apiPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除主机'},
    'queryHostMonitor': {'urlStrs': ['{}resource/monitor'.format(apiPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取主机监控信息'},
    'queryHostOption': {'urlStrs': ['{}resource/option'.format(apiPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取主机配置'},
    # 参数组模板管理
    'queryParamTemplateList': {'urlStrs': ['{}paramgroup'.format(clusterPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取参数组模板列表'},
    'queryParamTemplateParams': {'urlStrs': ['{}paramgroup/params'.format(clusterPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取参数组模板参数'},
    'createParamTemplate': {'urlStrs': ['{}paramgroup'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '创建参数组模板'},
    'updateParamTemplate': {'urlStrs': ['{}paramgroup/'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '更新参数组模板'},
    'queryParamTemplateDetail': {'urlStrs': ['{}paramgroup/'.format(clusterPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取参数组模板详情'},
    'deleteParamTemplate': {'urlStrs': ['{}paramgroup/'.format(clusterPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除参数组模板'},
    'applyParamTemplate': {'urlStrs': ['{}paramgroup/'.format(clusterPrefix), '/apply'], 'excludeStr': '', 'method': 'POST', 'remark': '应用参数组模板'},
    'applyConfigCluster': {'urlStrs': ['{}tidbs/'.format(clusterPrefix), '/config'], 'excludeStr': '', 'method': 'POST', 'remark': '应用集群配置'},
    'applyClusterToParamTemplate': {'urlStrs': ['{}paramgroup/cluster/'.format(clusterPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '应用集群到参数组模板'},
    # 巡检管理
    'queryInspecPolicyList': {'urlStrs': ['{}page'.format(inspectPolicyPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取巡检策略列表'},
    'queryInpecReportList': {'urlStrs': ['{}reports/page'.format(inspectPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取巡检报告列表'},
    'queryInspections': {'urlStrs': ['{}inspections/page'.format(inspectPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取巡检列表'},
    'createInspecPolicy': {'urlStrs': ['{}create'.format(inspectPolicyPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '创建巡检策略'},
    'updateInspecPolicy': {'urlStrs': ['{}update'.format(inspectPolicyPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '更新巡检策略'},
    'queryInspecPolicyDetail': {'urlStrs': ['{}'.format(inspectPolicyPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取巡检策略详情'},
    'deleteInspection': {'urlStrs': ['{}inspections/'.format(inspectPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除巡检'},
    'createInspection': {'urlStrs': ['{}inspections/create'.format(inspectPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '创建巡检'},
    'deleteInspecPolicy': {'urlStrs': ['{}'.format(inspectPolicyPrefix)], 'excludeStr': '', 'method': 'DELETE', 'remark': '删除巡检策略'},
    'queryClusterInspecReportDetail': {'urlStrs': ['{}reports/'.format(inspectPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取集群巡检报告详情'},
    # 审计管理
    'queryAuditList': {'urlStrs': ['{}audit'.format(apiPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取审计列表'},
    'updateAuditConfig': {'urlStrs': ['{}audit'.format(apiPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '更新审计配置'},
    'enableAudit': {'urlStrs': ['{}audit/enable'.format(apiPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '启用审计'},
    'disableAudit': {'urlStrs': ['{}audit/disable'.format(apiPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '禁用审计'},
    'queryAuditLog': {'urlStrs': ['{}audit/logs'.format(apiPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取审计日志'},
    'queryAuditLogOption': {'urlStrs': ['{}audit/logs/option'.format(apiPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取审计配置'},
    # 任务流
    'queryTaskFlowList': {'urlStrs': ['{}task/flow/page'.format(apiPrefix)], 'excludeStr': '', 'method': 'POST', 'remark': '获取任务流列表'},
    'restartTaskFlow': {'urlStrs': ['{}task/flow/'.format(apiPrefix), '/restart'], 'excludeStr': '', 'method': 'POST', 'remark': '重启任务流'},
    'queryTaskFlowDetail': {'urlStrs': ['{}task/flow/'.format(apiPrefix)], 'excludeStr': '', 'method': 'GET', 'remark': '获取任务流详情'},
}
