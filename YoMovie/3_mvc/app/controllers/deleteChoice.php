<?php
require_once '../core/DB.php';
$idChoice = $_POST['idChoice'];

$con = DB::getInstance()->getConnection();
$stmt = $con->prepare('DELETE FROM choices WHERE id=?');
$stmt->bindParam(1, $idChoice, PDO::PARAM_INT);
$stmt->execute();