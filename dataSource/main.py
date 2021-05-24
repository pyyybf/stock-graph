import csv
import re

'''
获取Stock表的信息
'''
stock_data = {}
with open('./resources/stock.csv', 'r', encoding='utf-8') as stock_csv:
    next(stock_csv)
    stock_csv_reader = csv.reader(stock_csv)
    for row in stock_csv_reader:
        stock_data[row[0]] = {
            'name': row[1],
            'quarter_p': 0,
            'quarter_a': 1,
            'halfYear_p': 2,
            'halfYear_a': 3,
            'year_p': 4,
            'year_a': 5,
            'guarantee_a': 0
        }
    stock_csv.close()

# 计算担保总额
non_decimal = re.compile(r'[^\d.]+')
with open('./resources/guarantee_pre.csv', 'r', encoding='utf-8') as guarantee_csv:
    next(guarantee_csv)
    guarantee_csv_reader = csv.reader(guarantee_csv)
    for row in guarantee_csv_reader:
        if int(row[2].split('-')[0]) < 2018:
            continue
        if row[5][-1] == '亿':
            stock_data[row[0]]['guarantee_a'] += float(non_decimal.sub('', row[5]))
        elif row[5][-1] == '万':
            stock_data[row[0]]['guarantee_a'] += float(non_decimal.sub('', row[5])) * 0.0001
        # TODO: 判断币种
    guarantee_csv.close()

'''
写入stockgraph.sql文件
'''
with open('../backend/sql/stockgraph.sql', 'w', encoding='utf-8') as sql:
    '''
    =======================写入文件开头=======================
    '''
    print('写入文件开头')
    sql.write("-- MySQL dump 10.13  Distrib 5.7.19, for macos10.12 (x86_64)\n")
    sql.write("--\n")
    sql.write("-- Host: 127.0.0.1    Database: StockGraph\n")
    sql.write("-- ------------------------------------------------------\n")
    sql.write("-- Server version	5.7.19-log\n")
    sql.write("/*!40101 SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT */;\n")
    sql.write("/*!40101 SET @OLD_CHARACTER_SET_RESULTS = @@CHARACTER_SET_RESULTS */;\n")
    sql.write("/*!40101 SET @OLD_COLLATION_CONNECTION = @@COLLATION_CONNECTION */;\n")
    sql.write("/*!40101 SET NAMES utf8 */;\n")
    sql.write("/*!40103 SET @OLD_TIME_ZONE = @@TIME_ZONE */;\n")
    sql.write("/*!40103 SET TIME_ZONE = '+00:00' */;\n")
    sql.write("/*!40014 SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0 */;\n")
    sql.write("/*!40014 SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0 */;\n")
    sql.write("/*!40101 SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO' */;\n")
    sql.write("/*!40111 SET @OLD_SQL_NOTES = @@SQL_NOTES, SQL_NOTES = 0 */;\n")
    sql.write("\n")
    sql.write("--\n")
    sql.write("-- Table structure for table `Stock`\n")
    sql.write("--\n")
    sql.write("\n")

    '''
    =======================写入表Stock=======================
    '''
    print('写入表Stock')
    sql.write("SET NAMES utf8mb4;\n")
    sql.write("SET FOREIGN_KEY_CHECKS = 0;\n")
    sql.write("DROP TABLE IF EXISTS `Stock`;\n")
    sql.write("/*!40101 SET @saved_cs_client = @@character_set_client */;\n")
    sql.write("/*!40101 SET character_set_client = utf8 */;\n")
    sql.write("CREATE TABLE `Stock`\n")
    sql.write("(\n")
    sql.write("    `id`          int(11)      NOT NULL AUTO_INCREMENT,\n")
    sql.write("    `name`        varchar(255) DEFAULT NULL,\n")
    sql.write("    `quarter_p`   double       DEFAULT NULL,\n")
    sql.write("    `quarter_a`   double       DEFAULT NULL,\n")
    sql.write("    `halfYear_p`  double       DEFAULT NULL,\n")
    sql.write("    `halfYear_a`  double       DEFAULT NULL,\n")
    sql.write("    `year_p`      double       DEFAULT NULL,\n")
    sql.write("    `year_a`      double       DEFAULT NULL,\n")
    sql.write("    `guarantee_a` double       DEFAULT NULL,\n")
    sql.write("    PRIMARY KEY (`id`)\n")
    sql.write(") ENGINE = InnoDB\n")
    sql.write("  AUTO_INCREMENT = 1\n")
    sql.write("  DEFAULT CHARSET = utf8;\n")
    sql.write("/*!40101 SET character_set_client = @saved_cs_client */;\n")
    sql.write("\n")
    sql.write("--\n")
    sql.write("-- Dumping data for table `Stock`\n")
    sql.write("--\n")
    sql.write("BEGIN;\n")
    sql.write("/*!40000 ALTER TABLE `Stock` DISABLE KEYS */;\n")
    # example
    # sql.write("INSERT INTO Stock VALUES (1, 'stock1', 0, 1, 2, 3, 4, 5, 6);\n")
    # TODO: 季度、半年、一年
    for stock_id, stock_info in stock_data.items():
        sql.write("INSERT INTO Stock VALUES ({0}, '{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8});\n".format(
            stock_id,
            stock_info['name'],
            stock_info['quarter_p'],
            stock_info['quarter_a'],
            stock_info['halfYear_p'],
            stock_info['halfYear_a'],
            stock_info['year_p'],
            stock_info['year_a'],
            round(stock_info['guarantee_a'], 2)
        ))
    sql.write("/*!40000 ALTER TABLE `Stock` ENABLE KEYS */;\n")
    sql.write("COMMIT;\n")

    '''
    =======================写入表Event=======================
    '''
    print('写入表Event')
    sql.write("SET NAMES utf8mb4;\n")
    sql.write("SET FOREIGN_KEY_CHECKS = 0;\n")
    sql.write("DROP TABLE IF EXISTS `Event`;\n")
    sql.write("/*!40101 SET @saved_cs_client = @@character_set_client */;\n")
    sql.write("/*!40101 SET character_set_client = utf8 */;\n")
    sql.write("CREATE TABLE `Event`\n")
    sql.write("(\n")
    sql.write("    `id`          int(11)      NOT NULL AUTO_INCREMENT,\n")
    sql.write("    `stock_id`    int(11)      DEFAULT NULL,\n")
    sql.write("    `date`        varchar(255) DEFAULT NULL,\n")
    sql.write("    `type`        varchar(255) DEFAULT NULL,\n")
    sql.write("    PRIMARY KEY (`id`)\n")
    sql.write(") ENGINE = InnoDB\n")
    sql.write("  AUTO_INCREMENT = 1\n")
    sql.write("  DEFAULT CHARSET = utf8;\n")
    sql.write("/*!40101 SET character_set_client = @saved_cs_client */;\n")
    sql.write("\n")
    sql.write("--\n")
    sql.write("-- Dumping data for table `Event`\n")
    sql.write("--\n")
    sql.write("BEGIN;\n")
    sql.write("/*!40000 ALTER TABLE `Event` DISABLE KEYS */;\n")
    # example
    # sql.write("INSERT INTO Event VALUES (1, 000001, 2021-04-22, '发布公告');\n")
    with open('./resources/recent_pre.csv', 'r', encoding='utf-8') as recent_csv:
        next(recent_csv)
        recent_csv_reader = csv.reader(recent_csv)
        cur_id = 0
        for row in recent_csv_reader:
            if int(row[2].split('-')[0]) < 2018:
                continue
            cur_id += 1
            sql.write("INSERT INTO Event VALUES ({0}, {1}, '{2}', '{3}');\n".format(
                cur_id,
                row[0],
                row[2],
                row[3]
            ))
        guarantee_csv.close()
    sql.write("/*!40000 ALTER TABLE `Event` ENABLE KEYS */;\n")
    sql.write("COMMIT;\n")

    sql.close()

