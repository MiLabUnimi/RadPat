#include "mainwindow.h"
#include <QApplication>

// Questa e` una modifica
// Seconda Modifica

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
