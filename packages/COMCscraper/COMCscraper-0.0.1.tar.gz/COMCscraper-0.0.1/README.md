# COMCscraper

# Jared Randall

This is package has been built to scrape the website, Check Out My Cards (COMC). COMC...

This package is strictly built for end users who wish to scrape data for personal use. If you are interested in using this data for professional purposes, I recommend you look into the <a href="https://www.eliteprospects.com/api" >Elite Prospects API</a>.

Please be consideration of COMC servers when using COMCscraper.

# Installation
---

You can install the package by entering the following command in terminal:

<code> pip install COMCscraper</code>

Then import the module using this function:

<code> import COMCscraper as comc</code>

# User-End Functions

---

### function one

Returns a dataframe containing...

<ul>
    <li>leagues: One or multiple leagues. If one league, enter as a string i.e; "nhl". If multiple leagues, enter as a tuple or list i.e; ("nhl", "ahl").</li>
    <li>seasons: One or multiple leagues. If one league, enter as a string i.e; "2018-2019". If multiple leagues, enter as a tuple or list i.e; ("2018-2019", "2019-2020").</li>
    </ul>

Example code:

<code></code>

Example:

Say you obtain skater data for the KHL in 2020-2021 and store that as a dataframe called <code>output</code>. You can run this function to get bio information for every player in that league's scrape.

<code>output = tdhepscrape.get_skaters("khl", "2020-2021")</code>

<code>tdhepscrape.get_player_information(output)</code>

---

# Comments, Questions, or Concerns.

---

If you should have any comments, questions or concerns about COMCscraper, please do not hesitate to email me at jaredtroyrandall@gmail.com.

If you have any requests, please feel free to send them my way as well :)