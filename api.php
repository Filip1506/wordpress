<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

$host = "mysql45.simply.com";  // Opdater med din database-host
$username = "itco_dk";       // Opdater med dit database-brugernavn
$password = "BbawpD64fGFcdAEgrzRt"; // Opdater med din adgangskode
$database = "itco_chatbot";    // Opdater med dit database-navn

// Forbind til databasen
$conn = new mysqli($host, $username, $password, $database);

if ($conn->connect_error) {
    die(json_encode(["error" => "Database connection failed: " . $conn->connect_error]));
}

// Hent spørgsmål fra databasen
$sql = "SELECT key_name, text FROM questions";
$result = $conn->query($sql);

$questions = [];
while ($row = $result->fetch_assoc()) {
    $questions[] = $row;
}

echo json_encode($questions);
$conn->close();
?>