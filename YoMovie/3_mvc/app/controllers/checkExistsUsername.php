<?php

define ('DOCXML', './particip.xml');
header ('Content-type: text/xml');
require_once '../core/DB.php';

function checkExistsUsername ($username) {
    $con = DB::getInstance()->getConnection();
    $stmt = $con->prepare('SELECT id FROM users WHERE username=?');
    $stmt->bindParam(1, $username, PDO::PARAM_STR,20);
    $stmt->execute();
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    if($row)return 1;

	return 0;
}
?>
<response>
  <result><?php echo checkExistsUsername($_REQUEST['username']); ?></result>
</response>
