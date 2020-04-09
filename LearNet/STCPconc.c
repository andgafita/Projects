/* servTCPIt.c - Exemplu de server TCP iterativ
   Asteapta un nume de la clienti; intoarce clientului sirul
   "Hello nume".
   
   Autor: Lenuta Alboaie  <adria@infoiasi.ro> (c)2009
*/

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <ctype.h>
#include <errno.h>
#include <pwd.h>
#include <sys/wait.h>
#include <math.h>
#include <dirent.h>
#include <time.h>
#include <pthread.h>
#include <sqlite3.h>
#define true 1
#define PORT 2024

/* codul de eroare returnat de anumite apeluri */
extern int errno;
int j;

typedef struct thData{
  int idThread; //id-ul thread-ului tinut in evidenta de acest program
  int client; //descriptorul intors de accept
  char* chatdb; //pentru thread-urile care ajuta la realizarea unui chat
  char* from; //la fel ca la chatdb, tine minte utilizatorul thread-ului
}thData;

static int callback(char* data, int argc, char** argv, char** azColName);
static void *treat(void *); /* functia executata de fiecare thread ce realizeaza comunicarea cu clientii */
static void *chatDBtoClient(void * arg);
char* itoa(int x);
char* subString(char* sourceString,int nrCuv);
void loginClient(char* Response,char* msg,char* user,int client,int* login, int* admin);
void showLecture(char* Response,char* msg);
void lectureAdd(char* Response, char* msg, int client);
void lectureDelete(char* Response, char* msg, int client);
int testIfUserExists(char* name);
void friend(char* Response, char* msg,char* user);
char* friendDBname(char* user,char*msg);
int getLastmsgno(char* table);
char* sqlInsert(char* user,char* table, char* msg);
int testIfFriends(char* msg, char* user);
void initLectures(int client);
void getFriendList(char* user, int client);
void signUp(char* Response,char* msg,int client);
void deleteAccount(char* user);
int getFriendsNo(char* user);
void makeadmin(char* username,char* Response);
void removeadmin(char* username,char* Response);
int testIfLectureExists(char* name);

int main ()
{
  struct sockaddr_in server;  // structura folosita de server
  struct sockaddr_in from;  
  char msg[10000];    //mesajul primit de la client 
  char Response[10000];        //mesaj de raspuns pentru client
  int sd;     //descriptorul de socket 
  int optval = 1,i=0;
  pthread_t th[100];    //Identificatorii thread-urilor care se vor crea
  

  setsockopt(sd,SOL_SOCKET, SO_REUSEADDR,&optval,sizeof(optval));

  /* crearea unui socket */
  if ((sd = socket (AF_INET, SOCK_STREAM, 0)) == -1)
    {
      perror ("[server]Eroare la socket().\n");
      return errno;
    }

  /* pregatirea structurilor de date */
  bzero (&server, sizeof (server));
  bzero (&from, sizeof (from));
  
  /* umplem structura folosita de server */
  /* stabilirea familiei de socket-uri */
    server.sin_family = AF_INET;  
  /* acceptam orice adresa */
    server.sin_addr.s_addr = htonl (INADDR_ANY);
  /* utilizam un port utilizator */
    server.sin_port = htons (PORT);
  
  /* atasam socketul */
  if (bind (sd, (struct sockaddr *) &server, sizeof (struct sockaddr)) == -1)
    {
      perror ("[server]Eroare la bind().\n");
      return errno;
    }

  /* punem serverul sa asculte daca vin clienti sa se conecteze */
  if (listen (sd, 5) == -1)
    {
      perror ("[server]Eroare la listen().\n");
      return errno;
    }
printf ("[server]Asteptam la portul %d...\n",PORT);
  /* servim in mod iterativ clientii... */















  while (1)
    {
      int client;
      int length = sizeof (from);
      thData * td;
      
      fflush (stdout);

      client = accept (sd, (struct sockaddr *) &from, &length);/* acceptam un client (stare blocanta pina la realizarea conexiunii) */
      if (client < 0)      /* eroare la acceptarea conexiunii de la un client */
  {
    perror ("[server]Eroare la accept().\n");
    continue;
  }
      

  td=(struct thData*)malloc(sizeof(struct thData)); 
  td->idThread=i++;
  td->client=client;
  td->chatdb="";
  td->from="";

  pthread_create(&th[i], NULL, &treat, td); 
  //close (client);
  //while(waitpid(-1,NULL,WNOHANG));

    }       /* while */
}       /* main */
















