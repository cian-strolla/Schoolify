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

$findsender = '';
$findsender2 = '';
$senderfname = '';
$senderlname = '';
$senderfname2 = '';
$senderlname2 = '';

$con = mysqli_connect('cs1.ucc.ie','rjf1','ahf1Aeho','2021_rjf1');
if (!$con) {
    die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con, "2021_rjf1");
$sql="SELECT * FROM discussion_board WHERE sender_id = '".$q."' AND receiver_id = '".$k."'";
$result = mysqli_query($con,$sql);

echo "<table id='discussion_table'>
<tr id='discussion_header'>
<th class='sendernameh'>Sender Name</th>
<th class='messageh'>Message</th>
<th class='timestamph'>Timestamp</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
  $findsender = $row['sender_id'];
}

$sql2 = "SELECT * FROM users WHERE id = '".$findsender."'";
$senderfinder = mysqli_query($con,$sql2);


while($row1 = mysqli_fetch_array($senderfinder)) {
    $senderfname = $row1['first_name'];
    $senderlname = $row1['last_name'];
}

$sql3="SELECT * FROM discussion_board WHERE sender_id = '".$q."' AND receiver_id = '".$k."'";
$final = mysqli_query($con,$sql3);

while($row = mysqli_fetch_array($final)) {
    echo "<tr>";
    echo "<td class='sendername'>" . $senderfname . " " . $senderlname . "</td>";
    echo "<td class='message'>" . $row['message'] . "</td>";
    echo "<td class='timestamp'>" . $row['time_stamp'] . "</td>";
    echo "</tr>";
}

$sql4="SELECT * FROM discussion_board WHERE sender_id = '".$k."' AND receiver_id = '".$q."'";
$result = mysqli_query($con,$sql4);

while($row = mysqli_fetch_array($result)) {
  $findsender2 = $row['sender_id'];
}

$sql5 = "SELECT * FROM users WHERE id = '".$findsender2."'";
$senderfinder = mysqli_query($con,$sql5);

while($row2 = mysqli_fetch_array($senderfinder)) {
    $senderfname2 = $row2['first_name'];
    $senderlname2 = $row2['last_name'];
}

$sql6="SELECT * FROM discussion_board WHERE sender_id = '".$k."' AND receiver_id = '".$q."'";
$final = mysqli_query($con,$sql6);

while($row = mysqli_fetch_array($final)) {
    echo "<tr>";
    echo "<td class='sendername'>" . $senderfname2 . " " . $senderlname2 . "</td>";
    echo "<td class='message'>" . $row['message'] . "</td>";
    echo "<td class='timestamp'>" . $row['time_stamp'] . "</td>";
    echo "</tr>";
}


echo "</table>";
mysqli_close($con);
?>
</body>
</html>
