# Crypto Dash
#### Video Demo:  <https://www.youtube.com/watch?v=x6z0yFUXQig>

## Getting Started

Simply do a "flask run" command within the vscode environment and click on the generated link. API key is already hardcoded in the program.

### Description

My Project is about creating a cryptocurrency dashboard using the CoinMarketCap API and widgets. I used the Finance problem set as the backbone of my project, but significantly updated the look of the website to make it look more dark-themed and also less blocky. I used a lot of border radius styling in my CSS to make sure the buttons look a bit more modern. I also extensively used bootstrap to make sure that the elements of my web page are responsive and relatively retain their size ratio no matter the size of the viewport. I tried using media queries at one point but decided to delete it as using vh for some text makes the resizing look smoother in action.

Another thing I reused from Finance is the MemeGenerator API, which I had a lot of fun tinkering with. It was used mainly to generate what the problem set called "apology" pages, which anticipates any mistakes a user can make in filling up the forms in this web app. It serves as a reminder and to steer the user to the right direction.

In the beginning, my project was supposed to be a mock trading platform for currencies you own, but I found it very difficult to work with APIs. Manipulating the information received through code was very alien to me, and so I opted instead to just use a simple dashboard project. And yet, even that proved to be more than enough of a challenge for me!

After creating all the frontend, login, and database details, I had to work with the API in figuring out how to determine that the user inputted symbol exists in the CoinMarketCap database. I ended up passing in the user input as a parameter for the request. I also had to create another function that again calls the API just to get each coin's ID information to be passed in the SQL database. For some reason, I couldn't return a dictionary with more than one key-value pair and iterate through it. I kept getting an "int object is not subscriptable" error.

My line of code that didn't work:

>return JSONdata["symbol"]

Anyway, I ended up iterating through each JSONdata (picked up from the API) and grabbing the key-value pair I want. So now I have 2 similar functions that do an API request to get 2 different values: a coin's ticker and it's CoinMarketCap ID. I'm sure there's a better way of doing things.

My next step was creating a SQL table for the new values and to connect each user to their portfolio of CoinMarketCap IDs, which will be used to iteratively create widgets in a JINJA for loop inside the index.html page.

THe final step was to create a way to remove the coins. I decided to use a checkbox because it's the most intuitive way if you want to remove multiple objects at once. It took me a while to figure out how to do this, and was starting to build Rube Goldberg scripts inside my html when I finally found out after hours of research that I can simply get the checkbox value with Python in Flask! All i needed was this very simple code:

>request.form.getlist('checkbox')

And after that, I was finally able to more or less complete my first Fullstack web project.

Thanks for reading all that and I hope I made enough sense!

## Deployment

I found out that only static pages can be deployed in github pages. I am eploring other options, such as Heroku, to create a live demo of this website.

## Built With

* [Bootstrap](https://getbootstrap.com/) - The web framework used
* [MemeGenerator API](https://memegen.link/) - Used to generate apology pages
* [CoinMarketCap API](https://coinmarketcap.com/api/) - Used to generate price widgets


## Acknowledgments

* Thank you to the CS50 Finance problem set for the login and database help
* Quick coding Tuts on Youtube and his dropdown menu was very helpful
* Shoutout to W3 schools for being so insanely helpful with HTML and CSS elements