# Are you here for Opportunity Hack 2022?
- Hacker Signup [on DevPost](https://opportunity-hack-2022.devpost.com/)
- Arizona [In-person RSVP form](https://docs.google.com/forms/d/e/1FAIpQLScTveAW1rOEN_YO-IgI0qmi3aPkFH71O5j1OElqgYUXScKysA/viewform)
- Mentor [signup](https://docs.google.com/forms/d/e/1FAIpQLSdY352vtbNhNM5fyKozQ7HbuxCKfkU6xTO2aA7cKx7UpWRZog/viewform) and more about OHack [mentorship](https://www.ohack.org/about/mentors)
- Follow us on [Instagram](https://www.instagram.com/opportunityhack/), [LinkedIn](https://www.linkedin.com/company/opportunity-hack/), [YouTube](https://www.youtube.com/@opportunityhack)


# Opportunity Hack Developer Portal (Backend)
- 📝 [ohack.dev frontend code is here](https://github.com/opportunity-hack/frontend-ohack.dev)
- This code is the backend [api.ohack.dev](https://api.ohack.dev) and supports [ohack.dev](https://www.ohack.dev) frontend.  
- Like most things we build, to keep it simple, this runs on [Heroku](https://trifinlabs.com/what-is-heroku/).
- We borrowed the code from [Auth0 here](https://github.com/auth0-developer-hub/api_flask_python_hello-world) to bootstrap our development (always a good practice)

## Quickstart
- [Use this doc to setup GitHub Codespaces](https://docs.google.com/document/d/1RDJsTLouF3S35mgFZptQv4DZXK0SC6P1mieCinFicDs/edit?usp=sharing): you won't need to download anything on your computer

- Install Python modules
```bash
pip install -r requirements.txt
```
- Run the app
```bash
flask run
```
- Create a `.env` file under the root project directory and populate it with the contents listed [in our doc here](https://docs.google.com/document/d/1RDJsTLouF3S35mgFZptQv4DZXK0SC6P1mieCinFicDs/edit#bookmark=id.ho9aqosnukcm)

# References
## Running this on your laptop
### The easy way with Heroku CLI
- Review [these instructions](https://devcenter.heroku.com/articles/heroku-cli) 
- Install Heroku CLI
- Run via `heroku local` command 

### The longer way
Create a virtual environment.
You can use:
1. [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (preferred) 
2. [Virtual Env](https://docs.python.org/3/tutorial/venv.html) (venv)
3. [Anaconda](https://www.anaconda.com/products/distribution)
4. Don't create a virtual environment at all and trample on a single Python environment you might already have

What are the diffs between Miniconda and Anaconda? [See this](https://stackoverflow.com/questions/45421163/anaconda-vs-miniconda)

You'll need to run Python 3.9.13 (see runtime.txt) to match the same version that Heroku runs.

Once you have a virtual environment ready, you will want to install the project dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file under the root project directory and populate it with the following content:

_You will need to get these values from our Slack channel_.
```bash
# Flask Settings
FLASK_APP=api
FLASK_RUN_PORT=6060
FLASK_ENV=development
PORT=6060

# AUTH0 Settings
CLIENT_ORIGIN_URL=
AUTH0_AUDIENCE=
AUTH0_DOMAIN=
AUTH0_USER_MGMT_CLIENT_ID=
AUTH0_USER_MGMT_SECRET=

# Firebase Settings
FIREBASE_CERT_CONFIG=
```


Run the project in development mode:
```bash
flask run
```


# References
- [Firestore UI](https://github.com/thanhlmm/refi-app)
- [Using Python with Firestore](https://towardsdatascience.com/nosql-on-the-cloud-with-python-55a1383752fc)
- [Querying Firestore with Python](https://firebase.google.com/docs/firestore/query-data/get-data)
- [Auth0 Python Flask boilerplate used to start this repo](https://github.com/auth0-developer-hub/api_flask_python_hello-world)