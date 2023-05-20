// Incluye la biblioteca jQuery
var script = document.createElement('script');
script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js';
script.onload = function() {
  chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.message === 'background_to_content') {
      console.log("Me ha llegado el mensaje.")
      scrapeTimeline(request.list);
    }
  });
};

function scrapeTimeline(list) {
  console.log("He iniciado la funcion.");
  
  $(function() {
    // Utiliza jQuery para seleccionar los tweets en el timeline
    var tweets = $('article[data-testid="tweet"]');
    console.log("Estoy dentro de la funcion.");
    console.log(tweets);
    
    tweets.each(function(index) {
      // Accede al contenido de texto del tweet
      var tweet = $(this);
      var text = tweet.html();
      
      // Obten la credibilidad del tweet correspondiente al indice actual
      var credibility = list[index];
      
      // Anade "CREDIBILITY:" al final del texto del tweet junto con el valor de credibilidad
      var newText = text + ' <span style="font-weight: bold; color: ' + getColorFromCredibility(credibility) + ';">Text credibility: ' + credibility + '</span>';
      
      // Crea un nuevo elemento div con el texto modificado
      var newContent = $('<div>').html(newText);
      
      // Reemplaza el contenido del tweet con el nuevo elemento
      tweet.html(newContent);
    });
  });
}

function getColorFromCredibility(credibility) {
  // Define los colores segun el valor de credibilidad
  if (credibility >= 70.0) {
    return 'green'; // verde
  } else if (credibility >= 40.0) {
    return 'orange'; // naranja
  } else {
    return 'red'; // rojo
  }
}

document.getElementsByTagName('head')[0].appendChild(script);
