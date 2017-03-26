#include "mainwindow.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QFile f(":/qss/style.qss");
    if (f.open(QFile::ReadOnly | QFile::Text)) {
        QString styleSheet = QString(f.readAll());
        app.setStyleSheet(styleSheet);
    } else {
        qDebug() << "Can't open the file!";
    }
    f.close();

    MainWindow w;
    w.show();

    return app.exec();
}
