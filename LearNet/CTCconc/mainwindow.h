#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <cstring>
#include <pthread.h>
#include <arpa/inet.h>
#include <string.h>
#include <QDebug>
#include <arpa/inet.h>

#include <QMainWindow>
#include <testwindow.h>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    int sd;
    //char* msg = (char*) calloc(10000,1);
private slots:
    void on_pushButton_clicked();

    void on_LoginButton_clicked();

    void on_TestButton_clicked();

    void on_SignInButton_clicked();

private:
    Ui::MainWindow *ui;
    TestWindow* testwindow;
};

#endif // MAINWINDOW_H
