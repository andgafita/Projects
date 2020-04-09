#include "testwindow.h"
#include "lectureaddwindow.h"
#include "ui_testwindow.h"

#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <QComboBox>
#include <QListWidget>
#include <QString>
#include <QMessageBox>

typedef struct thData{
  int idThread; //id-ul thread-ului tinut in evidenta de acest program
  int client; //descriptorul intors de accept
  int noFriends;
  char* chatdb; //pentru thread-urile care ajuta la realizarea unui chat
  Ui::TestWindow *ui;
}thData;

void* TestWindow::serverDbToTermnial(void* arg){
    struct thData tdL;
    tdL= *((struct thData*)arg);
    char* Response = new char[10000];
    char* testResponseChat = new char[10000];
    char* testResponseFriends = new char[10000];

    while(true){
      //qDebug("WE HAVE LIFTOFF");
      bzero(Response,10000);
      bzero(testResponseChat,10000);
      bzero(testResponseFriends,10000);
      read(tdL.client,Response,10000);
      strncpy(testResponseChat,Response,14);
      strncpy(testResponseFriends,Response,21);

      if(strcmp(Response,"WAITSIGNAL")==0){usleep(1000000);continue;}
      if(strcmp(testResponseChat,"<CHAT_MESSAGE>")!=0 && strcmp(testResponseFriends,"<FRIENDS_LIST_UPDATE>")!=0 && strcmp(Response,"")!=0){
          qDebug(" **%s**",Response);
          bzero(testResponseChat,10000);
          strcat(testResponseChat,"REPEAT");
          write(tdL.client,testResponseChat,10000);
          write(tdL.client,Response,10000);
          usleep(200000);
          continue;
      }

      if(strcmp(testResponseChat,"<CHAT_MESSAGE>")==0){
        bzero(testResponseChat,10000);
        strcpy(testResponseChat,Response+14);
        tdL.ui->textBrowser_2->append(QString::fromLocal8Bit(testResponseChat));
        tdL.ui->textBrowser_2->ensureCursorVisible();
        }
        else if(strcmp(testResponseFriends,"<FRIENDS_LIST_UPDATE>")==0){
          qDebug("am intrat pe friends in thread!");
          bzero(testResponseFriends,10000);
          strcpy(testResponseFriends,Response+21);

          tdL.ui->friendsList->addItem(QString::fromLocal8Bit(testResponseFriends));
          tdL.noFriends++;
      }
      //printf("%s",Response);fflush(stdout);
    }

    pthread_detach(pthread_self());
    //close((intptr_t)arg);
    return(nullptr);
  }











TestWindow::TestWindow(QWidget *parent, int Sd,int isadmin) :
    QDialog(parent),
    ui(new Ui::TestWindow)
{
    sd = Sd;

    char* msg = new char[10000];bzero(msg,10000);
    char* user = new char[10000];bzero(user,10000);

    strcat(msg,"initLectures");
    write(sd,msg,10000);
    read(sd,&noLectures,4);
    //QString* item;

    ui->setupUi(this);

    if(isadmin==0){
        this->ui->lineEdit_2->hide();
        this->ui->DeleteLectureButton->hide();
        this->ui->LectureAddButton->hide();
        this->ui->MakeAdminButton->hide();
        this->ui->RemoveAdminButton->hide();
    }
    else if (isadmin == 2){
        this->ui->DeleteAccountButton->hide();
    }

    for(int i = 1;i <= noLectures;i++){
        bzero(msg,10000);
        read(sd,msg,10000);
        //item = fromLocal8Bit(msg);
        //qDebug("%i**%s**\n",noLectures,msg);qDebug() << "--" << QString::fromLocal8Bit(msg) << "--";
        if(strcmp(msg,"")!=0)ui->comboBox->addItem(QString::fromLocal8Bit(msg));
        write(sd,msg,10000);
    }
    noLectures = ui->comboBox->count();
    char* firstLecture = new char[10000];bzero(firstLecture,10000);
    strcat(firstLecture,"showLecture ");
    strcat(firstLecture,ui->comboBox->currentText().toLocal8Bit());
    write(sd,firstLecture,10000);

    bzero(firstLecture,10000);
    read(sd,firstLecture,10000);
    ui->textBrowser->setText(QString::fromLocal8Bit(firstLecture));

    delete[] firstLecture;

    bzero(msg,10000);
    strcat(msg,"getFriendList");
    write(sd,msg,10000);
    read(sd,&noFriends,4);
    qDebug("FRIENDZ: %i\n",noFriends);

    for(int i = 1;i <= noFriends;i++){
        bzero(msg,10000);
        read(sd,msg,10000);
        if(i == 1)strcat(user,msg);
        qDebug("FRIEND FRIEND %s\n",msg);
        ui->friendsList->addItem(QString::fromLocal8Bit(msg));
        write(sd,msg,10000);
    }

    inChat = 1;
    char* chatCommand = new char[10000];bzero(chatCommand,10000);

    strcat(chatCommand,"chat ");
    strcat(chatCommand,user);

    write(sd,chatCommand,10000);

    bzero(chatCommand,10000);
    read(sd,chatCommand,10000);

    ui->textBrowser_2->clear();
    ui->textBrowser_2->append(QString::fromLocal8Bit(chatCommand));

    thData * td;

    td=(struct thData*)malloc(sizeof(struct thData));
    td->idThread=o++;
    td->noFriends=noFriends;
    td->client=sd;
    td->ui=ui;

    pthread_create(&th[o], NULL, &TestWindow::serverDbToTermnial, td);
}

