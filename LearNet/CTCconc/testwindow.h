#ifndef TESTWINDOW_H
#define TESTWINDOW_H

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

#include <QDialog>
#include <QListWidget>
#include <QComboBox>
#include <QListWidget>
#include <QString>
#include <QMessageBox>

namespace Ui {
class TestWindow;
}

class TestWindow : public QDialog
{
    Q_OBJECT

public:
    explicit TestWindow(QWidget *parent = nullptr,int Sd = 0,int isadmin = 0);
    static void *serverDbToTermnial(void* arg);
    int sd, noLectures, noFriends, o=0, inChat = 0;
    unsigned long th[1000];
    ~TestWindow();
private slots:
    void on_QuitButton_clicked();

    void on_comboBox_currentIndexChanged(int index);

    void on_comboBox_currentIndexChanged(const QString &arg1);

    void on_Friendbutton_clicked();

    void on_lineEdit_returnPressed();

    void on_friendsList_itemDoubleClicked(QListWidgetItem *item);

    void on_SendButton_clicked();

    void on_DeleteAccountButton_clicked();

    void on_JoinLectureChatButton_clicked();

    void on_DownloadButton_clicked();

    void on_LectureAddButton_clicked();

    void on_DeleteLectureButton_clicked();

    void on_MakeAdminButton_clicked();

    void on_RemoveAdminButton_clicked();
private:
    Ui::TestWindow *ui;
};

#endif // TESTWINDOW_H
