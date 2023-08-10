## Install

Run in console

```bash
    pip3 install -r requirements.txt
```

## Set Up

Copy and paste _.env_example_, rename it with _.env_, and set the data required

## Run the project

### Windows

`py main.py`

### Linux & Mac

`python3 main.py`

## Create systemctl service

Go to `/etc/systemd/system` and create a file `script.service` and write:

```
[Unit]
Description="Script Description"
After=network.target

[Service]
User=server
WorkingDirectory=/home/server/script/
ExecStart=/home/server/.asdf/shims/python3.10 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

then `sudo systemctl enable script` and `sudo systemctl start script`

## Endpoints

Authorization: Bearer.

- <b>POST</b> _/ask_

  #### Body:

  ```json
  {
    "message": "test message",
    "assistant_id": "1",
    "assistant_key": "a5da4cf4-fa90-4b87-b8e6-2c3da7884e81"
  }
  ```

  #### Response:

  <b>200</b>

  ```json
  {
    "response": [
      {
        "content": "GTP config",
        "role": "system"
      },
      {
        "content": "How can I help u?",
        "role": "assistant"
      },
      {
        "content": "test message",
        "role": "user"
      },
      {
        "content": "test response",
        "role": "assistant"
      }
    ],
    "status": 200
  }
  ```

---

- <b>POST</b> _/view_

  #### Body:

  ```json
  {
    "assistant_id": "1",
    "assistant_key": "a5da4cf4-fa90-4b87-b8e6-2c3da7884e81"
  }
  ```

  #### Response:

  <b>200</b>

  ```json
  {
    "response": "https://www.image.url",
    "status": 200
  }
  ```

---

- <b>POST</b> _/create-assistant_

  #### Response:

  <b>200</b>

  ```json
  {
    "assistant_id": "1",
    "assistant_key": "a5da4cf4-fa90-4b87-b8e6-2c3da7884e81",
    "status": 200
  }
  ```

---

- <b>POST</b> _/get-memory_

  #### Body:

  ```json
  {
    "assistant_id": "1",
    "assistant_key": "a5da4cf4-fa90-4b87-b8e6-2c3da7884e81"
  }
  ```

  #### Response:

  <b>200</b>

  ```json
  {
    "response": [
      {
        "content": "GTP config",
        "role": "system"
      },
      {
        "content": "How can I help u?",
        "role": "assistant"
      },
      {
        "content": "test message",
        "role": "user"
      },
      {
        "content": "test response",
        "role": "assistant"
      }
    ],
    "status": 200
  }
  ```

---

- <b>POST</b> _/clean_memory_

  #### Body:

  ```json
  {
    "assistant_id": "1",
    "assistant_key": "a5da4cf4-fa90-4b87-b8e6-2c3da7884e81"
  }
  ```

  #### Response:

  <b>200</b>

  ```json
  {
    "response": [
      {
        "content": "GTP config",
        "role": "system"
      }
    ],
    "status": 200
  }
  ```

---

- <b>GET</b> _/health_

  #### Response:

  <b>200</b>

  ```json
  {
    "response": "OK",
    "status": 200
  }
  ```
