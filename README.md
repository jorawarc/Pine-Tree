
# Pine Tree
A Dicord Bot that fetchs useful game data and information

## League of Legends
- Live game stats
- Champion cool down times

## Call of Duty: Warzone
- Post game stats
    - Average Team KD
    - Team ranking relative to lobby

## Spell Break
TBA

## Usage
Running an instance of Pine Tree requires access to the Discord API, Riot Games API and a Activision Account.
The fields in `.env_template` should be filled and then renamed to `.env`

### Local Instance
```
python -m pip install -r requirements.txt
python ./main.py
```

### Docker Instance
```
docker build -t pine tree .
docker run --env-file=.env -d pine-tree
```
