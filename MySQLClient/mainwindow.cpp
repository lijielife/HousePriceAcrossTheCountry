#include "mainwindow.h"

MainWindow::MainWindow() {
    CreateMainWindow();
}

MainWindow::~MainWindow() {
    delete result;
    delete statement;
    delete prestatement;
    delete conn;

    delete gHost;
    delete gUsername;
    delete gPassword;
    delete gDB;
    delete gLogger;

    delete gDatabaseTree;
    delete gDatabaseTable;
}

void MainWindow::CreateMainWindow() {
    setWindowTitle("MySQLClient");
    setWindowIcon(QIcon(":/staticfiles/mysql.ico"));

    setMinimumSize(1140, 585);
    setMaximumSize(1140, 585);

    SetWidgets();
}

void MainWindow::SetWidgets() {
    /*  */
    gHost = new QLineEdit;
    gHost->setText(tr("127.0.0.1"));
    gUsername = new QLineEdit;
    gUsername->setText(tr("root"));
    gPassword = new QLineEdit;
    gPassword->setEchoMode(QLineEdit::Password);
    gDB = new QLineEdit;
    QPushButton * okButton = new QPushButton;
    // okButton->setText(tr("Connect"));
    okButton->setIcon(QIcon(":/staticfiles/ui/handshake.png"));
    connect(okButton, SIGNAL(clicked()), this, SLOT(SlotConnectToMySQL()));

    QHBoxLayout * topLayout = new QHBoxLayout;
    topLayout->addSpacing(300);
    topLayout->addWidget(new QLabel(tr("host :")));
    topLayout->addWidget(gHost);
    topLayout->addSpacing(5);
    topLayout->addWidget(new QLabel(tr("username :")));
    topLayout->addWidget(gUsername);
    topLayout->addSpacing(5);
    topLayout->addWidget(new QLabel(tr("password :")));
    topLayout->addWidget(gPassword);
    topLayout->addSpacing(5);
    topLayout->addWidget(new QLabel(tr("database :")));
    topLayout->addWidget(gDB);
    topLayout->addSpacing(50);
    topLayout->addWidget(okButton);
    topLayout->addSpacing(10);

    /*  */
    gDatabaseTree = new QTreeWidget;
    gDatabaseTree->setHeaderHidden(true);
    connect(gDatabaseTree, SIGNAL(itemDoubleClicked(QTreeWidgetItem *, int)), this, SLOT(SlotDatabaseTreeItemClicked()));
    QHBoxLayout * leftLayout = new QHBoxLayout;
    leftLayout->addWidget(gDatabaseTree);

    /*  */
    gDatabaseTable = new QTableWidget(0, 0);
    gDatabaseTable->horizontalHeader()->setSectionResizeMode(QHeaderView::ResizeToContents);
    QHBoxLayout * rightLayout = new QHBoxLayout;
    rightLayout->addWidget(gDatabaseTable);

    /*  */
    QHBoxLayout * middleLayout = new QHBoxLayout;
    middleLayout->addLayout(leftLayout);
    middleLayout->addLayout(rightLayout);
    middleLayout->setStretchFactor(leftLayout, 1);
    middleLayout->setStretchFactor(rightLayout, 3);

    /*  */
    gLogger = new QTextEdit;
    gLogger->setEnabled(false);
    QHBoxLayout * bottomLayout = new QHBoxLayout;
    bottomLayout->addWidget(gLogger);

    /*  */
    QVBoxLayout * layout = new QVBoxLayout;
    layout->addLayout(topLayout);
    layout->addLayout(middleLayout);
    layout->addLayout(bottomLayout);
    layout->setStretchFactor(topLayout, 1);
    layout->setStretchFactor(middleLayout, 3);
    layout->setStretchFactor(bottomLayout, 1);

    this->setLayout(layout);
}

void MainWindow::SlotConnectToMySQL() {
    if (gHost->text() != "" && gUsername->text() != "" && gPassword->text() != "" && gDB->text() != "") {
        try {
            driver = get_driver_instance();
            conn = driver->connect(gHost->text().toStdString(), gUsername->text().toStdString(), gPassword->text().toStdString());
            conn->setSchema(gDB->text().toStdString());
            gLogger->append(">>  Connect to " + gDB->text() + "@" + gHost->text());
            QTreeWidgetItem * root = new QTreeWidgetItem;
            root->setText(0, gDB->text());
            gDatabaseTree->addTopLevelItem(root);

            prestatement = conn->prepareStatement("SHOW TABLES;");
            result = prestatement->executeQuery();
            result->last();
            int count = result->getRow();
            QVector<QTreeWidgetItem *> tableNameVector(count);
            result->beforeFirst();

            int i = 0;
            while (result->next()) {
                tableNameVector[i] = new QTreeWidgetItem;
                tableNameVector[i]->setText(0, QString::fromStdString(result->getString(1).asStdString()));
                root->addChild(tableNameVector[i]);
                i++;
            }

            gDatabaseTree->expandAll();
        } catch(sql::SQLException &e) {
            gLogger->append(tr(">>  MySQL error : ") + tr(e.what()));
            gLogger->append(tr(">>  MySQL state : ") + QString::fromStdString(e.getSQLState()));
        }
    } else {
        gLogger->append(tr(">>  username or password is null!"));
    }
}

void MainWindow::SlotDatabaseTreeItemClicked() {
    try {
        QTreeWidgetItem * selectedTable = gDatabaseTree->selectedItems()[0];

        gDatabaseTable->clearContents();

        prestatement = conn->prepareStatement("SELECT COUNT(*) totalCount FROM " + selectedTable->text(0).toStdString() + ";");
        result = prestatement->executeQuery();
        result->next();
        int rowTotal = result->getInt("totalCount");
        gDatabaseTable->setRowCount(rowTotal);

        prestatement = conn->prepareStatement("DESC " + selectedTable->text(0).toStdString() + ";");
        result = prestatement->executeQuery();
        int j = 0;
        QStringList columnNames;
        result->next();
        while (result->next()) {
            columnNames << QString::fromStdString(result->getString(1).asStdString());
            ++j;
        }
        int columnTotal = j;
        gDatabaseTable->setColumnCount(columnTotal);
        gDatabaseTable->setHorizontalHeaderLabels(columnNames);

        prestatement = conn->prepareStatement("SELECT * FROM " + selectedTable->text(0).toStdString() + ";");
        result = prestatement->executeQuery();
        QVector<QTableWidgetItem *> elementVector(rowTotal * columnTotal);

        int i = 0;
        while (result->next()) {
            for (j = 0; j < columnTotal; ++j) {
                elementVector[i * columnTotal + j] = new QTableWidgetItem(QString::fromStdString(result->getString(j + 2).asStdString()));
                gDatabaseTable->setItem(i, j, elementVector[i * columnTotal + j]);
            }
            i++;
        }
    } catch(sql::SQLException &e) {
        gLogger->append(tr(">>  MySQL error : ") + tr(e.what()));
        gLogger->append(tr(">>  MySQL state : ") + QString::fromStdString(e.getSQLState()));
    }
}