static void *treat(void * arg)
{   
  struct thData tdL; 
  tdL= *((struct thData*)arg);
  sqlite3* DB;

  int filedesc, inChat = 0;
  char msg[10000];    //mesajul primit de la client 
  char Response[10000];
  pthread_t lastThread;
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(10000,1);
  char* table = (char*) calloc(100,1);
  char* messageError;
  int lastmsgno,i=0;
  

  sqlite3_open("LearNet.db", &DB); 

    bzero (msg, 10000);
        printf ("[server]Asteptam mesajul...\n");
        fflush (stdout);

        int login = 0, admin = 0;
        char x;
        char* user = (char*) calloc(10000,1);

        bzero(msg,10000);
        read(tdL.client, msg, 10000);
        printf("****%s****\n",msg);
        bzero(Response,10000);
        strcat(Response,"Error! User does not exist!\n");
        strcat(Response,msg);

        if(strcmp(msg,"SIGNUP")==0){printf("EXECUTED SIGNUP\n");signUp(Response,msg,tdL.client);}
          else loginClient(Response,msg,user,tdL.client,&login,&admin);
        if(login == 0){
                      sqlite3_close(DB);
                      write (tdL.client, Response, 10000);close(tdL.client);pthread_detach(pthread_self());
                      close ((intptr_t)arg);
                      return(NULL);}


        while(true){
          bzero(msg,10000);
          read(tdL.client, msg, 10000);
          printf("AM PRIMIT MESAJUL **%s**\n",msg);
          bzero(Response,10000);
          if(strcmp(msg,"REPEAT")==0 && strcmp(msg,"")!=0){
            read(tdL.client,Response,10000);
            printf("Retrimitem mesajul \"%s\" la clientul : %s!\n",Response,user);
            write (tdL.client, Response, 10000);
            continue;
          }
          if(strcmp(subString(msg,1),"quit")==0){
            bzero(sql,10000);
            strcat(sql,"INSERT INTO ");strcat(sql,table);strcat(sql," VALUES ( 0, '0', '0' );");
            sqlite3_exec(DB, sql, callback, query, &messageError);

            printf("Am inchis conexiunea cu %s!\n",user);
            bzero(sql,10000);
            strcat(sql,"UPDATE users SET isonline = 0 WHERE username = '");
            strcat(sql,user);
            strcat(sql,"';");

            sqlite3_exec(DB, sql, callback, query, &messageError);  
            sqlite3_close(DB);close(tdL.client);pthread_detach(pthread_self());
            close ((intptr_t)arg);
            return(NULL); 
            }
            else 
              if(strcmp(subString(msg,1),"lectureAdd")==0 && admin == 1)lectureAdd(Response,msg,tdL.client);
                else 
                  if((strcmp(subString(msg,1),"lectureAdd")==0 || strcmp(subString(msg,1),"lectureDelete") == 0) && admin == 0)strcat(Response,"You don't have admin privileges!");
                    else
                      if(strcmp(subString(msg,1),"lectureDelete") == 0)lectureDelete(Response, msg, tdL.client);
                        else 
                          if(strcmp(subString(msg,1),"showLecture")==0)showLecture(Response,msg);                      
                          else
                            if(strcmp(subString(msg,1),"friend")==0)friend(Response,msg,user);
                              else 
                                if(strcmp(subString(msg,1),"initLectures")==0){initLectures(tdL.client);continue;}
                                  else 
                                    if(strcmp(subString(msg,1),"getFriendList")==0){getFriendList(user, tdL.client);continue;}  
                                      else
                                        if(strcmp(subString(msg,1),"chat")==0 && inChat == 0){
                                          inChat=1;
                                          table = friendDBname(user,msg);

                                          bzero(sql,10000);bzero(query,10000);
                                          strcat(sql,"SELECT * FROM ");strcat(sql,table);strcat(sql,";");
                                          sqlite3_exec(DB, sql, callback, query, &messageError);

                                          if(strcmp(query,"")==0)continue;
  										  lastmsgno = getLastmsgno(table);
  										  bzero(Response,10000);
                                          for(int k = 1; k<=lastmsgno;k++){
											bzero(sql,10000);
											bzero(query,10000);
											strcat(sql,"SELECT sender, msg FROM ");strcat(sql,table);strcat(sql," WHERE msgno = ");strcat(sql,itoa(k));
											strcat(sql,";");

											sqlite3_exec(DB, sql, callback, query, &messageError); 

											printf("%s\n",query);
											strcat(Response,query);
											strcat(Response,"\n");
											}
                                          thData * td;

                                          td=(struct thData*)malloc(sizeof(struct thData)); 
                                          td->idThread=i++;
                                          td->client=tdL.client;
                                          td->chatdb=table;
                                          td->from=user;

                                          pthread_create(&lastThread, NULL, &chatDBtoClient, td); 

                                            
                                          }
                                          else 
                                            if(strcmp(subString(msg,1),"chat")==0 && inChat == 1){
                                              if(testIfUserExists(subString(msg,2))==0){bzero(Response,10000);strcat(Response,"User does not exist!");}
                                              else{
                                              bzero(sql,10000);
                                              strcat(sql,"UPDATE users SET terminate_chat = 1 WHERE username = '");strcat(sql,user);strcat(sql,"';");
                                              sqlite3_exec(DB, sql, callback, query, &messageError);
                                              pthread_join(lastThread,NULL);
                                              table = friendDBname(user,msg);
                                              lastmsgno = getLastmsgno(table);

                                              bzero(sql,10000);bzero(query,10000);
                                              strcat(sql,"SELECT * FROM ");strcat(sql,table);strcat(sql,";");
                                              sqlite3_exec(DB, sql, callback, query, &messageError);
                                              printf("\n\nLA CHANGE CHAT %s \n %s\n\n\n",table,query);
                                              if(strcmp(query,"")==0){printf("ALTCEVA ALTCEVA\n");continue;}
											  bzero(Response,10000);
                                              for(int k = 1; k<=lastmsgno;k++){
																    bzero(sql,10000);
																    bzero(query,10000);
																    strcat(sql,"SELECT sender, msg FROM ");strcat(sql,table);strcat(sql," WHERE msgno = ");strcat(sql,itoa(k));
																    strcat(sql,";");

																    sqlite3_exec(DB, sql, callback, query, &messageError); 

																    printf("%s\n",query);
																    strcat(Response,query);
																    strcat(Response,"\n");
																    }


                                              thData * td;

                                              td=(struct thData*)malloc(sizeof(struct thData)); 
                                              td->idThread=i++;
                                              td->client=tdL.client;
                                              td->chatdb=table;
                                              td->from=user;

                                              pthread_create(&lastThread, NULL, &chatDBtoClient, td); 
                                              }
                                              }
                                              else
                                                if(strcmp(msg,"<CHAT>")==0 && inChat == 1){
                                                  bzero(msg,10000);
                                                  read(tdL.client,msg,10000);
                                                  printf("Read message: %s\n",msg);

                                                  bzero(sql,10000);
                                                  sql = sqlInsert(user,table,msg);
                                                  sqlite3_exec(DB, sql, callback, query, &messageError);

                                                  continue;
                                                  }
                                                  else
                                                    if(strcmp(subString(msg,1),"DELETE_ACCOUNT")==0){
                                                      bzero(sql,10000);
                                                      strcat(sql,"UPDATE users SET terminate_chat = 1 WHERE username = '");strcat(sql,user);strcat(sql,"';");
                                                      sqlite3_exec(DB, sql, callback, query, &messageError);
                                                      printf("DELETE : *%s*\n",sql);

                                                      pthread_join(lastThread,NULL);
                                                      deleteAccount(user);

                                                      sqlite3_close(DB);close(tdL.client);pthread_detach(pthread_self());
                                                      close ((intptr_t)arg);
                                                      return(NULL);
                                                      }
                                                      else
                                                        if(strcmp(subString(msg,1),"chatlecture")==0 && inChat == 0){
                                                          inChat=1;
                                                          table = subString(msg,2);
                                                          lastmsgno = getLastmsgno(table);
                                                          bzero(sql,10000);bzero(query,10000);
                                                          strcat(sql,"SELECT * FROM ");strcat(sql,table);strcat(sql,";");
                                                          sqlite3_exec(DB, sql, callback, query, &messageError);

                                                          if(strcmp(query,"")==0)continue;
                                                          bzero(Response,10000);
                                                          for(int k = 1; k<=lastmsgno;k++){
																    bzero(sql,10000);
																    bzero(query,10000);
																    strcat(sql,"SELECT sender, msg FROM ");strcat(sql,table);strcat(sql," WHERE msgno = ");strcat(sql,itoa(k));
																    strcat(sql,";");

																    sqlite3_exec(DB, sql, callback, query, &messageError); 

																    printf("%s\n",query);
																    strcat(Response,query);
																    strcat(Response,"\n");
																    }
                                                          thData * td;

                                                          td=(struct thData*)malloc(sizeof(struct thData)); 
                                                          td->idThread=i++;
                                                          td->client=tdL.client;
                                                          td->chatdb=table;
                                                          td->from=user;

                                                          pthread_create(&lastThread, NULL, &chatDBtoClient, td); 
                                                          
                                                            
                                                          }
                                                          else 
                                                            if(strcmp(subString(msg,1),"chatlecture")==0 && inChat == 1){
                                                              bzero(sql,10000);
                                                              strcat(sql,"UPDATE users SET terminate_chat = 1 WHERE username = '");strcat(sql,user);strcat(sql,"';");
                                                              sqlite3_exec(DB, sql, callback, query, &messageError);
                                                              pthread_join(lastThread,NULL);

                                                              table = subString(msg,2);
                                                              lastmsgno = getLastmsgno(table);
                                                              bzero(sql,10000);bzero(query,10000);
                                                              strcat(sql,"SELECT * FROM ");strcat(sql,table);strcat(sql,";");
                                                              sqlite3_exec(DB, sql, callback, query, &messageError);

                                                              if(strcmp(query,"")==0)continue;
																lastmsgno = getLastmsgno(table);
																  printf("%i  %s\n",lastmsgno,table);
																  bzero(Response,10000);
																  for(int k = 1; k<=lastmsgno;k++){
																    bzero(sql,10000);
																    bzero(query,10000);
																    strcat(sql,"SELECT sender, msg FROM ");strcat(sql,table);strcat(sql," WHERE msgno = ");strcat(sql,itoa(k));
																    strcat(sql,";");

																    sqlite3_exec(DB, sql, callback, query, &messageError); 
																    
																    printf("%s\n",query);
																    strcat(Response,query);
																    strcat(Response,"\n");
																    }
                                                              thData * td;

                                                              td=(struct thData*)malloc(sizeof(struct thData)); 
                                                              td->idThread=i++;
                                                              td->client=tdL.client;
                                                              td->chatdb=table;
                                                              td->from=user;

                                                              pthread_create(&lastThread, NULL, &chatDBtoClient, td); 
                                                              }
                                                              else
                                                              	if(strcmp(subString(msg,1),"makeadmin")==0){
                                                              		makeadmin(subString(msg,2),Response);
                                                              	}
	                                                              	else
	                                                              		if(strcmp(subString(msg,1),"removeadmin")==0){
	                                                              		removeadmin(subString(msg,2),Response);
	                                                              	}
	                                                              	  		else {printf("%s\n",msg);strcat(Response,"Comanda necunoscuta!");}
	                                                    
                                                
                                              
                                        
                                      
                                
          printf("Trimitem mesajul \"%s\" la clientul : %s!\n",Response,user);
          write (tdL.client, Response, 10000);
        }
      
    sqlite3_close(DB);
    pthread_detach(pthread_self());   
    close ((intptr_t)arg);
    return(NULL); 
      
};

