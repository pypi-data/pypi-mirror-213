# krrsnk-api
Easy way to use my API

[Switch to Russian](https://github.com/kararasenok-gd/krrsnk-api#readme)
## Getting the key
1. [Log in](https://kararasenok.ueuo.com/accounts/login.php) (if necessary [register](https://kararasenok.ueuo.com/accounts/register.php))
2. [Go](https://kararasenok.ueuo.com/api/create/) and create a key
3. We save the received key somewhere
4. Done!
## Examples
### Example 1: Interaction with [Chat](https://kararasenok.ueuo.com/tests/phpchat)

I added the ability to interact with the chat. Here is an example:

```python
from krrsnkapi import Chat

message = input("Message to send: ")

status = Chat("your API Key").send_message(message)

if status == "MESSAGE_ADDED":
     print("Sent!")
elif status == "KEY_NOT_FOUND":
     print("Key not found")
else:
     print("Unknown error")
```

### Example 2: Base64

There is also a Base64 decoder and encoder, here is an example of a decoder:

```python
from krrsnkapi import Base64

message = input("Text to decode: ")

status = Base64("your API Key").decode(message)

if status == "KEY_NOT_FOUND":
     print("Key not found")
else:
     print(status)
```

And here is the encoder:

```python
from krrsnkapi import Base64

message = input("Text to decode: ")

status = Base64("your API Key").decode(message)

if status == "KEY_NOT_FOUND":
     print("Key not found")
else:
     print(status)
```

There will be more opportunities in the future! If you want, you can offer something in [Telegram!](https://t.me/logovo_amogusov)