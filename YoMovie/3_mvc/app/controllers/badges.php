<?php
if(!isset($_SESSION)) {
    session_start();
}

class Badges extends Controller {
    public function index($movieId = 0) {
        $this->model('Movie');
        $this->model('Badge');
        $this->model('Choice');
        $badges = [];
        $results = Movie::getViewedByUser($_SESSION['userID']);
        if($movieId == 0) {
            $this->view('badges/badges',['movies'=>$results['movies'],'badges'=>$results['badges'],'all' => true]);
        }
        else {
            $this->view('badges/badges',['movies'=>$results['movies'], 'badges' => $results['badges'][$movieId],'all' => false]);
        }
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
}