static void *chatDBtoClient(void * arg){
  struct thData tdL; 
  tdL= *((struct thData*)arg);

  sqlite3* DB; 
  char* Response = (char*) calloc(10000,1);
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(10000,1);
  char* table = (char*) calloc(100,1);
  strcat(table,tdL.chatdb);
  char* messageError;
  int newlastmsgno, lastmsgno;
  int friendsno = getFriendsNo(tdL.from), newfriendsno;
  sqlite3_open("LearNet.db", &DB); 

  lastmsgno = getLastmsgno(table);
  friendsno = getFriendsNo(tdL.from);

  printf("am ajuns in while\n");
  while(true){
    usleep(125000); // 1 000 000 microseconds = 1 second
    newlastmsgno = getLastmsgno(table);
    newfriendsno = getFriendsNo(tdL.from);

    if(newlastmsgno > lastmsgno){
      bzero(Response,10000);
      for(int k = lastmsgno+1; k<=newlastmsgno;k++){
        strcat(Response,"<CHAT_MESSAGE>");
        bzero(query,10000);
        bzero(sql,10000);
        strcat(sql,"SELECT sender, msg FROM ");strcat(sql,table);strcat(sql," WHERE msgno = ");strcat(sql,itoa(k));
        strcat(sql,";");
        sqlite3_exec(DB, sql, callback, query, &messageError); 

        strcat(Response,query);
        strcat(Response,"\n");}

      write (tdL.client, Response, 10000);
      lastmsgno = newlastmsgno;
    }

    if(newfriendsno > friendsno){
      bzero(Response,10000);

      bzero(sql,10000);
      bzero(query,10000);
      strcat(sql,"SELECT friend FROM friendslist WHERE username = '");strcat(sql,tdL.from);strcat(sql,"';");
      sqlite3_exec(DB, sql, callback, query, &messageError); 
      
      for(int k = friendsno+1;k <= newfriendsno;k++){
        bzero(Response,10000);
        strcat(Response,"<FRIENDS_LIST_UPDATE>");

        strcat(Response,subString(query,k));
        write(tdL.client,Response,10000);
      }
      friendsno = newfriendsno;
    }

    bzero(sql,10000);bzero(query,10000);
    strcat(sql,"SELECT terminate_chat FROM users WHERE username = '");strcat(sql,tdL.from);strcat(sql,"';");
    sqlite3_exec(DB, sql, callback, query, &messageError); 

    if(strcmp(query,"1 ")==0){
      bzero(sql,10000);bzero(query,10000);
      strcat(sql,"UPDATE users SET terminate_chat = 0 WHERE username = '");strcat(sql,tdL.from);strcat(sql,"';");
      sqlite3_exec(DB, sql, callback, query, &messageError);

      printf("S-A TERMINAT THREADUL!!!!!\n");
      sqlite3_close(DB); 
      pthread_detach(pthread_self());   
      close ((intptr_t)arg);
      return(NULL); 
    }
  }

  sqlite3_close(DB); 
  pthread_detach(pthread_self());   
  close ((intptr_t)arg);
  return(NULL); 
}