'''
写入sample.sql文件
'''
with open('../backend/sql/sample.sql', 'w', encoding='utf-8') as sql:
    '''
    =======================写入文件开头=======================
    '''
    print('写入文件开头')
    sql.write("-- MySQL dump 10.13  Distrib 5.7.19, for macos10.12 (x86_64)\n")
    sql.write("--\n")
    sql.write("-- Host: 127.0.0.1    Database: StockGraph\n")
    sql.write("-- ------------------------------------------------------\n")
    sql.write("-- Server version	5.7.19-log\n")
    sql.write("/*!40101 SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT */;\n")
    sql.write("/*!40101 SET @OLD_CHARACTER_SET_RESULTS = @@CHARACTER_SET_RESULTS */;\n")
    sql.write("/*!40101 SET @OLD_COLLATION_CONNECTION = @@COLLATION_CONNECTION */;\n")
    sql.write("/*!40101 SET NAMES utf8 */;\n")
    sql.write("/*!40103 SET @OLD_TIME_ZONE = @@TIME_ZONE */;\n")
    sql.write("/*!40103 SET TIME_ZONE = '+00:00' */;\n")
    sql.write("/*!40014 SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0 */;\n")
    sql.write("/*!40014 SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0 */;\n")
    sql.write("/*!40101 SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO' */;\n")
    sql.write("/*!40111 SET @OLD_SQL_NOTES = @@SQL_NOTES, SQL_NOTES = 0 */;\n")
    sql.write("\n")
    sql.write("--\n")
    sql.write("-- Table structure for table `Stock`\n")
    sql.write("--\n")
    sql.write("\n")

    '''
    =======================写入表Stock=======================
    '''
    print('写入表Stock')
    sql.write("SET NAMES utf8mb4;\n")
    sql.write("SET FOREIGN_KEY_CHECKS = 0;\n")
    sql.write("DROP TABLE IF EXISTS `Stock`;\n")
    sql.write("/*!40101 SET @saved_cs_client = @@character_set_client */;\n")
    sql.write("/*!40101 SET character_set_client = utf8 */;\n")
    sql.write("CREATE TABLE `Stock`\n")
    sql.write("(\n")
    sql.write("    `id`          int(11)      NOT NULL AUTO_INCREMENT,\n")
    sql.write("    `name`        varchar(255) DEFAULT NULL,\n")
    sql.write("    `quarter_p`   double       DEFAULT NULL,\n")
    sql.write("    `quarter_a`   double       DEFAULT NULL,\n")
    sql.write("    `halfYear_p`  double       DEFAULT NULL,\n")
    sql.write("    `halfYear_a`  double       DEFAULT NULL,\n")
    sql.write("    `year_p`      double       DEFAULT NULL,\n")
    sql.write("    `year_a`      double       DEFAULT NULL,\n")
    sql.write("    `guarantee_a` double       DEFAULT NULL,\n")
    sql.write("    PRIMARY KEY (`id`)\n")
    sql.write(") ENGINE = InnoDB\n")
    sql.write("  AUTO_INCREMENT = 1\n")
    sql.write("  DEFAULT CHARSET = utf8;\n")
    sql.write("/*!40101 SET character_set_client = @saved_cs_client */;\n")
    sql.write("\n")
    sql.write("--\n")
    sql.write("-- Dumping data for table `Stock`\n")
    sql.write("--\n")
    sql.write("BEGIN;\n")
    sql.write("/*!40000 ALTER TABLE `Stock` DISABLE KEYS */;\n")
    # example
    # sql.write("INSERT INTO Stock VALUES (1, 'stock1', 0, 1, 2, 3, 4, 5, 6);\n")
    # TODO: 季度、半年、一年
    for stock_id, stock_info in stock_data.items():
        if int(stock_id) <= 100:
            sql.write("INSERT INTO Stock VALUES ({0}, '{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8});\n".format(
                stock_id,
                stock_info['name'],
                stock_info['quarter_p'],
                stock_info['quarter_a'],
                stock_info['halfYear_p'],
                stock_info['halfYear_a'],
                stock_info['year_p'],
                stock_info['year_a'],
                round(stock_info['guarantee_a'], 2)
            ))
    sql.write("/*!40000 ALTER TABLE `Stock` ENABLE KEYS */;\n")
    sql.write("COMMIT;\n")

    '''
    =======================写入表Event=======================
    '''
    print('写入表Event')
    sql.write("SET NAMES utf8mb4;\n")
    sql.write("SET FOREIGN_KEY_CHECKS = 0;\n")
    sql.write("DROP TABLE IF EXISTS `Event`;\n")
    sql.write("/*!40101 SET @saved_cs_client = @@character_set_client */;\n")
    sql.write("/*!40101 SET character_set_client = utf8 */;\n")
    sql.write("CREATE TABLE `Event`\n")
    sql.write("(\n")
    sql.write("    `id`          int(11)      NOT NULL AUTO_INCREMENT,\n")
    sql.write("    `stock_id`    int(11)      DEFAULT NULL,\n")
    sql.write("    `date`        varchar(255) DEFAULT NULL,\n")
    sql.write("    `type`        varchar(255) DEFAULT NULL,\n")
    sql.write("    PRIMARY KEY (`id`)\n")
    sql.write(") ENGINE = InnoDB\n")
    sql.write("  AUTO_INCREMENT = 1\n")
    sql.write("  DEFAULT CHARSET = utf8;\n")
    sql.write("/*!40101 SET character_set_client = @saved_cs_client */;\n")
    sql.write("\n")
    sql.write("--\n")
    sql.write("-- Dumping data for table `Event`\n")
    sql.write("--\n")
    sql.write("BEGIN;\n")
    sql.write("/*!40000 ALTER TABLE `Event` DISABLE KEYS */;\n")
    # example
    # sql.write("INSERT INTO Event VALUES (1, 000001, 2021-04-22, '发布公告');\n")
    with open('./resources/recent_pre.csv', 'r', encoding='utf-8') as recent_csv:
        next(recent_csv)
        recent_csv_reader = csv.reader(recent_csv)
        cur_id = 0
        for row in recent_csv_reader:
            if int(row[0]) > 100 or int(row[2].split('-')[0]) < 2018:
                continue
            cur_id += 1
            sql.write("INSERT INTO Event VALUES ({0}, {1}, '{2}', '{3}');\n".format(
                cur_id,
                row[0],
                row[2],
                row[3]
            ))
        guarantee_csv.close()
    sql.write("/*!40000 ALTER TABLE `Event` ENABLE KEYS */;\n")
    sql.write("COMMIT;\n")

    sql.close()
