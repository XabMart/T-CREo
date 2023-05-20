# T-CREo
T-CREo Chrome extension to calculate Twitter accounts and tweets credibility.

The Front-end contains the Chrome add-on which is used as interface with the user. It has three main buttons:
 - The Follow button is used to add accounts to the database. In order to do so, the user must be visualizing the account timeline in the Chrome active tab and back-end must      be running.
 - The Options button is used to set the parameters of the credibility filters.
 - The Timeline button shows the credibility of the tweets of the timeline that is being visualized on the Chrome active tab. To be able to calculate the credibility, the        account must be stored in the database before.

The Back-end contains the scripts to calculate the credibility of accounts and tweets, to create the account and tweets repository and the real-time tweets processing.ç
The Collections folder contains the MongoDB collections of accounts and tweets that have been retrieved during the tests of the add-on.
