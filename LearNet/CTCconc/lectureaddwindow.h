#ifndef LECTUREADDWINDOW_H
#define LECTUREADDWINDOW_H

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
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

#include <QCloseEvent>
#include <QListWidget>
#include <QComboBox>
#include <QListWidget>
#include <QString>
#include <QMessageBox>
#include <QDialog>

namespace Ui {
class LectureAddWindow;
}

class LectureAddWindow : public QDialog
{
    Q_OBJECT

public:
    explicit LectureAddWindow(QWidget *parent = nullptr,int SD = 0);
    ~LectureAddWindow();
    int sd, sentText;
private slots:
    void on_DoneButton_clicked();

    void closeEvent (QCloseEvent *event);

private:
    Ui::LectureAddWindow *ui;
};

#endif // LECTUREADDWINDOW_H
