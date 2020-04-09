<?php

define ('DOCXML', './particip.xml');
header ('Content-type: text/xml');
require_once '../core/DB.php';

function checkExistsEmail ($email) {
    $con = DB::getInstance()->getConnection();
    $stmt = $con->prepare('SELECT id FROM users WHERE email=?');
    $stmt->bindParam(1, $email, PDO::PARAM_STR,30);
    $stmt->execute();
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    if($row)return 1;

	return 0;
}
?>
<response>
  <result><?php echo checkExistsEmail($_REQUEST['email']); ?></result>
</response>
