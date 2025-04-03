# Telegram bot Session createor

> [!IMPORTANT]
> **Warning**
> This project is not intended for malicious use. It is a tool for educational purposes only. Use it responsibly and ethically.
>
> **Disclaimer**
> The author is not responsible for any misuse or damage caused by this tool. Use it at your own risk.
> **Note**
> This project is not affiliated with Telegram in any way. It is an independent tool created for educational purposes only.

## Example work:
<img src='https://github.com/NoNFake/tg_bot_session_creator/blob/main/example/example_work.png' width=20%>


## Proxy setup
1. Open the `proxy.txt` file in `pyrobot/data/proxy`
2. Add your proxy in the following format:
```
# Example proxy format
# without @:

ip:port:username:password

# with @:
ip:port@username:password
```
3. Save the file

> [!NOTE]
Make sure to use a proxy that supports the `HTTP` protocol
Make sure to use a proxy that supports the `SOCKS5` protocol

## .env setup
1. Open the `.env` file.
2. Add your `API_ID`,`API_HASH`, `BOT_TOKEN` in the following format:
```
API_ID = your_api_id
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
```

3. Save the file
## Install dependencies
```bash
pip install -r req.txt
```

## Run the bot
```bash
python -m pyrobot
```
