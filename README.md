# teeworlds-map-convert-6to7
python script using twmap to move doodads from 0.6 positions to 0.7 positions

## quickstart

```
git clone git@github.com:ChillerDragon/teeworlds-map-convert-6to7
cd teeworlds-map-convert-6to7
pip install -r requirements.txt
./twmap_6to7.py ~/.teeworlds/maps/mymap.map mymap_07_doodads.map
```

## linting

```
pip install -r requirements/dev.txt
mypy .
pylint twmap_6to7.py
```
