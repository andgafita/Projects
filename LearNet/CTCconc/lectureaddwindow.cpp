#include "lectureaddwindow.h"
#include "ui_lectureaddwindow.h"
#include <QCloseEvent>

LectureAddWindow::LectureAddWindow(QWidget *parent, int SD) :
    QDialog(parent),
    ui(new Ui::LectureAddWindow)
{
    sd = SD;
    sentText = 0;
    ui->setupUi(this);
}

LectureAddWindow::~LectureAddWindow()
{
    delete ui;
    this->accept();
    close();

}

void LectureAddWindow::on_DoneButton_clicked()
{
    char* lectureText = new char[10000];bzero(lectureText,10000);

    strcat(lectureText,ui->textEdit->toPlainText().toLocal8Bit());
    sentText=1;
    write(sd,lectureText,10000);
    qDebug("**%s**",lectureText);
    delete[] lectureText;
    this->accept();
    close();
    LectureAddWindow::done(true);
    qDebug("closed");
}

void LectureAddWindow::closeEvent (QCloseEvent *event)
{
    if(sentText==0){
        char* lectureText = new char[10000];bzero(lectureText,10000);
        strcat(lectureText,"CANCEL_LECTURE");

        write(sd,lectureText,10000);
    }
    this->accept();
    delete ui;
    close();
}
