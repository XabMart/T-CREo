
const express = require('express');
const app = express();

app.get('/', function (req, res) {
  res.send('�Hola, mundo!');
});

app.listen(5000, function () {
  console.log('El servidor est� ejecut�ndose en el puerto 3000');
});