TestWindow::~TestWindow()
{
    char test[10000];memset(test,'\0',10000);
    ::strcat(test,"quit");

    write(this->sd,test,10000);

    delete ui;
}

void TestWindow::on_QuitButton_clicked()
{
    //qDebug("TEST BUTTON");
    char test[10000];memset(test,'\0',10000);
    ::strcat(test,"quit");

    write(this->sd,test,10000);
    QCoreApplication::quit();
    //qDebug("aici e test%s\n",test);
}

void TestWindow::on_comboBox_currentIndexChanged(const QString &arg1)
{
    qDebug("lecture index updated!\n");
    if(ui->comboBox->count() < noLectures || ui->friendsList->count() < noFriends)return;
    qDebug("lecture index updated!\n");
    qDebug("SDSAFDSAFDSAF");qDebug() << ui->comboBox->count();
    char* msg = new char[10000];bzero(msg,10000);
    strcat(msg,"showLecture ");
    strcat(msg,(arg1.toLocal8Bit()));
    write(sd,msg,10000);

    bzero(msg,10000);
    read(sd,msg,10000);
    qDebug() << QString::fromLocal8Bit(msg);
    ui->textBrowser->setText(QString::fromLocal8Bit(msg));

    delete[] msg;
}

void TestWindow::on_Friendbutton_clicked()
{   qDebug("Friend button clicked!\n");
    char* msg = new char[10000];bzero(msg,10000);
    char* friendName = new char[10000];bzero(friendName,10000);strcat(friendName,(ui->AddFriendName->text()).toLatin1().data());
    strcat(msg,"friend ");strcat(msg,friendName);

    if(strlen(this->ui->AddFriendName->text().toLocal8Bit())<2){
        QMessageBox::information(this,"Friend request","Invalid name!");
        return;
    }

    char* replyComp = new char[10000];bzero(replyComp,10000);
    strcat(replyComp,"Felicitari! Te-ai imprietenit cu ");
    strcat(replyComp,friendName);
    strcat(replyComp,"!");

    char* otherReplyComp = new char[10000];bzero(otherReplyComp,10000);
    strcat(otherReplyComp,"Userul pe care l-ati inserat nu exista!");

    char* yetAnotherReplyComp = new char[10000];bzero(yetAnotherReplyComp,10000);
    strcat(yetAnotherReplyComp,"Sunteti prieteni deja!");

    write(sd,msg,10000);
    bzero(msg,10000);
    read(sd,msg,10000);

    char* testResponseChat = new char[10000];
    char* testResponseFriends = new char[10000];

    while(strcmp(msg,replyComp)!=0 && strcmp(msg,otherReplyComp)!=0 && strcmp(msg,yetAnotherReplyComp)!=0){
        bzero(testResponseChat,10000);
        bzero(testResponseFriends,10000);
        strncpy(testResponseChat,msg,14);
        strncpy(testResponseFriends,msg,21);
        qDebug("MESAJ GRESIT **%s**\n",msg);

    if((strcmp(testResponseChat,"<CHAT_MESSAGE>")==0 || strcmp(testResponseFriends,"<FRIENDS_LIST_UPDATE>")==0) && strcmp(msg,"")!=0){
        bzero(testResponseChat,10000);
        strcat(testResponseChat,"REPEAT");
        write(sd,testResponseChat,10000);
        write(sd,msg,10000);
        bzero(msg,10000);
        read(sd,msg,10000);
        usleep(100000);
        qDebug("MESAJ RETRIMIS **%s**\n",msg);
    }
}
    QMessageBox::information(this,"Friend request",QString::fromLocal8Bit(msg));

    //if(strcmp(msg,replyComp)==0){
    //    ui->friendsList->addItem(QString::fromLocal8Bit(friendName));
    //    noFriends++;
    //}

    delete[] msg;
    delete[] friendName;
    delete[] replyComp;
}

