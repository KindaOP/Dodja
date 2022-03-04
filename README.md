# Dodja
A simple project detecting Thai phrases and keywords from system sound output, totally not intended for skipping classes.

## Version 0.1
### Requirements (Windows)
1. Install dependencies using `pip install requirements.txt`.
2. Install VB-Cable Virtual Audio Device from https://vb-audio.com/Cable/.
3. Use CABLE Output and Speakers from VB-Cable Virtual Audio Device.
4. Listen to CABLE Output using Headphones. (Current Limitation)
5. Generate token for LINE Notify in https://notify-bot.line.me/en/.
6. Add LINE Notify to target chat/group for notification.
7. Assign token to TOKEN in juke.py.

### Usage
To run the script (for now), type in cmd:
```
python dodja.py [-h/--help] [--v] <w1> <w2> <w3> ...
```
When any phrase or keyword `<w>` is found, `report(.)` currently plays siren SFX and sends post request to LINE Notify API. Feel free to edit `report(.)` or anything within the script. Just be sure to include the original license.