char* subString(char* sourceString,int nrCuv){
  char* subString = (char*) calloc(100,1);
  int position = 0, positionSubString=0;

  for(int cuvant = 1; cuvant <= nrCuv;cuvant++){
    while(sourceString[position]!=' ' && sourceString[position]!='\n' && sourceString[position]!='\0')
      subString[position-positionSubString]=sourceString[position++];
    if(cuvant!=nrCuv){
      position++;
      positionSubString = position+1;
    }
}
  subString[position-positionSubString+1]='\0';
  if(nrCuv==1)
    for(int i = 0;i<100;i++)subString[i]=subString[i+1];

  return subString;
}


void loginClient(char* Response,char* msg,char* user,int client,int* login, int* admin){

  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(10000,1);

  sqlite3_open("LearNet.db", &DB); 
  char* messageError;
  
  char x;

  read(client, msg, 10000);

  strcat(sql,"SELECT DISTINCT username,isadmin,isonline FROM users WHERE username = '");
  strcat(sql,subString(msg,1));
  strcat(sql,"';");

  sqlite3_exec(DB, sql, callback, query, &messageError); 
  if(strcmp(subString(query,3),"1")==0){bzero(Response,10000);strcat(Response,"User already online!\n");}
    else
      if(strcmp(subString(query,1),subString(msg,1))==0){
        memset(Response,'\0',10000);
        strcpy(Response,"Logged in as user: ");
        strcat(Response,subString(msg,1));
        strcat(Response,"\n");
        strcat(user,subString(msg,1));

        printf("[server]Trimitem mesajul inapoi...%s\n",Response);
        *login = 1;

        if(strcmp(subString(query,2),"1")==0){*admin = 1;
	        memset(Response,'\0',10000);
	        strcpy(Response,"Logged in as admin: ");
	        strcat(Response,subString(msg,1));
	        strcat(Response,"\n");
        }
        if(strcmp(user,"admin")==0){
	        memset(Response,'\0',10000);
	        strcpy(Response,"Logged in as superadmin: ");
	        strcat(Response,subString(msg,1));
	        strcat(Response,"\n");
        }
        write (client, Response, 10000);

        bzero(sql,10000);
        strcat(sql,"UPDATE users SET isonline = 1 WHERE username = '");
        strcat(sql,subString(msg,1));
        strcat(sql,"';");

        sqlite3_exec(DB, sql, callback, query, &messageError); 

        sqlite3_close(DB); 
        return;
        }
    
  sqlite3_close(DB); 
  return;
}

