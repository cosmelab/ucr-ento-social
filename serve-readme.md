# website development server

a fast threaded python server for testing websites locally and on mobile devices.

## quick start

```bash
python3 serve.py
```

the server will:
- automatically find an available port
- show your local ip address for mobile testing
- handle multiple requests in parallel (fast mobile performance)
- use threading for better speed

## usage

### basic commands

start the server:
```bash
python3 serve.py
```

stop all servers:
```bash
python3 serve.py --kill
```

show help:
```bash
python3 serve.py --help
```

### testing on mobile

1. make sure your phone is on the same wifi network
2. use the ip address shown when the server starts
3. or scan the qr code if displayed

### using with other projects

copy `serve.py` to any website project root and run it. it works with any static website.

## features

- finds available port automatically (8000-9000 range)
- threaded server for parallel request handling (faster mobile loading)
- shows local ip for easy mobile testing
- lightweight and fast
- works on macos, linux, and windows

## troubleshooting

if port is busy:
```bash
lsof -ti:8000 | xargs kill -9  # kill server on port 8000
python3 serve.py               # start fresh
```

## requirements

- python 3.6 or higher
- no additional dependencies required