void TestWindow::on_lineEdit_returnPressed()
{
    if(inChat==0)return;

    char* msg = new char[10000];bzero(msg,10000);
    char* lineEditContent = new char[10000];bzero(lineEditContent,10000);

    strcat(msg,"<CHAT>");

    strcat(lineEditContent,(ui->lineEdit->text()).toLatin1().data());

    ui->lineEdit->clear();

    if(strcmp(lineEditContent,"")!=0){
    write(sd,msg,10000);
    write(sd,lineEditContent,10000);
    }
}

void TestWindow::on_SendButton_clicked(){
    if(inChat==0)return;

    char* msg = new char[10000];bzero(msg,10000);
    char* lineEditContent = new char[10000];bzero(lineEditContent,10000);

    strcat(msg,"<CHAT>");

    strcat(lineEditContent,(ui->lineEdit->text()).toLatin1().data());

    ui->lineEdit->clear();

    if(strcmp(lineEditContent,"")!=0){
    write(sd,msg,10000);
    write(sd,lineEditContent,10000);
    }
}

void TestWindow::on_friendsList_itemDoubleClicked(QListWidgetItem *item)
{
    inChat = 1;
    char* itemText = new char [10000];bzero(itemText,10000);
    char* chatCommand = new char[10000];bzero(chatCommand,10000);
    QString QitemText = item->text();
    qDebug() << QitemText;

    strcat(itemText,QitemText.toLocal8Bit());

    strcat(chatCommand,"chat ");
    strcat(chatCommand,itemText);

    write(sd,chatCommand,10000);

    bzero(chatCommand,10000);
    read(sd,chatCommand,10000);
    if(strcmp(chatCommand,"User does not exist!")==0)return;
    ui->textBrowser_2->clear();
    ui->textBrowser_2->append(QString::fromLocal8Bit(chatCommand));
}

void TestWindow::on_DeleteAccountButton_clicked(){
    char* deleteAccountMessage = new char[10000];bzero(deleteAccountMessage,10000);
    strcat(deleteAccountMessage,"DELETE_ACCOUNT");

    QMessageBox::StandardButton reply = QMessageBox::question(this,"Account deletion","Are you sure?", QMessageBox::Yes | QMessageBox::No);

    if(reply == QMessageBox::Yes){
        write(sd,deleteAccountMessage,10000);
        QCoreApplication::quit();
    }
    else return;
}

void TestWindow::on_JoinLectureChatButton_clicked(){
    inChat = 1;
    if(strcmp(ui->textBrowser->toPlainText().toLocal8Bit(),"Documentul nu exista!\n")==0)return;
    if(strcmp((ui->comboBox->currentText()).toLocal8Bit(),"")==0)return;
    char* lectureName = new char [10000];bzero(lectureName,10000);
    char* chatCommand = new char[10000];bzero(chatCommand,10000);
    strcat(lectureName,(ui->comboBox->currentText()).toLocal8Bit());

    strcat(chatCommand,"chatlecture ");
    strcat(chatCommand,lectureName);

    write(sd,chatCommand,10000);

    bzero(chatCommand,10000);
    read(sd,chatCommand,10000);

    ui->textBrowser_2->clear();
    ui->textBrowser_2->append(QString::fromLocal8Bit(chatCommand));
}