void showLecture(char* Response,char* msg){
    sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(1000,1);

  sqlite3_open("LearNet.db", &DB); 
  char* messageError; 

  strcat(sql,"SELECT lecturename FROM lectures WHERE lecturename = '");strcat(sql,subString(msg,2));strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError);  

  if(strcmp(query,"") == 0){
    strcat(Response,"Documentul nu exista!\n");
    }
    else{
      bzero(sql,1000);
      bzero(query,10000);
      strcat(sql,"SELECT content FROM lectures WHERE lecturename = '");strcat(sql,subString(msg,2));strcat(sql,"';");
      sqlite3_exec(DB, sql, callback, query, &messageError);  

      bzero(Response,10000);
      strcat(Response,query);
      }

  sqlite3_close(DB);
}

void lectureDelete(char* Response, char* msg, int client){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(1000,1);

  sqlite3_open("LearNet.db", &DB); 
  char* messageError; 

  strcat(sql,"SELECT lecturename FROM lectures WHERE lecturename = '");strcat(sql,subString(msg,2));strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError);  

  if(strcmp(query,"") == 0){
    strcat(Response,"Documentul nu exista!\n");
    }
    else{
      bzero(sql,1000);
      strcat(sql,"DELETE FROM lectures WHERE lecturename = '");strcat(sql,subString(msg,2));strcat(sql,"';");
      sqlite3_exec(DB, sql, callback, query, &messageError);  

	  bzero(sql,1000);
      strcat(sql,"DROP TABLE ");strcat(sql,subString(msg,2));strcat(sql,";");
      sqlite3_exec(DB, sql, callback, query, &messageError);  

      strcat(Response,"Lecture deleted succesfully!");
      }

  sqlite3_close(DB);
}

