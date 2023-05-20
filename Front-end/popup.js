function updateCredibility(credibility) {
  var credibilityElement = document.getElementById('credibility');
  credibilityElement.textContent = credibility;
}

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.type === 'update_credibility') {
    var credibility = message.credibility;
    var credibilityValue = extractCredibilityValue(credibility);
    updateTimelineButtonVisibility(credibility);
    updateCredibilityColor(credibilityValue)
    updateCredibility(credibility);
  }
});

document.addEventListener('DOMContentLoaded', function() {
  var followButton = document.getElementById('followButton');
  var credibility = document.getElementById('credibility');
  var optionsButton = document.getElementById("optionsButton");
  var timelineButton = document.getElementById("timelineButton"); // Agregado

  optionsButton.addEventListener("click", function() {
    window.open("options.html", "Opciones", "width=496,height=740");
  });

  followButton.addEventListener('click', function() {
    chrome.runtime.sendMessage({type: 'follow'}, function(response) {
      console.log('Follow button clicked');
    });
  });

  timelineButton.addEventListener('click', function() {
    chrome.runtime.sendMessage({type: 'scrapeTimeline'}, function(response) {
      console.log('Timeline button clicked');
    });
  });
});


function updateTimelineButtonVisibility(credibility) {
  var timelineButton = document.getElementById('timelineButton');
  
  if (credibility.includes('Credibility')) {
    timelineButton.style.display = 'block';
  } else {
    timelineButton.style.display = 'none';
  }
}

function extractCredibilityValue(credibility) {
  // Verifica si la cadena contiene la palabra "Credibility:" seguida de un número
  var regex = /Credibility:\s*(\d+)/i;
  var match = regex.exec(credibility);
  if (match && match[1]) {
    return parseInt(match[1]);
  }
  return null;
}

function updateCredibilityColor(credibilityNumber) {
  var credibilityField = document.getElementById('credibility');
  if (credibilityNumber !== null) {
    credibilityField.textContent = credibilityNumber;
    // Cambia el color del campo en función del valor de la credibilidad
    if (credibilityNumber >= 70) {
      credibilityField.style.color = 'green';    // Cambia a verde si la credibilidad es mayor o igual a 50
    } 
    else if(credibilityNumber >= 40){
        credibilityField.style.color = 'orange'
    }
    else {
      credibilityField.style.color = 'red';      // Cambia a rojo si la credibilidad es menor a 50
    }
  } else {
    credibilityField.textContent = 'N/A';        // Muestra "N/A" si no se encontró un número de credibilidad válido
    credibilityField.style.color = 'black';      // Restaura el color negro por defecto
  }
}