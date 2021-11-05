# BeyondTo20
Beyond to twenty is to be used to scrape the game log from dndbeyond and post rolls into roll20.

## TECHNOLOGY
Python
Selenium
Chromedriver

## HOW TO

*Download Chromedriver and extract it. BT20 defaults to checking for "C:/Program Files (x86)/Chromedriver.exe". You can change it on line 14.

*BT20 uses two seperate chrome profiles, a default, and a profile 2. Copy your path for chrome profiles there, or into a .env such as written on line 17 & 18.
(default path should be similar to this "C:/Users/{USERNAME}/AppData/Local/Google/Chrome/User Data/")

*If this is your first time using BT20:<br/>
  Login with your preferred OAUTH provider on D&D Beyond. If you are not able to login with google, you can try and allow less secure apps permissions, however this did not work with my testing. <br/>
  The method that works for me is creating a new google account for this app.

 *Create a new character<br/>
  suggested class: Homebrew "Scribe"<br/>
  suggested background: "Scribe of the Chromium Dragon. Job description: Transcribe messages for those in another plane, and write them to something they call 'text area'. Pay is in exposure."

*If this is a new campaign or you just made your 'Scribe of the Chromium Dragon':<br/>
  Invite your BT20 listener character to your campaign.

*Select your campaign from 'my campaigns'

*Login to roll20 with the new browser.

*Select your game.

Congrats! BT20 will now print out all rolls to your campaign.