void lectureAdd(char* Response, char* msg, int client){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(1000,1);

  sqlite3_open("LearNet.db", &DB); 
  char* messageError; 

  strcat(sql,"SELECT lecturename FROM lectures WHERE lecturename = '");strcat(sql,subString(msg,2));strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError);  

  if(strlen(msg)<=12);
    else 
      if(strcmp(query,"") != 0){
      	bzero(msg,10000);
        read(client,msg,10000);  
        strcat(Response,"Documentul exista deja!\n");
        }
        else{
          char* lectureName = (char*) calloc(10000,1);strcat(lectureName,subString(msg,2));
          bzero(sql,1000);
          strcat(sql,"INSERT INTO lectures ( lecturename, content ) VALUES ( '");strcat(sql,lectureName);strcat(sql,"', '");
          printf("\n\nWAITING FOR LECTURE TEXT\n\n");
          bzero(msg,10000);
          read(client,msg,10000);          
          if(strcmp(msg,"CANCEL_LECTURE")==0){
          	strcat(Response,"Lecture was canceled!");
			sqlite3_close(DB);
			return;          	
          }
          strcat(sql,msg);strcat(sql,"' );");
          sqlite3_exec(DB, sql, callback, query, &messageError);

          memset(sql,'\0',1000);
          strcat(sql,"CREATE TABLE ");
          strcat(sql,lectureName);
          strcat(sql," ( msgno INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, sender TEXT NOT NULL, msg TEXT NOT NULL );");
          sqlite3_exec(DB, sql, callback, query, &messageError);

          memset(sql,'\0',1000);
          strcat(sql,"INSERT INTO ");strcat(sql,lectureName);
          strcat(sql,"  VALUES ( 1, 'LearNet', 'You can now chat with eachother! :)');");
          sqlite3_exec(DB, sql, callback, query, &messageError); 

          bzero(Response,10000);
          strcat(Response,"Lecture created succesfully");
          }

  sqlite3_close(DB);
}

int testIfUserExists(char* name){
    sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(10000,1);
  
  strcat(sql,"SELECT DISTINCT username FROM users WHERE username = '");
  strcat(sql,subString(name,1));
  strcat(sql,"';");

  sqlite3_open("LearNet.db", &DB); 
  char* messageError; 
  sqlite3_exec(DB, sql, callback, query, &messageError);   
  sqlite3_close(DB);
  if(strcmp(subString(query,1),subString(name,1))==0)return 1;
 
  return 0;
}

int testIfLectureExists(char* name){
    sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(10000,1);
  
  strcat(sql,"SELECT DISTINCT lecturename FROM lectures WHERE lecturename = '");
  strcat(sql,subString(name,1));
  strcat(sql,"';");

  sqlite3_open("LearNet.db", &DB); 
  char* messageError; 
  sqlite3_exec(DB, sql, callback, query, &messageError);   
  sqlite3_close(DB);
  if(strcmp(subString(query,1),subString(name,1))==0)return 1;
 
  return 0;
}

void friend(char* Response, char* msg,char* user){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(1000,1);

  sqlite3_open("LearNet.db", &DB); 
  char* messageError; 

  if(testIfUserExists(subString(msg,2)) == 0){
  	bzero(Response,10000);
    strcat(Response,"Userul pe care l-ati inserat nu exista!");
    }
    else {
      char* existsFriend = calloc(10000,1);

      existsFriend=friendDBname(user,msg);
      printf("%s\n",existsFriend);

      strcat(sql,"SELECT * FROM ");strcat(sql,existsFriend);strcat(sql,";");
      sqlite3_exec(DB, sql, callback, query, &messageError); 

      if(strcmp(query,"")!=0){bzero(Response,10000);strcat(Response,"Sunteti prieteni deja!");}
        else {
          memset(sql,'\0',1000);
          strcat(sql,"CREATE TABLE ");
          strcat(sql,existsFriend);
          strcat(sql," ( msgno INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, sender TEXT NOT NULL, msg TEXT NOT NULL );");
          sqlite3_exec(DB, sql, callback, query, &messageError); 
          memset(sql,'\0',1000);
          strcat(sql,"INSERT INTO ");strcat(sql,existsFriend);
          strcat(sql,"  VALUES ( 1, 'LearNet', 'You can now chat with eachother! :)');");
          sqlite3_exec(DB, sql, callback, query, &messageError); 

          bzero(sql,1000);
          strcat(sql,"INSERT INTO friendslist ( username, friend) VALUES ( '");strcat(sql,user);strcat(sql,"', '");strcat(sql,subString(msg,2));strcat(sql,"' );");
          sqlite3_exec(DB, sql, callback, query, &messageError); 

          bzero(sql,1000);
          strcat(sql,"INSERT INTO friendslist ( username, friend) VALUES ( '");strcat(sql,subString(msg,2));strcat(sql,"', '");strcat(sql,user);strcat(sql,"' );");
          sqlite3_exec(DB, sql, callback, query, &messageError); 
          
          strcat(Response,"Felicitari! Te-ai imprietenit cu ");
          strcat(Response,subString(msg,2));
          strcat(Response,"!");    
          }                    
      }
  sqlite3_close(DB); 
}

