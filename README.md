# Mini File Sync Program

This program allows you to keep two directories synced between hosts

## Features

- Simple server/client model
- Sync two directories. This uses modification times and then MD5 hashes

## Running

- Clone this repo on server and client
- Run `python server.py` on server. Uses files from `test_dir`
- Run `python client.py` on client. Uses files from `client_dir`

## Commands

- `ls` and `ls -l` commands to list remote files
- `hash <filename>` to print MD5 hash of remote file
- `download <filename>` to download remote file
- `upload <filename>` to upload local file
- `sync` to sync files between server and client
