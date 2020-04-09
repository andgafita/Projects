<?php 
session_start(); 
if(!isset($_SESSION['user']))header("Refresh:0;url = /mvc/public/logincontroller");

class WatchController extends Controller {
    public function index() {
        echo 'mama';
    }

    private function addBadge($id, $badge) {
        if($badge->id != 0) {
            $con = DB::getInstance()->getConnection();
            $stmt = $con->prepare('SELECT * FROM rewards WHERE user_id=? and badge_id=?');
            $stmt->bindParam(1,$id, PDO::PARAM_INT);
            $stmt->bindParam(2, $badge->id, PDO::PARAM_INT);
            $stmt->execute();
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
            if(!$row) {
                $stmt = $con->prepare('INSERT INTO rewards VALUES(?,?)');
                $stmt->bindParam(1, $id, PDO::PARAM_INT);
                $stmt->bindParam(2, $badge->id, PDO::PARAM_INT);
                $stmt->execute();
                return 1;
            }
            return 0;
        }
        return 0;
    }

    public function watch($clipNr = 0) {
        $this->model('Choice');
        $this->model('Badge');
        $choice = new Choice($clipNr);
        $badge = new Badge($choice->badgeId);
        $added = $this->addBadge($_SESSION['userID'], $badge);
        $this->view('watch/watch',['childNodes'=>Choice::getAllChildNodes($clipNr),'badge'=>$badge,'added'=>$added], $choice);
        //$vi = new UploadView();
        //$vi->content();
    }
}