int testIfFriends(char* msg, char* user){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(1000,1);

  sqlite3_open("LearNet.db", &DB); 
  char* messageError; 
  char* existsFriend = calloc(10000,1);

  existsFriend = friendDBname(user,msg);

  strcat(sql,"SELECT msgno FROM ");strcat(sql,existsFriend);strcat(sql," WHERE msgno = 1;");
  sqlite3_exec(DB, sql, callback, query, &messageError); 

  if(strcmp(query,"")!=0)return 1;
    else return 0;                 
      
  sqlite3_close(DB); 
}

char* itoa(int x){
  char* rezultat = (char*) calloc(10,1);
  int div = 1, nr = 0, y;
  if(x<0){
    rezultat[nr++]='-';
    x=-x;
  }

  y=x;
  while(y>9){
    div*=10;
    y/=10;
  }
  while(div!=0){
    rezultat[nr++]=((x/div)%10)+'0';
    div/=10;
  }
  rezultat[nr]=0;
  return rezultat;
}

static int callback(char* data, int argc, char** argv, char** colName) 
{ 
    int i;  
    for (i = 0; i < argc; i++) { 
        strcat(data,argv[i]); 
        strcat(data," ");
    } 
    return 0; 
} 

char* friendDBname(char* user,char* msg){
  char* existsFriend = calloc(10000,1);

  if(strcmp(subString(user,1),subString(msg,2))>0){strcat(existsFriend,subString(user,1));strcat(existsFriend,subString(msg,2));}
    else {strcat(existsFriend,subString(msg,2));strcat(existsFriend,subString(user,1));}

  return existsFriend;
}

int getLastmsgno(char* table){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(1000,1);
  char* messageError;

  sqlite3_open("LearNet.db", &DB); 

  strcat(sql,"SELECT MAX(msgno) FROM ");strcat(sql,table);strcat(sql,";");
  //strcat(sql," GROUP BY msgno;");

  sqlite3_exec(DB, sql, callback, query, &messageError); 
  
  sqlite3_close(DB); 
  //printf("din functie: %s\n",query);
  return atol(query);
}

char* sqlInsert( char* user, char* table, char* msg){
  char* sql = (char*) calloc(10000,1);

  strcat(sql,"INSERT INTO ");strcat(sql,table);
  strcat(sql," ( sender, msg ) VALUES ( ");
  strcat(sql,"'");strcat(sql,user);strcat(sql,"', '");strcat(sql,msg);strcat(sql,"' );");

  return sql;
}

void initLectures(int client){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(1000,1);
  char* messageError; 
  int noLectures;

  sqlite3_open("LearNet.db", &DB);
  
  strcat(sql,"SELECT MAX(lectureid) FROM lectures;");
  sqlite3_exec(DB, sql, callback, query, &messageError); 
  noLectures = atol(query);
  printf("%i\n",noLectures);
  write(client,&noLectures,4);

  for(int k = 1;k <= noLectures;k++){
    bzero(sql,1000);
    bzero(query,10000);
    strcat(sql,"SELECT lecturename FROM lectures WHERE lectureid = ");strcat(sql,itoa(k));strcat(sql,";");
    sqlite3_exec(DB, sql, callback, query, &messageError); 

    write(client,query,10000);

    read(client,query,10000);
  }

  sqlite3_close(DB); 
}

void getFriendList(char* user,int client){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(10000,1);
  char* messageError; 
  int noFriends;

  sqlite3_open("LearNet.db", &DB); 
  
  strcat(sql,"SELECT COUNT(friend) FROM friendslist WHERE username = '");strcat(sql,user);strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError); 
  noFriends = atol(query);
  printf("Friends:%i\n",noFriends);
  write(client,&noFriends,4);

  bzero(sql,10000);
  bzero(query,10000);
  strcat(sql,"SELECT friend FROM friendslist WHERE username = '");strcat(sql,user);strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError); 
  
  for(int k = 1;k <= noFriends;k++){
    bzero(sql,10000);
    strcat(sql,subString(query,k));
    write(client,sql,10000);
    printf("friends: %s\n",subString(query,k));
    read(client,sql,10000);
  }

  sqlite3_close(DB); 
}

