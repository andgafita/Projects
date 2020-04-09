#include "mainwindow.h"
#include "ui_mainwindow.h"

using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{
}

void MainWindow::on_LoginButton_clicked()
{
    struct sockaddr_in server;
    unsigned short int port = 2024;

    char* LOGINMESSAGE = new char[10000];bzero(LOGINMESSAGE,10000);strcat(LOGINMESSAGE,"LOGIN");
    char* username = new char[10000];memset(username,'\0',10000);
    char* serverReply = new char[10000];memset(serverReply,'\0',10000);
    ::strcat(serverReply,"Logged in as user: ");

    char* serverReplyAdmin = new char[10000];memset(serverReplyAdmin,'\0',10000);
    ::strcat(serverReplyAdmin,"Logged in as admin: ");

    char* serverReplySuperAdmin = new char[10000];memset(serverReplySuperAdmin,'\0',10000);
    ::strcat(serverReplySuperAdmin,"Logged in as superadmin: ");

    sd = socket (AF_INET, SOCK_STREAM, 0);

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_port = htons (port);

    ::connect(this->sd, (struct sockaddr*)&server,sizeof(struct sockaddr));
    ::strcat(username,(ui->lineEdit->text()).toLatin1().data());
    ::strcat(serverReply,username);
    ::strcat(serverReply,"\n");
    ::strcat(serverReplyAdmin,username);
    ::strcat(serverReplyAdmin,"\n");
    ::strcat(serverReplySuperAdmin,username);
    ::strcat(serverReplySuperAdmin,"\n");

    if(strlen(username)<2){QMessageBox::information(this,"Login message","Invalid name!");return;}

    write(this->sd,LOGINMESSAGE,10000);
    write(this->sd,username,10000);
    bzero(username,10000);
    read(this->sd,username,10000);

    QMessageBox::information(this,"Login message",username);

    if(strcmp(username,serverReplySuperAdmin)==0){
    hide();
    testwindow = new TestWindow(this,sd,2);
    testwindow->show();
}
    else if(strcmp(username,serverReplyAdmin)==0){
    hide();
    testwindow = new TestWindow(this,sd,1);
    testwindow->show();
}
    else if(strcmp(username,serverReply)==0){
    hide();
    testwindow = new TestWindow(this,sd,0);
    testwindow->show();
}
    delete[] username;
    delete[] serverReply;
    delete[] LOGINMESSAGE;
}

void MainWindow::on_SignInButton_clicked()
{
    char* SIGNUPMESSAGE = new char[10000];bzero(SIGNUPMESSAGE,10000);strcat(SIGNUPMESSAGE,"SIGNUP");

    struct sockaddr_in server;
    unsigned short int port = 2024;

    char* username = new char[10000];memset(username,'\0',10000);
    sd = socket (AF_INET, SOCK_STREAM, 0);

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_port = htons (port);

    ::connect(this->sd, (struct sockaddr*)&server,sizeof(struct sockaddr));
    ::strcat(username,(ui->lineEdit_2->text()).toLatin1().data());
    if(strlen(username)<2){QMessageBox::information(this,"Sign up message","Invalid name!");return;}
    write(this->sd,SIGNUPMESSAGE,10000);
    write(this->sd,username,10000);
    read(this->sd,username,10000);

    QMessageBox::information(this,"Sign up message",username);

    delete[] username;
    delete[] SIGNUPMESSAGE;
}
