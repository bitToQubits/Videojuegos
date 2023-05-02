#Por juan pablo santos
<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "Rage";


$conn = mysqli_connect($servername, $username, $password, $dbname);

#Procesamiento de resultados 
if (!$conn) {
    die("Conexión fallida: " . mysqli_connect_error());
}

$sql = "SELECT * FROM jugadores";

$resultado = mysqli_query($conn, $sql);


while ($fila = mysqli_fetch_assoc($resultado)) {
    echo "ID: " . $fila["id"] . " - Nombre: " . $fila["nombre"] . " - Score: " . $fila["Score"] . "<br>";
}

#Creacion de una matriz de datos#
$datos = array(
    array("Javier", "Peralta", "3000"),
    array("Morelia", "Garza", "1500"),
    array("Polo", "Santos", "1200")
);

#creacion de variables con codigo html# 
$tabla = "<table>";
$tabla .= "<tr><th>Nombre</th><th>Apellido</th><th>Score</th></tr>";
foreach ($datos as $fila) {
    $tabla .= "<tr>";
    foreach ($fila as $dato) {
        $tabla .= "<td>$dato</td>";
    }
    $tabla .= "</tr>";
}
$tabla .= "</table>";

echo $tabla;

?>
#cierre de Conexion 
mysqli_close($conn);
