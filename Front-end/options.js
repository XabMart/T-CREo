const saveButton = document.getElementById('save-button');

document.addEventListener('DOMContentLoaded', function() {
    chrome.storage.local.get("text-credibility-config", function(result) {
      console.log("Values retrieved from local storage:", result["text-credibility-config"]);
      if (result && result["text-credibility-config"]) {
        // Asignar los valores recuperados a los campos de input
        document.getElementById('spam-detection').value = result["text-credibility-config"]["spam_weight"];
        document.getElementById('bad-words-detection').value = result["text-credibility-config"]["bad_words_weight"];
        document.getElementById('misspelling-detection').value = result["text-credibility-config"]["spell_errors_weight"];
      }
    });

  chrome.storage.local.get("credibility-config", function(result) {
    console.log("Values retrieved from local storage:", result["credibility-config"]);
    // Asignar los valores recuperados a los campos de input
    document.getElementById('text-credibility').value = result["credibility-config"]["text_credibility_weight"];
    document.getElementById('user-credibility').value = result["credibility-config"]["user_credibility_weight"];
    document.getElementById('social-credibility').value = result["credibility-config"]["social_credibility_weight"];
  });

});


saveButton.addEventListener('click', function() {
  const spamDetection = parseFloat(document.getElementById('spam-detection').value);
  const badWordsDetection = parseFloat(document.getElementById('bad-words-detection').value);
  const misspellingDetection = parseFloat(document.getElementById('misspelling-detection').value);
  const textCredibility = parseFloat(document.getElementById('text-credibility').value);
  const userCredibility = parseFloat(document.getElementById('user-credibility').value);
  const socialCredibility = parseFloat(document.getElementById('social-credibility').value);

  const sum1 = spamDetection + badWordsDetection + misspellingDetection;
  const sum2 = textCredibility + userCredibility + socialCredibility;

  const textCredibilityConfig = {
  "spam_weight": spamDetection,
  "bad_words_weight": badWordsDetection,
  "spell_errors_weight": misspellingDetection
  };

  const credibilityConfig = {
  "text_credibility_weight": textCredibility,
  "user_credibility_weight": userCredibility,
  "social_credibility_weight": socialCredibility
  };
    
  if (sum1 == 1 && sum2 == 1) {
    chrome.storage.local.set({"text-credibility-config": textCredibilityConfig}, function() {
        console.log("Values saved to local storage");
    });

    chrome.storage.local.set({"credibility-config": credibilityConfig}, function() {
        console.log("Values saved to local storage");
    });


  } else {
    alert('Data is not correct. Correct and save again.');
  }
});
