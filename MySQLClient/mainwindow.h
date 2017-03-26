#ifndef __MAINWINDOW_H__
#define __MAINWINDOW_H__

#include <Qt>
#include <QAbstractItemView>
#include <QAction>
#include <QApplication>
#include <QDebug>
#include <QFile>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QIcon>
#include <QLabel>
#include <QLineEdit>
#include <QWidget>
#include <QMessageBox>
#include <QPushButton>
#include <QTableWidget>
#include <QTableWidgetItem>
#include <QTextEdit>
#include <QTreeWidget>
#include <QTreeWidgetItem>
#include <QTreeWidgetItemIterator>
#include <QVBoxLayout>

#include "mysql/include/mysql_connection.h"
#include "mysql/include/cppconn/driver.h"
#include "mysql/include/cppconn/exception.h"
#include "mysql/include/cppconn/statement.h"
#include "mysql/include/cppconn/prepared_statement.h"
#include "mysql/include/cppconn/resultset.h"

#include "auxiliary_function.h"

class MainWindow : public QWidget {
    Q_OBJECT

public:
    MainWindow();
    ~MainWindow();

    void CreateMainWindow();
    void SetWidgets();

protected:
    QLineEdit * gHost;
    QLineEdit * gUsername;
    QLineEdit * gPassword;
    QLineEdit * gDB;
    QTextEdit * gLogger;

    QTreeWidget * gDatabaseTree;
    QTableWidget * gDatabaseTable;

    sql::Driver * driver;
    sql::Connection * conn;
    sql::Statement * statement;
    sql::PreparedStatement * prestatement;
    sql::ResultSet * result;

private slots:
    void SlotConnectToMySQL();
    void SlotDatabaseTreeItemClicked();
};

#endif // __MAINWINDOW_H__