void TestWindow::on_DownloadButton_clicked(){
    qDebug("lecture index updated!\n");
    if(ui->comboBox->count() < noLectures || ui->friendsList->count() < noFriends)return;
    qDebug("lecture index updated!\n");
    qDebug("SDSAFDSAFDSAF");qDebug() << ui->comboBox->count();
    char* msg = new char[10000];bzero(msg,10000);
    char* lectureName = new char[10000];bzero(lectureName,10000);
    strcat(lectureName,(this->ui->comboBox->currentText()).toLocal8Bit());
    strcat(msg,"showLecture ");
    strcat(msg,lectureName);

    write(sd,msg,10000);
    bzero(msg,10000);
    read(sd,msg,10000);

    int file = ::open(lectureName,O_WRONLY | O_CREAT);
    chmod(lectureName,0777);

    qDebug("%s\n",lectureName);
    strcat(lectureName,"\n\n");
    write(file,lectureName,strlen(lectureName));
    write(file,msg,strlen(msg));
    delete[] lectureName;
    delete[] msg;
}

void TestWindow::on_LectureAddButton_clicked(){
    char* msg = new char[10000];bzero(msg,10000);
    char* test = new char[10000];bzero(test,10000);
    strcat(msg,"lectureAdd ");
    strcat(msg,this->ui->lineEdit_2->text().toLocal8Bit());

    if(strlen(this->ui->lineEdit_2->text().toLocal8Bit())<2){
        QMessageBox::information(this,"Add lecture message","Invalid name!");
        return;
    }

    this->ui->lineEdit_2->clear();

    write(sd,msg,10000);

    LectureAddWindow* lectureaddwindow = new LectureAddWindow(this,sd);
    lectureaddwindow->setModal(true);
    lectureaddwindow->exec();
    qDebug("does this print?\n");
    bzero(msg,10000);
    read(sd,msg,10000);
    QMessageBox::information(this,"Lecture add message",msg);
}

void TestWindow::on_DeleteLectureButton_clicked(){
    char* msg = new char[10000];bzero(msg,10000);
    char* test = new char[10000];bzero(test,10000);
    strcat(msg,"lectureDelete ");
    strcat(msg,this->ui->lineEdit_2->text().toLocal8Bit());

    if(strlen(this->ui->lineEdit_2->text().toLocal8Bit())<2){
        QMessageBox::information(this,"Delete lecture message","Invalid name!");
        return;
    }

    this->ui->lineEdit_2->clear();

    write(sd,msg,10000);

    bzero(msg,10000);
    read(sd,msg,10000);
    QMessageBox::information(this,"Lecture add message",QString::fromLocal8Bit(msg));
    qDebug("does this print?\n");
}

void TestWindow::on_MakeAdminButton_clicked(){
    char* msg = new char[10000];bzero(msg,10000);
    strcat(msg,"makeadmin ");
    strcat(msg,this->ui->lineEdit_2->text().toLocal8Bit());

    if(strlen(this->ui->lineEdit_2->text().toLocal8Bit())<2){
        QMessageBox::information(this,"Make admin message","Invalid name!");
        return;
    }

    this->ui->lineEdit_2->clear();

    write(sd,msg,10000);

    bzero(msg,10000);
    read(sd,msg,10000);
    QMessageBox::information(this,"Make admin message",msg);
}

void TestWindow::on_RemoveAdminButton_clicked(){
    char* msg = new char[10000];bzero(msg,10000);
    strcat(msg,"removeadmin ");
    strcat(msg,this->ui->lineEdit_2->text().toLocal8Bit());

    if(strlen(this->ui->lineEdit_2->text().toLocal8Bit())<2 || strcmp((this->ui->lineEdit_2->text().toLocal8Bit()),"admin")==0){
        QMessageBox::information(this,"Remove admin message","Invalid name!");
        return;
    }

    this->ui->lineEdit_2->clear();

    write(sd,msg,10000);

    bzero(msg,10000);
    read(sd,msg,10000);
    QMessageBox::information(this,"Remove admin message",msg);
}






