
function getCredibility() {
  // Obtiene la URL de la pestaña activa
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var activeTab = tabs[0];
    var url = activeTab.url;
    
   // Realiza una solicitud GET a la API para obtener la credibilidad de la URL anterior
    fetch('http://localhost:8000/get-credibility', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({url: url}) // Envía la URL en el cuerpo de la solicitud (opcional)
    }).then(function(response) {
      return response.json();
    }).then(function(data) {
      console.log('Received credibility (GET):', data.credibility);
      // Aquí puedes hacer lo que quieras con el valor de la credibilidad
      chrome.runtime.sendMessage({type: 'update_credibility', credibility: data.credibility});
    }).catch(function(error) {
      console.log('Error getting credibility (GET):', error);
    });
    
    // Realiza una solicitud PUT a la API con la URL de la pestaña activa
    // Realiza una solicitud POST a la API con la URL de la pestaña activa
    fetch('http://localhost:8000/get-credibility', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({url: url}) // Envía la URL en el cuerpo de la solicitud
    }).then(function(response) {
      return response.json();
    }).then(function(data) {
      console.log('Received credibility (POST):', data.credibility);

      // Aquí puedes hacer lo que quieras con el valor de la credibilidad
      chrome.runtime.sendMessage({type: 'update_credibility', credibility: data.credibility});
    }).catch(function(error) {
      console.log('Error getting credibility (POST):', error);

    });
      
  });

}

// Llama a la función getCredibility() cada segundo
setInterval(getCredibility, 5000);



chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === 'follow') {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      var url = tabs[0].url;
      var screen_name = get_screen_name_from_html(url);
      if (screen_name) {
        fetch('http://localhost:5000/add-account', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: 'url=' + screen_name  + '&event=follow'
        }).then(function(response) {
          console.log('Flask is now running');
        }).catch(function(error) {
          console.log('Error starting Flask:', error);
        });
      } else {
        console.log('Error getting screen name from URL');
      }
    });
  }
});

function get_screen_name_from_html(url) {
  var match = url.match(/twitter\.com\/(\w+)/);
  if (match) {
    return match[1];
  } else {
    return null;
  }
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === 'scrapeTimeline') {
   
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var activeTab = tabs[0];
      var currentUrl = activeTab.url;
      
      // Enviar la URL al servidor Flask
      fetch('http://localhost:5000/tweets_timeline', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: currentUrl })
      })
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        // Enviar la lista recibida a content.js
        chrome.tabs.sendMessage(activeTab.id, { message: 'background_to_content', list: data });
      })
      .catch(function(error) {
        console.error('Error:', error);
      });
    });
  }
});


