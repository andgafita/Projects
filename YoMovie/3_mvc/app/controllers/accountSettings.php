<?php

class accountSettings extends Controller {
    public function index() {
        
        $this->view('accountSettings/accountsettings');
    }

    public function getMail(){
        session_start();

        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT email FROM users WHERE username=?');
        $stmt->bindParam(1, $_SESSION['user'], PDO::PARAM_STR,20);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        return $row['email'];
    }

    public function updateData() {
        session_start();

        if( isset($_POST['newPass']) && isset($_POST['confNewPass']) && ($_POST['newPass'] == $_POST['confNewPass']) && $_POST['newPass'] != "" ) {
            $con = DB::getInstance()->getConnection();
            $stmt = $con->prepare('UPDATE users SET parola = ? WHERE username=?');
            //$stmt->bindParam(1, $_POST['confNewPass'], PDO::PARAM_STR,17);
            //$stmt->bindParam(2, $_SESSION['user'], PDO::PARAM_STR,20);
            $stmt->execute([sha1($_POST['confNewPass']), $_SESSION['user']]);
        }

        if( isset($_POST['username']) && ($_SESSION['user'] != $_POST['username']) ) {
            $con = DB::getInstance()->getConnection();
            $stmt = $con->prepare('UPDATE users SET username = ? WHERE username=?');
            //$stmt->bindParam(1, $_POST['username'], PDO::PARAM_STR,20);
            //$stmt->bindParam(2, $_SESSION['user'], PDO::PARAM_STR,20);
            $stmt->execute([$_POST['username'],$_SESSION['user']]);

            $_SESSION['user'] = $_POST['username'];
        }

        if( isset($_POST['email']) && $this->getMail() != $_POST['email']) {
            $con = DB::getInstance()->getConnection();
            $stmt = $con->prepare('UPDATE users SET email = ? WHERE username=?');
            //$stmt->bindParam(1, $_POST['email'], PDO::PARAM_STR,30);
            //$stmt->bindParam(2, $_SESSION['user'], PDO::PARAM_STR,20);
            $stmt->execute([ $_POST['email'], $_SESSION['user']]);
            }
        
            header("Refresh:0;url = /mvc/public/accountSettings");
            //$this->view('accountSettings/accountsettings');
        }
    }
