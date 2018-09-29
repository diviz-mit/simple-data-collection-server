# Simple data-collecting python server
A simple python server that can: 
- serve an html page 
- collect data that is PUT to the address /data and save locally or to an s3 bucket
- keep a simple counter

Can be deployed to Heroku.

# Setup
To save data in local files, set the var `SAVE_LOCALLY` in `server.py` to `True`; to save to S3, set the var to `False`.

If you want to use with S3, you must set the env vars in `example_config.sh`, locally and/or in the heroku remote.

To run locally: `python3 server.py [port num]`

Modified from: https://gist.github.com/bradmontgomery/2219997
