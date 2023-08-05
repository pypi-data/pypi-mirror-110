# socialfeeder
Mini CLI to feed social activities with supported actions:
* Click
* Fill
* Browse
* Scroll down
* Wait

Installation:
```
python -m pip install socialfeeder --upgrade

# install from git
python -m pip install git+https://github.com/datnguye/socialfeeder.git --upgrade

# check version
python -m socialfeeder --version
```


## Usage
```
python -m socialfeeder --help
```

Sample commands:
* Run facebook:
```
python -m socialfeeder --social "facebook" --config "C:\Users\DAT\Documents\Sources\socialfeeder\samples\like_top_5-share_2-posts.xml" --feed
```

## Development Enviroment
Virtual enviroment:
```
python -m venv env
```

Activate virtual env:
```
Windows: 	.\env\Scripts\activate
Linux:		source env/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```