void signUp(char* Response,char* msg,int client){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(1000,1);
  char* messageError; 

  bzero(msg,10000);
  read(client,msg,10000);

  if(testIfUserExists(msg)==1){
    bzero(Response,10000);
    strcat(Response,"User already exists!\n");

    sqlite3_close(DB); 
    return (0);
  }

  sqlite3_open("LearNet.db", &DB); 
  
  strcat(sql,"INSERT INTO users ( username, isadmin, isonline, terminate_chat) VALUES ( '");
  strcat(sql,subString(msg,1));strcat(sql,"', 0, 0, 0);");
  sqlite3_exec(DB, sql, callback, query, &messageError); 

  bzero(sql,1000);
  strcat(sql,"INSERT INTO friendslist ( username, friend) VALUES ( '");
  strcat(sql,subString(msg,1));strcat(sql,"', '");strcat(sql,subString(msg,1));strcat(sql,"');");
  sqlite3_exec(DB, sql, callback, query, &messageError);

  bzero(sql,1000);
  strcat(sql,"CREATE TABLE ");strcat(sql,subString(msg,1));strcat(sql,subString(msg,1));
  strcat(sql," ( msgno INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, sender TEXT NOT NULL, msg TEXT NOT NULL);");
  sqlite3_exec(DB, sql, callback, query, &messageError);

  memset(sql,'\0',1000);
  strcat(sql,"INSERT INTO ");strcat(sql,subString(msg,1));strcat(sql,subString(msg,1));
  strcat(sql,"  VALUES ( 1, 'LearNet', 'You can now chat with eachother! :)');");
  sqlite3_exec(DB, sql, callback, query, &messageError);
  
  bzero(Response,10000);
  strcat(Response,"User created succesfully!\n");

  sqlite3_close(DB); 
  return (0);
}

void deleteAccount(char* user){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* msgtemp = (char*) calloc(10000,1);
  char* sql = (char*) calloc(1000,1);
  char* messageError; 
  int noFriends;

  sqlite3_open("LearNet.db", &DB); 
  
  strcat(sql,"SELECT COUNT(friend) FROM friendslist WHERE username = '");strcat(sql,subString(user,1));strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError); 
  noFriends = atol(query);

  bzero(sql,1000);
  bzero(query,10000);
  strcat(sql,"SELECT friend FROM friendslist WHERE username = '");strcat(sql,subString(user,1));strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError); 
  
  for(int k = 1;k <= noFriends;k++){
    bzero(sql,1000);
    bzero(msgtemp,10000);
    strcat(msgtemp,subString(query,k));strcat(msgtemp," ");strcat(msgtemp,subString(query,k));
    strcat(sql,"DROP TABLE ");strcat(sql,friendDBname(subString(user,1),msgtemp));strcat(sql,";");
    sqlite3_exec(DB, sql, callback, query, &messageError); 
    printf("droptable: %s\n",sql);
  }
  
  bzero(sql,1000);
  strcat(sql,"DELETE FROM users WHERE username = '");
  strcat(sql,subString(user,1));strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError); 

  bzero(sql,1000);
  strcat(sql,"DELETE FROM friendslist WHERE username = '");
  strcat(sql,subString(user,1));strcat(sql,"' OR friend = '");strcat(sql,subString(user,1));strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError);

  sqlite3_close(DB); 
  return (0);
}

int getFriendsNo(char* user){
    sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(10000,1);
  char* messageError; 

  sqlite3_open("LearNet.db", &DB); 
  
  strcat(sql,"SELECT COUNT(friend) FROM friendslist WHERE username = '");strcat(sql,user);strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError); 
  sqlite3_close(DB);
  //printf("\n**%s**\n**%i**\n",sql,atol(query));
  return  atol(query); 
}

void makeadmin(char* username,char* Response){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(10000,1);
  char* messageError; 

  sqlite3_open("LearNet.db", &DB); 
  
  if(testIfUserExists(username)==0){strcat(Response,"User does not exist!");return;}

  strcat(sql,"UPDATE users SET isadmin = 1 WHERE username = '");strcat(sql,username);strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError); 
  sqlite3_close(DB);
  strcat(Response,"User is now admin!");
}

void removeadmin(char* username,char* Response){
  sqlite3* DB; 
  char* query = (char*) calloc(10000,1);
  char* sql = (char*) calloc(10000,1);
  char* messageError; 

  sqlite3_open("LearNet.db", &DB); 
  
  if(testIfUserExists(username)==0){strcat(Response,"User does not exist!");return;}

  strcat(sql,"UPDATE users SET isadmin = 0 WHERE username = '");strcat(sql,username);strcat(sql,"';");
  sqlite3_exec(DB, sql, callback, query, &messageError); 
  sqlite3_close(DB);
  strcat(Response,"User is not admin anymore!");
}