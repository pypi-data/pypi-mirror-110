# webstaterator

A `jinja2` powered static website generator that generates pages based on a JSON data models.

## Why?

I wanted to convert my `PHP` websites to static sites to save money but could not find a python based tool that allowed me to use a data model to do so.

### Why the stupid name?

I needed a name to create the repo, a friend suggested `webstaterator`. Good work Sasha!

## Install

```bash
pip install webstaterator
```

## Running

Webstaterator is available via the CLI using `webstaterator`. Help can be found using `webstaterator -h`

## Modes

| Action | Info | Arguments | Example |
|--------|------|-----------|---------|
| Verify | Check that a website setup is correct | **-w**, **--website** -  website.json | `webstaterator verify -w website.json` |
| Build | Build a website | **-w**, **--website** - website json. **-o**, **--output** - output directory | `webstaterator -w website.json -o build/` |
| Template | Generate a template for a website | **-o**, **--output** - output directory | `webstaterator template -o website/` |


## Website json

The website description JSON powers `webstaterator`. It can be used to describe two types of page, a standard page and a list page.
- A standard page simply takes a `jinja2` template, a file name, and an option data model and outputs a page.
- A list page  on top of the standard page attributes, specifies a target element within the data model. This will result in a page for every child element targeted in the list page.

### Format

```json
{
  "name":"my example website",
  "model":"model.json",
  "template":"templates/",
  "assets": ["images"],
  "pages": [
    {
      "name":"index",
      "template":"main.html",
      "filename":"index.html"
    }
  ]
}
```

- **name**: The name of the website  
- **model [optional]**: The path to a json object
- **template**: The path to a directory containing a set of `jinja2` template files
- **assets [optional]**: One or more directories to be copied into the build folder. This can be things like images, CSS, or JavaScript
- **pages:**: An array of pages see below for more details

### Basic Pages

- **name**: Name of the page, can be used to access the URL on other pages or check which page is currently being rendered
- **template**: The `jinja2` template file (found in the provided template directory)
- **filename**: The name of the output file. This is the file name use on the live site

### List Pages

- **name**: Name of the page, can be used to access the URL on other pages or check which page is currently being rendered
- **template**: The `jinja2` template file (found in the provided template directory)
- **filename**: The name of the output file. This is the file name use on the live site. Unlike a basic page a list filename **must** include `{}` so that a unique filename can be created for every item in the list
- **list**: The dot delimited path to the target array or dictionary within the provided data model.
- **id [optional]**: If the target of list is an array use `id` to specify the child attribute to use as an id.

#### List example targeting a dictionary

Given the following data model
```json
{
  "example": {
    "people": {
      "Chris": {
        "height": 6.1,
        "age": 34,
        "face": "ugly"
      },
      "Steve":{
        "height": 5.11,
        "age": 40,
        "face": "round"
      },
      "Karen":{
        "height": 5.2,
        "age": 38,
        "face": "trapazoid"
      }
    }
  }
}
```

and the page

```json
"pages": [
  {
    "name":"people",
    "template":"people.html",
    "filename":"person-{}.html",
    "list":"example.people"
  }
]
```

the output would be

- person-Chris.html
- person-Steve.html
- person-Karen.html

when generating each page the value in the dictionary will be made available via the `target` variable. So when rendering `person-Chris.html` the following will be available to the template `people.html` :-

```json
{
  "height": 6.1,
  "age": 34,
  "face": "ugly"
}
```

#### List example targeting an array

The same example would look like this if we used an array instead of a dictionary

```json
{
  "example": {
    "people": [
       {
        "name":"Chris",
        "height": 6.1,
        "age": 34,
        "face": "ugly"
      },
      {
        "name":"Steve",
        "height": 5.11,
        "age": 40,
        "face": "round"
      },
      {
        "name":"Karen",
        "height": 5.2,
        "age": 38,
        "face": "trapazoid"
      }
    ]
  }
}
```

and the page

```json
"pages": [
  {
    "name":"people",
    "template":"people.html",
    "filename":"person-{}.html",
    "list":"example.people",
    "id":"name"
  }
]
```

Notice this time we need to include an id to specify which attribute to use as an id.

the output for the above would be

- person-Chris.html
- person-Steve.html
- person-Karen.html

## Templates

Each `jinja2` template will have access to the following variables :-

- **links** - A dict of links with page name as key and an array of URLs as the value
- **page_link** - The URL for the current page
- **model** - The JSON file loaded described in the website JSON if provided

If the page is a list page the template will also have access to :-

- **target** - The child data element found in model that is linked to this list page.
