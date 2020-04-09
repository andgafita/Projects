<?php

class LoginController extends Controller {
    public function index() {
        if(!isset($_SESSION))session_start();
        if(isset($_SESSION['user'])){session_destroy();session_unset();header("Location: /mvc/public/logincontroller");}
        $this->view('login/login');
        //header("Location: /mvc/public/logincontroller");
    }

    public function checkExistsUsername(){
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT id FROM users WHERE username=?');
        $stmt->bindParam(1, $_POST['username'], PDO::PARAM_STR,20);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        return $row;
    }

    public function checkExistsEmail(){
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT id FROM users WHERE email=?');
        $stmt->bindParam(1, $_POST['email'], PDO::PARAM_STR,30);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        return $row;
    }

    public function maxUserID(){
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT MAX(id) AS maximum FROM users');
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        
        $maxID = $row['maximum'] + 1;

        return $maxID;
    }

    public function autentificare() {
        if( isset($_POST['username']) && isset($_POST['pass']) && $_POST['username']!="" && $_POST['pass']!="" ) {
            $con = DB::getInstance()->getConnection();
            $stmt = $con->prepare('SELECT id FROM users WHERE username=? AND parola=?');
            $stmt->bindParam(1, $_POST['username'], PDO::PARAM_STR,20);
            $stmt->bindValue(2, sha1($_POST['pass']), PDO::PARAM_STR);
            $stmt->execute();
            $row = $stmt->fetch(PDO::FETCH_ASSOC);

            if($row) {
                if(!isset($_SESSION))session_start();
                $_SESSION['user']=$_POST['username'];
                $_SESSION['userID']=$row['id'];
                //echo $_SESSION['user'];
                //$this->view('home/index');
                //header("Location: ../home");
                header("Location: /mvc/public/home");
            }
            else {
                //$this->view('login/login');
                header("Location: /mvc/public/logincontroller");
            }
        }
        else {
            $this->view('login/login',['wrongForm'=>"Complete all fields!"]);
        }
    }

    public function inregistrare() {
        //echo $_POST['pass'] . " " . $_POST['confirmpass'];
        if(isset($_POST['email'])&&isset($_POST['username'])&&isset($_POST['pass'])&&isset($_POST['confirmpass'])) {
            if($this->checkExistsUsername()) {
                $this->view('login/login',['wrongForm'=>"User already exists!"]);
            }
            else if($this->checkExistsEmail()){
                $this->view('login/login',['wrongForm'=>"Email already registered!"]);
            } 
            else{
                $con = DB::getInstance()->getConnection();
                $stmt = $con->prepare('INSERT INTO users (id,email,username,parola) VALUES(' . $this->maxUserID() . ',?,?,?)');
                //echo $this->maxUserID();
                //$stmt->bindParam(1, $this->maxUserID(), PDO::PARAM_INT);
                $stmt->bindParam(1, $_POST['email'], PDO::PARAM_STR,30);
                $stmt->bindParam(2, $_POST['username'], PDO::PARAM_STR,20);
                $stmt->bindValue(3, sha1($_POST['pass']), PDO::PARAM_STR);
                $stmt->execute();
                $this->view('login/login',['succes'=>"Ati fost inregistrat"]);
            }
        }
        else {
            $this->view('login/login',['wrongForm'=>"Complete all fields!"]);
        }
    }
}
