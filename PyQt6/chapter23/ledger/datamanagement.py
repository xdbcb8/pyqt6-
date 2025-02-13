#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   datamanagement.py
@Time    :   2024/01/23 11:20:01
@Author  :   yangff 
@Version :   1.0
@微信公众号:  学点编程吧
'''

import hashlib
from dbmanagement import DbManager
from PyQt6.QtCore import QDate

# 账户、分类、流水、密码操作类

dataBase = DbManager() # 连接数据库初始化

class AccountManagement:
    """
    账户操作类
    """
    def loadAllAccount(self):
        """
        载入全部一级账户
        """
        sql = "SELECT accountName FROM accounts ORDER BY accountName DESC"
        loadAllAccountResutl = dataBase.query(sql)
        return loadAllAccountResutl
    
    def loadAllSubAccount(self, accountName):
        """
        载入一级账户下全部二级账户
        accountName：一级账户的名称
        """
        sql = f"SELECT subaccountName FROM subaccountview WHERE accountName='{accountName}'"
        loadAllSubAccountResutl = dataBase.query(sql)
        return loadAllSubAccountResutl
    
    def loadAllSubAccountBalance(self, subaccountName):
        """
        载入某个二级账户的余额
        subaccountName：二级账户的名称
        """
        sql = f"SELECT totalMoney FROM subaccountbalanceview WHERE subaccountName='{subaccountName}'"
        loadAllSubAccountBalance = dataBase.query(sql)
        return loadAllSubAccountBalance
    
    def loadAccountBalance(self):
        """
        载入全部一级账户的余额（根据流水进行计算）
        """
        sql_1 = "SELECT accountName, totalMoney FROM accountbalanceview where totalMoney <> 0 ORDER BY totalMoney"
        accountBalance = dataBase.query(sql_1)
        sql_2 = "SELECT MAX(totalMoney), MIN(totalMoney) FROM accountbalanceview"
        maxormin = dataBase.query(sql_2)
        return accountBalance, maxormin
    
    def loadSubAccountBalance(self):
        """
        载入全部二级账户的余额（根据流水进行计算）
        """
        sql_1 = "SELECT subaccountName, totalMoney FROM subaccountbalanceview where totalMoney <> 0 ORDER BY totalMoney"
        subaccountBalance = dataBase.query(sql_1)
        sql_2 = "SELECT MAX(totalMoney), MIN(totalMoney) FROM subaccountbalanceview"
        maxormin = dataBase.query(sql_2)
        return subaccountBalance, maxormin

    def loadassets(self, dateS, dateE):
        """
        载入净资产的每月值
        dateS：开始日期
        dateE：结束日期
        """
        sql_1 = f"SELECT last_day_of_month_str, cumulative_total FROM assetsview WHERE last_day_of_month_str BETWEEN '{dateS}' AND '{dateE}'"
        assetsResult = dataBase.query(sql_1)
        sql_2 = f"SELECT MAX(cumulative_total) AS max_cumulative_total, MIN(cumulative_total) AS min_cumulative_total FROM assetsview WHERE last_day_of_month_str BETWEEN '{dateS}' AND '{dateE}';"
        maxinResult = dataBase.query(sql_2)
        return assetsResult, maxinResult

    def loadAllBanks(self):
        """
        载入全部银行名称
        """
        sql = "SELECT cleaned_subaccountName FROM bankview"
        loadAllBanks = dataBase.query(sql)
        return loadAllBanks      
    
    def loadAllRecentSubAccount(self):
        """
        载入全部的最近使用账户
        """
        sql = "SELECT accountName, subaccountName FROM recentaccountview"
        loadAllRecentSubAccountResutl = dataBase.query(sql)
        return loadAllRecentSubAccountResutl
    
    def loadALLassets(self):
        """
        返回净资产
        """
        sql = "SELECT sum(totalMoney) FROM accountbalanceview"
        assets = dataBase.query(sql)
        return assets
    
    def addRecentAccount(self, subaccount, datetime):
        """
        新增最近使用的账户
        subaccount：二级账户
        datetime：使用日期时间
        """
        isaccount = self.queryAccountID(subaccount ,3)
        if isaccount:
            idsubaccount, idaccount = isaccount[0][0], isaccount[0][1]
            sql = f"INSERT INTO recentaccount (idsubaccount, idaccount, dateTimeAccount) VALUES('{idsubaccount}', '{idaccount}', '{datetime}')"
            isok = dataBase.execute(sql)
            if isok == "execut_error":
                return "execut_recentaccount_error"
            else:
                return "success"

    def queryAccountID(self, account, level):
        """
        查找账户表中的账户ID
        account：一级或二级账户名称
        level：等级标记
        """
        if level == 1: # 一级账户
            sql = f"SELECT idaccount FROM accounts WHERE accountName='{account}'"
        elif level == 2: # 二级账户
            sql = f"SELECT idsubaccount FROM subaccount WHERE subaccountName='{account}'"
        elif level == 3: # 二级账户，多一个数据
            sql = f"SELECT idsubaccount, idaccount FROM subaccount WHERE subaccountName='{account}'"
        isExist = dataBase.query(sql)
        return isExist
    
    def addAccount(self, account):
        """
        增加一级账户
        account：账户名称
        """
        isExist = self.queryAccountID(account, 1)
        if isExist:
            return "existed"
        else:
            sql = f"INSERT INTO accounts (accountName) VALUES('{account}')"
            isok = dataBase.execute(sql)
            if isok == "execut_error":
                return "execut_account_error"
            else:
                return "success"
            
    def addSubAccount(self, subaccount, account):
        """
        增加二级账户
        subaccount：二级账户名称
        account：一级账户名称
        """
        isExist = self.queryAccountID(subaccount, 2)
        if isExist:
            return "existed"
        else:
            isaccountok = self.queryAccountID(account, 1)
            if isaccountok:
                idaccount = isaccountok[0][0]
                sql = f"INSERT INTO subaccount (subaccountName, idaccount) VALUES('{subaccount}', '{idaccount}')"
                isok = dataBase.execute(sql)
                if isok == "execut_error":
                    return "execut_subaccount_error"
                else:
                    return "success"
            
    def renameAccount(self, oldaccount, newaccount):
        """
        修改一级账户
        oldaccount：原有的一级账户名称
        newaccount：新的一级账户名称
        """
        isok = self.queryAccountID(oldaccount, 1)
        if isok:
            idaccount = isok[0][0]
            sql = f"UPDATE accounts SET accountName='{newaccount}' WHERE idaccount='{idaccount}'"
            isok = dataBase.execute(sql)
            if isok == "execut_error":
                return "execut_account_error"
            else:
                return "success"
        
    def renameSubAccount(self, oldsubaccount, newsubaccount):
        """
        修改二级账户
        oldsubaccount：原有的二级账户名称
        newsubaccount：新的二级账户名称
        """
        isok = self.queryAccountID(oldsubaccount, 2)
        if isok:
            idsubaccount = isok[0][0]
            sql = f"UPDATE subaccount SET subaccountName='{newsubaccount}' WHERE idsubaccount='{idsubaccount}'"
            isok = dataBase.execute(sql)
            if isok == "execut_error":
                return "execut_subaccount_error"
            else:
                return "success"
        
    def delAccount(self, account):
        """
        删除一级账户分类
        account：一级账户名称
        """
        isok = self.queryAccountID(account, 1)
        if isok:
            idaccount = isok[0][0]
            sql_1 = f"DELETE FROM accounts WHERE idaccount='{idaccount}'" # 删除一级账户表中的账户信息
            isok = dataBase.execute(sql_1)
            if isok == "execut_error":
                return "execut_account_error"
            else:
                sql_2 = f"DELETE FROM flowfunds WHERE idaccount='{idaccount}'" # 删除流水表中的账户信息
                isok2 = dataBase.execute(sql_2)
                if isok2 == "execut_error":
                    return "execut_flowfunds_error"
                else:
                    sql_3 = f"DELETE FROM recentaccount WHERE idaccount='{idaccount}'" # 删除最近账户表中的账户信息
                    isok3 = dataBase.execute(sql_3)
                    if isok3 == "execut_error":
                        return "execut_recentaccount_error"
                    else:
                        return "success"

    def delSubAccount(self, subaccount):
        """
        删除二级账户分类
        subaccount：二级账户名称
        """
        isok = self.queryAccountID(subaccount, 2)
        if isok:
            idsubaccount = isok[0][0]
            sql_1 = f"DELETE FROM subaccount WHERE idsubaccount='{idsubaccount}'" # 删除二级账户表中的账户信息
            isok = dataBase.execute(sql_1)
            if isok == "execut_error":
                return "execut_subaccount_error"
            else:
                sql_2 = f"DELETE FROM flowfunds WHERE idsubaccount='{idsubaccount}'" # 删除流水表中的二级账户信息
                isok2 = dataBase.execute(sql_2)
                if isok2 == "execut_error":
                    return "execut_flowfunds_error"
                else:
                    sql_3 = f"DELETE FROM recentaccount WHERE idsubaccount='{idsubaccount}'" # 删除最近账户表中的账户信息
                    isok3 = dataBase.execute(sql_3)
                    if isok3 == "execut_error":
                        return "execut_recentaccount_error"
                    else:
                        return "success"
        
class ClassificationManagement:
    """
    支出/收入分类操作类
    """
    def loadAllClassification(self, flag):
        """
        载入全部一级支出/收入分类
        flag：收、支的标志
        """
        sql = f"SELECT classificationName FROM classification WHERE flag='{flag}'"
        loadAllClassificationResutl = dataBase.query(sql)
        return loadAllClassificationResutl
    
    def loadAllSubClassification(self, classificationName, flag):
        """
        载入全部二级支出/收入分类
        classificationName：一级分类名称
        flag：收、支的标志
        """
        sql = f"SELECT subclassificationName FROM subclassificationview WHERE flag='{flag}' AND classificationName='{classificationName}'"
        loadAllSubClassificationResutl = dataBase.query(sql)
        return loadAllSubClassificationResutl

    def loadClassificationflow(self, start, end, flag):
        """
        载入全部一级分类的支出或收入的余额
        start：开始日期
        end：结束日期
        flag：收、支的标志
        """
        if flag == "out":
            dxy = "<"
        else:
            dxy = ">"
        sql_1 = f"SELECT classificationName, round(sum(money),2) FROM flowfundsview WHERE chargeDateTime BETWEEN '{start}' AND '{end}' AND classificationName IS NOT NULL AND money{dxy}0 GROUP BY classificationName ORDER BY round(sum(money),2)"
        classificationflow = dataBase.query(sql_1)
        sql_2 = f"""SELECT   
    MAX(rounded_sum) as max_rounded_sum,  
    MIN(rounded_sum) as min_rounded_sum  
FROM (  
    SELECT   
        ROUND(SUM(money), 2) as rounded_sum  
    FROM   
        flowfundsview  
    WHERE   
        chargeDateTime BETWEEN '{start}' AND '{end}'   
        AND classificationName IS NOT NULL   
        AND money {dxy} 0  
    GROUP BY   
        classificationName  
)AS subquery;
            """
        maxormin = dataBase.query(sql_2)
        return classificationflow, maxormin    
        
    def loadsubClassificationflow(self, start, end, flag):
        """
        载入全部二级分类的支出或收入TOP10
        start：开始日期
        end：结束日期
        flag：收、支的标志
        """
        if flag == "out":
            dxy = "<"
            sql_1 = f"SELECT subclassificationName, round(sum(money),2) FROM flowfundsview WHERE chargeDateTime BETWEEN '{start}' AND '{end}' AND subclassificationName IS NOT NULL AND money{dxy}0 GROUP BY subclassificationName ORDER BY round(sum(money),2) LIMIT 10"
        else:
            dxy = ">"
            sql_1 = f"SELECT subclassificationName, round(sum(money),2) FROM flowfundsview WHERE chargeDateTime BETWEEN '{start}' AND '{end}' AND subclassificationName IS NOT NULL AND money{dxy}0 GROUP BY subclassificationName ORDER BY round(sum(money),2) LIMIT 10"
        subclassificationflow = dataBase.query(sql_1)
        sql_2 = f"""SELECT   
    MAX(rounded_sum) as max_rounded_sum,  
    MIN(rounded_sum) as min_rounded_sum  
FROM (  
    SELECT   
        ROUND(SUM(money), 2) as rounded_sum  
    FROM   
        flowfundsview  
    WHERE   
        chargeDateTime BETWEEN '{start}' AND '{end}'   
        AND subclassificationName IS NOT NULL   
        AND money {dxy} 0  
    GROUP BY   
        subclassificationName  
)AS subquery;
            """
        maxormin = dataBase.query(sql_2)
        return subclassificationflow, maxormin
      
    def loadAllRecentClassification(self, flag):
        """
        载入最近使用的支出/收入分类
        flag：收、支的标志
        """
        sql = f"SELECT classificationName, subclassificationName FROM recentclassificationview WHERE flag='{flag}'"
        loadAllSubClassificationResutl = dataBase.query(sql)
        return loadAllSubClassificationResutl
    
    def addRecentClassification(self, subclassification, flag, datetime):
        """
        新增最近使用的支出/收入分类
        subclassification：二级分类名称
        flag：收、支的标志
        datetime：日期时间
        """
        isclassification = self.queryClassificationID(subclassification, 3, flag)
        if isclassification:
            idsubclassification, idclassification = isclassification[0][0], isclassification[0][1]
            sql = f"INSERT INTO recentclassification (idsubclassification, idclassification, flag, dateTimeClassification) VALUES('{idsubclassification}', '{idclassification}', '{flag}', '{datetime}')"
            isok = dataBase.execute(sql)
            if isok == "execut_error":
                return "execut_recentclassificaiton_error"
            else:
                return "success"
    
    def queryClassificationID(self, classification, level, flag):
        """
        查找支出/收入分类表中的分类ID
        classification：一、二级分类名称
        level：等级的标志
        flag：收、支的标志
        """
        if level == 1: # 一级分类
            sql = f"SELECT idclassification FROM classification WHERE classificationName='{classification}' AND flag='{flag}'"
        elif level == 2: # 二级分类
            sql = f"SELECT idsubclassification FROM subclassification WHERE subclassificationName='{classification}' AND flag='{flag}'"
        elif level == 3: # 二级分类，多个数据
            sql = f"SELECT idsubclassification, idclassification FROM subclassification WHERE subclassificationName='{classification}' AND flag='{flag}'"
        isExist = dataBase.query(sql)
        return isExist
    
    def addClassification(self, classification, flag):
        """
        增加一级支出/收入分类
        classification：一级分类名称
        flag：收、支的标志
        """
        isExist = self.queryClassificationID(classification, 1, flag)
        if isExist:
            return "existed"
        else:
            sql = f"INSERT INTO classification (classificationName, flag) VALUES('{classification}', '{flag}')"
            isok = dataBase.execute(sql)
            if isok == "execut_error":
                return "execut_classification_error"
            else:
                return "success"
            
    def addSubClassification(self, subclassificaiton, classification, flag):
        """
        增加二级支出/收入分类
        subclassificaiton：二级分类名称
        classification：一级分类名称
        flag：收、支的标志
        """
        isExist = self.queryClassificationID(subclassificaiton, 2, flag)
        if isExist:
            return "existed"
        else:
            isclassificationID = self.queryClassificationID(classification, 1, flag)
            if isclassificationID:
                classificationID = isclassificationID[0][0]
                sql = f"INSERT INTO subclassification (subclassificationName, idclassification, flag) VALUES('{subclassificaiton}', '{classificationID}', '{flag}')"
                isok = dataBase.execute(sql)
                if isok == "execut_error":
                    return "execut_subclassification_error"
                else:
                    return "success"
            
    def renameclassification(self, oldclassification, newclassification, flag):
        """
        修改一级支出/收入分类
        oldclassification：旧的一级分类名称
        newclassification：新的一级分类名称
        flag：收、支的标志
        """
        isok = self.queryClassificationID(oldclassification, 1, flag) # 查看一级支出/收入分类id
        if isok:
            classificationID = isok[0][0]
            sql = f"UPDATE classification SET classificationName='{newclassification}' WHERE idclassification='{classificationID}' AND flag='{flag}'"
            isok = dataBase.execute(sql)
            if isok == "execut_error":
                return "execut_classification_error"
            else:
                return "success"
        
    def renameSubclassification(self, oldsubclassification, newsubclassification, flag):
        """
        修改二级支出/收入分类
        oldsubclassification：旧的二级分类名称
        newsubclassification：新的二级分类名称
        flag：收、支的标志
        """
        isok = self.queryClassificationID(oldsubclassification, 2, flag) # 查看二级支出/收入分类
        if isok:
            subclassificationID = isok[0][0]
            sql = f"UPDATE subclassification SET subclassificationName='{newsubclassification}' WHERE idsubclassification='{subclassificationID}' AND flag='{flag}'"
            isok = dataBase.execute(sql)
            if isok == "execut_error":
                return "execut_subclassification_error"
            else:
                return "success"
        
    def delClassification(self, classification, flag):
        """
        删除一级支出/收入分类
        classification：一级分类名称
        flag：收、支的标志
        """
        isok = self.queryClassificationID(classification, 1, flag) # 查看一级支出/收入分类
        if isok:
            classificationID = isok[0][0]
            sql_1 = f"DELETE FROM classification WHERE idclassification='{classificationID}' AND flag='{flag}'" # 删除一级支出/收入分类表中的分类信息
            isok = dataBase.execute(sql_1)
            if isok == "execut_error":
                return "execut_classification_error"
            else:
                sql_2 = f"DELETE FROM flowfunds WHERE idclassification='{classificationID}'" # 删除流水表中的分类信息
                isok2 = dataBase.execute(sql_2)
                if isok2 == "execut_error":
                    return "execut_flowfunds_error"
                else:
                    sql_3 = f"DELETE FROM recentclassification WHERE idclassification='{classificationID}'" # 删除最近分类表中的分类信息
                    isok3 = dataBase.execute(sql_3)
                    if isok3 == "execut_error":
                        return "execut_recentaccount_error"
                    else:
                        return "success"
        
    def delSubClassification(self, subclassification, flag):
        """
        删除二级支出/收入分类
        subclassification：二级分类名称
        flag：收、支的标志
        """
        isok = self.queryClassificationID(subclassification, 2, flag) # 查看二级支出/收入分类
        if isok:
            subclassificationID = isok[0][0]
            sql = f"DELETE FROM subclassification WHERE idsubclassification='{subclassificationID}' AND flag='{flag}'" # 删除二级支出/收入分类表中的分类信息
            isok = dataBase.execute(sql)
            if isok == "execut_error":
                return "execut_subclassification_error"
            else:
                sql_2 = f"DELETE FROM flowfunds WHERE idsubclassification='{subclassificationID}'" # 删除流水表中的分类信息
                isok2 = dataBase.execute(sql_2)
                if isok2 == "execut_error":
                    return "execut_flowfunds_error"
                else:
                    sql_3 = f"DELETE FROM recentclassification WHERE idsubclassification='{subclassificationID}'" # 删除最近分类表中的分类信息
                    isok3 = dataBase.execute(sql_3)
                    if isok3 == "execut_error":
                        return "execut_recentaccount_error"
                    else:
                        return "success"
        
class PwdManagement:
    """
    密码操作类
    """
    def pwdEncryption(self, pwd):
        """
        密码加密（MD5加密方式）
        pwd：密码
        """
        md5 = hashlib.md5() # 返回md5哈希对象
        md5.update(pwd.encode("utf-8")) # 使用参数中的字节更新哈希对象
        return md5.hexdigest() # 摘要以双倍长度的字符串形式返回的，只包含十六进制数字。

    def queryPwd(self):
        """
        查看是否有密码
        """
        sql = f"SELECT password FROM pwdsetting"
        pwd = dataBase.query(sql)
        if not pwd:
            return ""
        return pwd[0][0]
    
    def comparePwd(self, upwd):
        """
        比较数据库中的密码和用户填写的密码是否一致
        upwd：用户填写的密码
        """
        upwdE = self.pwdEncryption(upwd)
        oldPwd = self.queryPwd()
        if upwdE == oldPwd:
            return True
        else:
            return False

    def settingPwd(self, pwd):
        """
        设置密码
        """
        pwdE = self.pwdEncryption(pwd)
        if not self.queryPwd():
            sql = f"INSERT INTO pwdsetting (password) VALUES('{pwdE}')"
        else:
            sql = f"UPDATE pwdsetting SET password='{pwdE}'"
        isok = dataBase.execute(sql)
        if isok == "execut_error":
            return "execut_pwd_error"
        else:
            return "success"
        
class FlowFunds:
    """
    支出/收入流水操作类
    """

    def __init__(self):
        self.accountM = AccountManagement()
        self.classificationM = ClassificationManagement()

    def loadAllFlowfunds(self, flag, dateStart, dateEnd, start, end):
        """
        从流水视图中载入全部支出/收入流水
        flag：区分支持还是收入
        dateStart：开始日期
        dateEnd：结束日期
        start：开始数据
        end：结束数据
        """
        if flag == "in":
            sql = f"SELECT chargeDateTime, accountName, subaccountName, classificationName, subclassificationName, money, beizhu, idflowfunds FROM flowfundsview WHERE money>0 AND chargeDateTime BETWEEN '{dateStart}' AND '{dateEnd}' ORDER BY chargeDateTime LIMIT {start}, {end} "
        else:
            sql = f"SELECT chargeDateTime, accountName, subaccountName, classificationName, subclassificationName, money, beizhu, idflowfunds FROM flowfundsview WHERE money<0 AND chargeDateTime BETWEEN '{dateStart}' AND '{dateEnd}' ORDER BY chargeDateTime LIMIT {start}, {end}"
        loadAllFlowfundsResutl = dataBase.query(sql)
        return loadAllFlowfundsResutl
    
    def addFlowfunds(self, subaName, subcName, money, beizhu, dateTime):
        """
        新增支出/收入流水
        subaName：二级账户名称
        subcName：二级分类名称
        money：金额
        beizhu：备注
        dateTime：流水产生的日期时间
        """
        isaccontok = self.accountM.queryAccountID(subaName, 3)
        if isaccontok:
            idsubaccount, idaccount = isaccontok[0][0], isaccontok[0][1]
            if subcName: # 不转账，考虑分类
                if money > 0: # 根据钱来判断是收入还是支出
                    flag = 'in'
                else:
                    flag = 'out'
                isclassificationok = self.classificationM.queryClassificationID(subcName, 3, flag)
                if isclassificationok:
                    idsubclassification, idclassification = isclassificationok[0][0], isclassificationok[0][1]
                    sql = f"INSERT INTO flowfunds (idaccount, idsubaccount, idclassification, idsubclassification, money, beizhu, chargeDateTime) VALUES('{idaccount}', '{idsubaccount}', '{idclassification}', '{idsubclassification}', '{money}', '{beizhu}', '{dateTime}')"    
                    isok = dataBase.execute(sql)
                    if isok == "execut_error":
                        return "execut_flowfunds_error"
                    else:
                        return "success"
            else: # 转账，不考虑分类
                sql = f"INSERT INTO flowfunds (idaccount, idsubaccount, idclassification, idsubclassification, money, beizhu, chargeDateTime) VALUES('{idaccount}', '{idsubaccount}', NULL, NULL, '{money}', '{beizhu}', '{dateTime}')"    
                isok = dataBase.execute(sql)
                if isok == "execut_error":
                    return "execut_flowfunds_error"
                else:
                    return "success"
        
    def modifyFlowfunds(self, idflowfunds, aName, subaName, cName, subcName, money, beizhu, dateTime):
        """
        修改支出/收入流水
        idflowfunds：流水id
        aName：一级账户名称
        subaName：二级账户名称
        cName：分类名称
        subcName：二级分类名称
        money：金额
        beizhu：备注
        dateTime：流水日期时间
        """
        if money > 0:
            flag = 'in'
        else:
            flag = 'out'
        issubaccountok = self.accountM.queryAccountID(subaName, 2)
        if issubaccountok:
            idsubaccount = issubaccountok[0][0]
        isaccountok = self.accountM.queryAccountID(aName, 1)
        if isaccountok:
            idaccount = isaccountok[0][0]
        issubclasok = self.classificationM.queryClassificationID(subcName, 2, flag)
        if issubclasok:
            idsubclassification = issubclasok[0][0]
        isclaok = self.classificationM.queryClassificationID(cName, 1, flag)
        if isclaok:
            idclassification = isclaok[0][0]
        if not cName: # 没有分类情况，例如转账
            sql = f"UPDATE flowfunds SET idaccount='{idaccount}', idsubaccount='{idsubaccount}', idclassification=null, idsubclassification=null, money={money}, beizhu='{beizhu}', chargeDateTime='{dateTime}' WHERE idflowfunds='{idflowfunds}'"
        else:
            sql = f"UPDATE flowfunds SET idaccount='{idaccount}', idsubaccount='{idsubaccount}', idclassification='{idclassification}', idsubclassification='{idsubclassification}', money={money}, beizhu='{beizhu}', chargeDateTime='{dateTime}' WHERE idflowfunds='{idflowfunds}'"
        isok = dataBase.execute(sql)
        if isok == "execut_error":
            return "execut_flowfunds_error"
        else:
            return "success"

    def delFlowfunds(self, idflowfunds):
        """
        删除支出/收入流水
        idflowfunds：流水id
        """
        sql = f"DELETE FROM flowfunds WHERE idflowfunds='{idflowfunds}'" # 根据id号删除支出/收入流水
        isok = dataBase.execute(sql)
        if isok == "execut_error":
            return "execut_flowfunds_error"
        else:
            return "success"
        
    def totalPages(self, flag, dateStart, dateEnd):
        """
        返回流水的总数
        flag：收、支的标志
        dateStart：开始日期
        dateEnd：结束日期
        """
        if flag == "in": # 收入
            sql = f"SELECT count(idflowfunds) FROM flowfundsview WHERE money>0 AND chargeDateTime BETWEEN '{dateStart}' AND '{dateEnd}'"
        else: # 支出
            sql = f"SELECT count(idflowfunds) FROM flowfundsview WHERE money<0 AND chargeDateTime BETWEEN '{dateStart}' AND '{dateEnd}'"
        totalResutl = dataBase.query(sql)
        return totalResutl
    
    def todayFlow(self):
        """
        返回今天的收支情况
        """
        today = QDate.currentDate().toString("yyyy-MM-dd") # 今日
        sqlin = f"SELECT Round(sum(money), 2) FROM flowfundsview WHERE date(chargeDateTime)='{today}' AND money > 0 AND classificationName is not NULL" # 收入
        sqlout = f"SELECT Round(sum(money),2) FROM flowfundsview WHERE date(chargeDateTime)='{today}' AND money < 0 AND classificationName is not NULL" # 支出
        inResult = dataBase.query(sqlin)
        outResult = dataBase.query(sqlout)
        if inResult:
            result_in = inResult[0][0]
        else:
            result_in = 0
        if outResult:
            result_out = outResult[0][0]
        else:
            result_out = 0
        return result_in, result_out

    def monthFlow(self):
        """
        返回当月的收支情况
        """
        month = QDate.currentDate().toString("yyyy-MM") # 当月
        sqlin = f"SELECT Round(sum(money),2) FROM flowfundsview WHERE DATE_FORMAT(chargeDateTime, '%Y-%m')='{month}' AND money > 0 AND classificationName is not NULL" # 收入
        sqlout = f"SELECT Round(sum(money),2) FROM flowfundsview WHERE DATE_FORMAT(chargeDateTime, '%Y-%m')='{month}' AND money < 0 AND classificationName is not NULL" # 支出
        inResult = dataBase.query(sqlin)
        outResult = dataBase.query(sqlout)
        if inResult:
            result_in = inResult[0][0]
        else:
            result_in = 0
        if outResult:
            result_out = outResult[0][0]
        else:
            result_out = 0
        return result_in, result_out
    
    def yearFlow(self):
        """
        返回今年的收支情况
        """
        year = QDate.currentDate().toString("yyyy") # 本年度
        sqlin = f"SELECT Round(sum(money),2) FROM flowfundsview WHERE year(chargeDateTime)='{year}' AND money > 0 AND classificationName is not NULL" # 收入
        sqlout = f"SELECT Round(sum(money),2) FROM flowfundsview WHERE year(chargeDateTime)='{year}' AND money < 0 AND classificationName is not NULL" # 支出
        inResult = dataBase.query(sqlin)
        outResult = dataBase.query(sqlout)
        if inResult:
            result_in = inResult[0][0]
        else:
            result_in = 0
        if outResult:
            result_out = outResult[0][0]
        else:
            result_out = 0
        return result_in, result_out

    def outinFlow(self, dateStart, dateEnd, flag):
        """
        返回某个时间段的支出情况
        dateStart：开始日期时间
        dateEnd：结束日期时间
        flag：支持还是收入的标志
        """
        if flag == "in":
            sql = f"SELECT subclassificationName, Round(sum(money),2) as money FROM flowfundsview WHERE money > 0 AND subclassificationName IS NOT NULL AND chargeDateTime BETWEEN '{dateStart}' AND '{dateEnd}' GROUP BY subclassificationName ORDER BY sum(money)"
        else:
            sql = f"SELECT subclassificationName, Round(sum(money),2) as money FROM flowfundsview WHERE money < 0 AND subclassificationName IS NOT NULL AND chargeDateTime BETWEEN '{dateStart}' AND '{dateEnd}' GROUP BY subclassificationName ORDER BY sum(money)"
        outResult = dataBase.query(sql)
        return outResult

    def dayFlow(self, start, end):
        """
        返回日支出情况，不含转账
        start：开始日期
        end：结束日期
        """
        sql = f"""SELECT   
    DATE_FORMAT(chargeDateTime, '%Y-%m-%d') AS chargeDateTime,  
    ABS(ROUND(SUM(money), 2)) AS totalmoney,  
    MAX(ABS(ROUND(SUM(money), 2))) OVER () AS max_totalmoney,
    MIN(ABS(ROUND(SUM(money), 2))) OVER () AS min_totalmoney
FROM   
    flowfundsview  
WHERE   
    money < 0  
    AND subclassificationName IS NOT NULL  
    AND chargeDateTime BETWEEN '{start}' AND '{end}'  
GROUP BY   
    DATE_FORMAT(chargeDateTime, '%Y-%m-%d')  
ORDER BY   
    chargeDateTime;
        """
        dayResutl = dataBase.query(sql)
        return dayResutl