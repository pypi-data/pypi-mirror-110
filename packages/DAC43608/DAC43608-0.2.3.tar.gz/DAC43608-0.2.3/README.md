# DAC43608

Python library for the DAC43608

### Installation

You will need `python3` first, install with
```
sudo apt update
sudo apt install -y python3-pip
```

Install the library with:

```
pip3 install DAC43608
```


### Simple usage

```python
from DAC43608 import DAC43608

dac = DAC43608()

# turn on channel A
dac.power_up(dac.A)

# set channel A to 75% of reference voltage
dac.set_intensity_to(dac.A, 0.75)


# power up all channels:
dac.power_up_all()

# power down all
dac.power_down_all()

# write to a channel B
dac.write_dac_B([0x08, 0x04])
```
