# AudioMoth PySocket

### Installation
```
sudo apt-get install portaudio19-dev python-pyaudio
virtualenv venv
source venv/bin/activate
pip install -R requirements.txt
```

### Running

The recorder is the device that is connected to the AudioMoth in USB Mic. Mode

```
# On a RaspberryPi device
source venv/bin/activate
python3 recorder.py
```

The receiver is the computer that will get the audio data
```
# On the receiver device
source venv/bin/activate
python3 receiver.py
```
