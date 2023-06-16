# Project setup

## Backend Requirements

- [Docker](https://www.docker.com/).
- [Docker Compose](https://docs.docker.com/compose/install/).
- [Poetry](https://python-poetry.org/) for Python package and environment management.

## Frontend Requirements

- Node.js (with `npm`).

## Installing backend dependencies

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

From `./backend/` you can install all the dependencies with:

```console
$ poetry install
```

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

## Installing frontend dependencies

You should install [Node.js](https://nodejs.org/en).
From `./frontend/` you can install all the dependencies with:

```console
$ npm install
```

Then you can run the frontend and try the app with

```console
$ npm run dev
```

## Demo

Nevertheless, our app is hosted publicly, so don't bother with the above and visit our website [Uncle's](https://uncles.vercel.app/).

Here you can explore all functionality of our [Uncle's API](https://uncles-api.onrender.com/docs#/).
