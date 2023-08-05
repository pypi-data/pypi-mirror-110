# Datify
This Python3 module allows to extract parts of valid date from user input.
User input is processed through class `Datify`.
## Languages supported: 
- English
- Russian - there is russian Readme at project's GitHub.
- Ukrainian.
---

## Installing
Simply run `pip install datify` from your command line.

---
## Class:
` Datify(user_input, year, month, date) ` : takes str when creating. Also, can take particular parameters like `year`, `month`, and `day` along with user input or without it. If no parameters are given, raises ValueError. **See the section *Formats* to discover default Datify's formats.**
### Class methods:
  #### Static:
  1. `findDate(string)` : Takes string. Returns substring with date in General Date format if it is contained in the given string.
  2. `isYear(year)` : Takes str or int. Returns True if given parameter suits year format.
  3. `isDigitMonth(month)` : Takes str or int. Returns True if given parameter suits digit month format.
  4. `isAlphaMonth(string)` : Takes str. Returns True if given string suits months dictionary. *For languages in which there are multiple forms of words it's basically enough to have only the main form of the word in dictionary.*
  5. `getAlphaMonth(string)` :  Takes str. Returns number(int) of month name in given string according to months dictionary. If no month name is found in the string, returns None.
  6. `isDay(day)` : Takes str or int. Returns True if given parameter suits day format.
  7. `isDate(date)` : Takes str or int. Returns True if given parameter suits general date format (See the section *Default formats*).
  8. `isDatePart(string)` : Takes str. Returns True if given string contains at least one of date parts such as day, month, or year.
  9. `_getWordsList(string)` : from given string returns list of words splitted by a found separator in separators list (See the section *Config* on GitHub). If no separators are found, returns None.

  #### Instance:
  1. `date()` : returns datetime object from parameters of Datify object. If not all of the necessary parameters are known (`year`, `month`, and `day`), raises TypeError.
  2. `tuple()` : returns tuple from all parameters in format `(day, month, year)`
  3. `date_or_tuple()` : returns datetime object if all of the necessary parameters are known, otherwise returns tuple from all parameters.
  4. `setYear(year)` : Takes str or int. Extracts year from given parameter and sets `year` field of the called Datify object. If given parameter doesn't suit year format, raises ValueError. *If the year is given in shortened format, counts it as 20YY.*
  5. `setMonth(month)` : Takes str or int. Extracts month from given parameter and sets `month` field of the called Datify object. If given parameter doesn't suit month format and doesn't contain any month names, raises ValueError.
  6. `setDay(day)` : Takes str or int. Extracts day from given parameter and sets `day` field of the called Datify object. If given parameter doesn't suit day format, raises ValueError.

## GitHub
Extended documentation can be found at [project's GitHub](https://github.com/MitryP/datify)