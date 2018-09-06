
**Stockify** allows you to stay updated with the stock market by querying
all the stocks you are following.

# Stockify: Setup Guide

Built from a scaffolded Django app, which can easily be deployed to
Heroku, and configured with Twilio Programmable SMS.

## Get Twilio Programmable SMS

If you haven't already, head on over to [Twilio](https://www.twilio.com)
to get your `Twilio phone number`, you will need it to setup the project.

Additionally, you will need [Account SID and Auth Token](https://www.twilio.com/console) from your Twilio
Console.

Once you have all three of them, run:
``` sh
cp config.py.template config.py
```
and put the update info in **config.py**.

## Heroku Configuration

Create an account on Heroku and create your app.

Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

Link remote heroku app to your local project
```sh
heroku git:remote -a NAME_OF_YOUR_HEROKU_APP
```

## Running Locally

Clone the repo, make sure you have [Python](http://install.python-guide.org), [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup) and [ngork](https://ngrok.com/download) installed.

```sh
$ cd stockify

$ pip install pipenv
$ pipenv install
$ pipenv shell

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
 ```

Your app should now be running on [localhost:5000](http://localhost:5000/).

To run the app with Twilio Programmable SMS, you will need a public url,
 which could be obtained by running [ngork](https://ngrok.com/docs)
 forwarding local port.

## Configure your Twilio Function

There are several ways to achieve this, you will essentially need a way
to trigger the REST API hosted on Heroku.

One easy way to achieve so is using the "drag and drop"
[Twilio Studio](https://www.twilio.com/console/studio/dashboard). Create
your flow and use a split statement for `Incoming Message` and configure
transition to HTTP Request.

### Available endpoints
Available endpoint for the Twilio Studio function includes:
```
    https://YOUR_HEROKU_URL/getall
        Request Body {{trigger.message.From}}

    https://YOUR_HEROKU_URL/unsubscribe
        Request Body {{trigger.message.From}}

    https://YOUR_HEROKU_URL/get
        Request Body {{trigger.message.From}} {{trigger.message.Body}}

    https://YOUR_HEROKU_URL/add
        Request Body {{trigger.message.From}} {{trigger.message.Body}}

    https://YOUR_HEROKU_URL/remove
        Request Body {{trigger.message.From}} {{trigger.message.Body}}
```

Once the Twilio Flow is deployed, add that flow to the incoming SMS of
the Twilio that you purchased.

## Deploying to Heroku
If you are using Heroku for deployment, head over to settings page of your project,
add 
`URL_BASE`
`ACCOUNT_SID`
`AUTH_TOKEN`
`TWLO_CELL`
and their corresponding value into the form.

```sh
$ git push heroku master

$ heroku run python manage.py migrate
```

## Bonus Step: Setting up daily market open/close update

If you want to get scheduled reminder of your stock price, we've got you
covered.

```sh
heroku addons:create scheduler:standard
```

Edit the `trigger.py` in the repo with your own url and deploy to heroku.

Head over to [Heroku console](https://scheduler.heroku.com/dashboard)
and select `Add new job`. Enter:
```
python trigger.py
```
to the command input and schedule your triggering time.

Wala! Now you can get scheduled stock market update automatically.