# Simple data-collecting python server
A simple python server that can: 
- serve an html page 
- collect data that is PUT to the address `/data` and save locally or to an s3 bucket
- keep a simple counter

Can be deployed to Heroku.

# Setup
To save data in local files, set the var `SAVE_LOCALLY` in `server/server.py` to `True`; to save to S3, set the var to `False`.

If you want to use with S3, you must set the env vars in `server/example_config.sh`, locally and/or in the heroku remote.

Include whatever ui code you want in the `ui` folder; include `index.hmtl` as the root.

To run locally: `python3 server/server.py [port num]` or `./run.sh`

Modified from: https://gist.github.com/bradmontgomery/2219997
