<!DOCTYPE html>
<html>
<head>
<style>
table {
    width: 100%;
    border-collapse: collapse;
}

table, td, th {
    border: 1px solid black;
    padding: 5px;
}

th {text-align: left;}
</style>
</head>
<body>

<?php
$q = strval($_GET['q']);
$k = strval($_GET['k']);

$con = mysqli_connect('cs1.ucc.ie','rjf1','ahf1Aeho','2021_rjf1');
if (!$con) {
    die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con, "2021_rjf1");
$sql="SELECT * FROM discussion_board WHERE sender_id = '".$q."' AND receiver_id = '".$k."'";
$result = mysqli_query($con,$sql);

echo "<table>
<tr>
<th>Sender</th>
<th>Message</th>
<th>Timestamp</th>
</tr>";
while($row = mysqli_fetch_array($result)) {
    echo "<tr>";
    echo "<td>" . $row['sender_id'] . "</td>";
    echo "<td>" . $row['message'] . "</td>";
    echo "<td>" . $row['time_stamp'] . "</td>";
    echo "</tr>";
}
echo "</table>";
mysqli_close($con);
?>
</body>
</html>
