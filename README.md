# Do You Know Card

A web application finding hot issues in Dcard.

Updates:
2019.12.04  Update the list of kanban & tidy up the project.

## Get Started - Build up environment(First Time)

  1. Clone and get into the root folder(do-you-know-card).
  2. Create a virtual environment named "venv".
  ```
  python -m venv venv
  ```
  3. Get into the virtual environment.
  ```
  source ./venv/bin/activate
  ```
  4. Install the necessary packages.
  ```
  pip install -r requirements.txt
  ```

## Let's Run.

  Open terminal and get into the root folder.
  Then run by typing the following command in terminal:
  1. Get into the virtual environment.
  ```
  source ./venv/bin/activate
  ```
  2. Run index.py
  ```
  python index.py
  ```
  
## Trouble Shooting
  1. ```urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1049)>```  
  Solution: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
