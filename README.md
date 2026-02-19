# SWE_Team14

1) Install Python (if not already installed)

check version:
    python3 --version
if not installed:
    sudo apt update
    sudo apt install python3

2) Install pip

    sudeo apt install python3-pip
verify installation:
    python3 -m pip --version

3) Instal Python package

   python -m pip install psycopg2-binary

4) Database Setup
     1) install PostgreSQL
        sudo apt install postgresql postgresql-contrib
     Start PostgreSQL:
        sudo systemctl start postgresql

     2) Create Database
      Log in to PostgreSQL:
          sudo -u postgres psql
      Create database:
          CREATE DATABASE playerdb;
      Connect to database:
          \c playerdb
      Create players table:
          CREATE TABLE players (
              player_id INTEGER PRIMARY KEY,
              codename VARCHAR(50) NOT NULL
          );
       Exit PostgreSQL:
          \q

Running the Program:
  python3 Main.py





Usernames:

katelyncraig  - Katelyn Craig
India-Jones   - India Jones
ReaganC05     - Reagan Clark
DarlaEthridge - Darla Ethridge
gaylene-perez - Gaylene Perez
