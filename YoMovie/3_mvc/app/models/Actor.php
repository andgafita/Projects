<?php

class Actor extends Model {
    public $id;
    public $nume;
    public $prenume;
    public $varsta;

    public function __construct() {
        ;
    }

    public function set($nume, $prenume, $varsta) {
        $this->nume = $nume;
        $this->prenume = $prenume;
        $this->varsta = $varsta;
    }

    private function getMaxActorId()
    {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT MAX(id) as maximum FROM actors');
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        $idMax = $row['maximum'] + 1;
        return $idMax;
    }

    public static function getActorID($nume, $prenume)
    {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT id FROM actors WHERE nume=? AND prenume=?');
        $stmt->bindParam(1, $nume, PDO::PARAM_STR);
        $stmt->bindParam(2, $prenume, PDO::PARAM_STR);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($row) {
            return $row['id'];
        }
        else {
            return NULL;
        }
    }

    public static function getActorOr404($id) {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT * FROM actors WHERE id=?');
        $stmt->bindParam(1, $id, PDO::PARAM_INT);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($row) {
           $actor = new Actor();
           $actor->id = $row['id'];
           $actor->nume = $row['nume'];
           $actor->prenume = $row['prenume'];
           $actor->varsta = $row['varsta'];
           return $actor;
        }	
        else {
            return NULL;
        }
    }

    public function commit() {
        $con = DB::getInstance()->getConnection();
        $stmt = $con->prepare('SELECT * FROM actors WHERE id=?');
        $stmt->bindParam(1, $this->id, PDO::PARAM_INT);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        if($row) {
            $stmt = $con->prepare('UPDATE actors SET nume=?, prenume=?, varsta=? WHERE id=?');
            $stmt->bindParam(1, $this->nume, PDO::PARAM_STR);
            $stmt->bindParam(2, $this->prenume, PDO::PARAM_STR);
            $stmt->bindParam(3, $this->varsta, PDO::PARAM_INT);
            $stmt->bindParam(4, $this->id, PDO::PARAM_INT);
            $stmt->execute();
        }
        else {
            $this->id = $this->getMaxActorId();
            $stmt = $con->prepare('INSERT INTO actors (id, nume, prenume, varsta) VALUES (?, ?, ?, ?)');
            $stmt->bindParam(1, $this->id, PDO::PARAM_INT);
            $stmt->bindParam(2, $this->nume, PDO::PARAM_STR);
            $stmt->bindParam(3, $this->prenume, PDO::PARAM_STR);
            $stmt->bindParam(4, $this->varsta, PDO::PARAM_INT);
            $stmt->execute();
        }
    }
}