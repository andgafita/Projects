<?php

class DB {
  // Hold the class instance.
  private static $instance = null;
  private $conn;
  
  private $host = '127.0.0.1';
  private $user = 'root';
  private $pass = '';
  private $name = 'yomovie_db';
  private $opt = [
	// erorile sunt raportate ca exceptii de tip PDOException
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    // rezultatele vor fi disponibile in tablouri asociative
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    // conexiunea e persistenta
    PDO::ATTR_PERSISTENT 		 => TRUE
];
   
  // The db connection is established in the private constructor.
  private function __construct() {
    $this->conn = new PDO("mysql:host={$this->host};
    dbname={$this->name}", $this->user,$this->pass,$this->opt);
  }
  
  public static function getInstance() {
    if(!self::$instance) {
      self::$instance = new DB();
    }
   
    return self::$instance;
  }
  
  public function getConnection()
  {
    return $this->conn;
  }
}