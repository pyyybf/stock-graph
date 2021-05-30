class SqlHelper:
    file_path = ''

    def __init__(self, file_path):
        self.file_path = file_path

    def write_init(self, database):
        with open(self.file_path, 'w', encoding='utf-8') as sql:
            sql.write("-- MySQL dump 10.13  Distrib 5.7.19, for macos10.12 (x86_64)\n")
            sql.write("--\n")
            sql.write("-- Host: 127.0.0.1    Database: {0}\n".format(database))
            sql.write("-- ------------------------------------------------------\n")
            sql.write("-- Server version	5.7.19-log\n")
            sql.write("\n")
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
            sql.write("DROP DATABASE IF EXISTS `{0}`;\n".format(database))
            sql.write("CREATE DATABASE {0};\n".format(database))
            sql.write("USE {0};\n".format(database))
            sql.write("\n")

            sql.close()

    def write_table(self, table, columns, primary_key, data):
        with open(self.file_path, 'a', encoding='utf-8') as sql:
            sql.write("--\n")
            sql.write("-- Table structure for table `{0}`\n".format(table))
            sql.write("--\n")
            sql.write("\n")
            sql.write("SET NAMES utf8mb4;\n")
            sql.write("SET FOREIGN_KEY_CHECKS = 0;\n")
            sql.write("DROP TABLE IF EXISTS `{0}`;\n".format(table))
            sql.write("/*!40101 SET @saved_cs_client = @@character_set_client */;\n")
            sql.write("/*!40101 SET character_set_client = utf8 */;\n")
            sql.write("CREATE TABLE `{0}`\n".format(table))
            sql.write("(\n")
            template = 'VALUES ('
            for column_key, column_attr in columns.items():
                sql.write("    `{0}` {1},\n".format(column_key, ' '.join(column_attr)))
                if column_attr[0].startswith('varchar'):
                    template = template + '\'{' + column_key + '}\', '
                else:
                    template = template + '{' + column_key + '}, '
            template = template[:len(template) - 2] + ');\n'
            sql.write("    PRIMARY KEY (`{0}`)\n".format(primary_key))
            sql.write(") ENGINE = InnoDB\n")
            sql.write("  AUTO_INCREMENT = 1\n")
            sql.write("  DEFAULT CHARSET = utf8;\n")
            sql.write("/*!40101 SET character_set_client = @saved_cs_client */;\n")
            sql.write("\n")

            sql.write("--\n")
            sql.write("-- Dumping data for table `{0}`\n".format(table))
            sql.write("--\n")
            sql.write("\n")
            sql.write("BEGIN;\n")
            sql.write("/*!40000 ALTER TABLE `{0}` ENABLE KEYS */;\n".format(table))
            for row in data:
                sql.write("INSERT INTO {0}\n".format(table))
                sql.write(template.format(**row))
            sql.write("/*!40000 ALTER TABLE `{0}` ENABLE KEYS */;\n".format(table))
            sql.write("COMMIT;\n")
            sql.write("\n")

            sql.close()
