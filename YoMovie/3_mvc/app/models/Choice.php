<?php

class Choice extends Model {
    public $id = 0;
    public $descriere = '';
    public $textIntrebare = '';
    public $clipPath = '';
    public $idPrecedent = 0;
    public $choiceNumber = 0;
    public $movieId = 0;
    public $badgeId = -1;
    public $vizualizari = 0;

    public function __construct($idClip) {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT * FROM choices WHERE id=?');
        $stmt->bindParam(1, $idClip, PDO::PARAM_INT);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if($row) {
           $this->id = $row['id'];
           $this->descriere = $row['descriere'];
           $this->textIntrebare = $row['text_intrebare'];
           $this->clipPath = $row['clip_path'];
           $this->idPrecedent = $row['id_precedent'];
           $this->choiceNumber = $row['choice_number'];
           $this->movieId = $row['movie_id'];
           $this->badgeId = $row['badge_id'];
           $this->vizualizari = $row['vizualizari'];
        }
        else {
            $this->id = $idClip;
        }
    }

    public static function giveVizualizare($id)
    {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('UPDATE choices SET vizualizari = vizualizari + 1 WHERE id=?');
        $stmt->bindParam(1, $id, PDO::PARAM_INT);
        $stmt->execute();
    }

    public static function getAllChildNodes($idClip) {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT * FROM choices WHERE id_precedent=? ORDER BY choice_number;');
        $stmt->bindParam(1, $idClip, PDO::PARAM_INT);
        $stmt->execute();
        $choiceArray = [];
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
           $choiceModel = new Choice($row['id']);
           /*
           $choiceModel->id = $row['id'];
           $choiceModel->descriere = $row['descriere'];
           $choiceModel->textIntrebare = $row['text_intrebare'];
           $choiceModel->clipPath = $row['clip_path'];
           $choiceModel->idPrecedent = $row['id_precedent'];
           $choiceModel->choiceNumber = $row['choice_number'];
           */
           array_push($choiceArray,$choiceModel);
        }	
        return $choiceArray;
    }

}