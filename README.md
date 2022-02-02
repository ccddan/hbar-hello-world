# Hedera - Hello World Py

## Development Environment

### Dependencies

Create and activate python environment:

```bash
$ python -m venv ./.env-hbar
$ source .env-hbar/bin/activate
```

Install python packages:

```bash
$ pip install -r requirements.dev.txt
$ pip install -r requirements.txt
```

Define Env Vars. After creating the `.env` file with the following command,
update the value of the environment variables inside `.env`:

```bash
$ cp .dev.env .env
```

## Usage

**main.py**

```bash
$ python src/main.py
```

- Load hedera testnet account (root account)
- Create a new testnet account (new account)
- Transfer HBAR tokens between accounts
- Publish/Subscribe to topics

**hts.py**

```bash
$ python src/hts.py
```

- Create custom token
- Send custom token from treasury to another account
  - Association
  - KYC
  - Token transaction
- Show account info
