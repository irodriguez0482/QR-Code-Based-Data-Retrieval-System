const express = require('express');
const app = express();
app.use(express.static("./public"));
const { pool } = require("./dbConfig");
const bcrypt = require('bcrypt');

require("dotenv");

const PORT = process.env.PORT || 4000; //uses env.PORT in deployment, 4000 in development

app.set('view engine', 'ejs'); //sets view engine to ejs

app.use(express.urlencoded({ extended: false })); //middleware to parse form data

app.get('/', (req, res) => {
  res.render('index');
});

app.get('/users/register', (req, res) => {
  res.render('register');
});

app.get('/users/login', (req, res) => {
  res.render('login');
});

app.get('/users/database', (req, res) => {
  res.render('database', { user: "User" });
});

app.post('/users/register', async (req, res) => {
    let { name, email, password, password2 } = req.body;
    
    console.log({
        name,
        email,
        password,
        password2
    });

    let errors = [];
    let results = [];

    //Checks that all fields are entered. If not, push message to errors array.
    if (!name || !email || !password || !password2) {
        errors.push({ message: "Please enter all fields" });
    }

    //Checks that passwords length is greater than 6 characters. If not, push message to errors array.
    if(password.length < 6) {
        errors.push({ message: "Password should be at least 6 characters" });
    }

    //Checks that passwords match. If not, push message to errors array.
    if(password !== password2) {
        errors.push({ message: "Passwords do not match" });
    }

    //Displays errors if there are any, otherwise, renders the register page.
    if(errors.length > 0) {
        res.render('register', { errors });
    }else {
        //Form validation has passed
        let hashedPassword = await bcrypt.hash(password, 10); //second argument is encryption rounds
        console.log(hashedPassword);

        //Check if user already exists.
        pool.query(
            `SELECT * FROM users`,
            (err, results) => {
              if (err) {
                console.log(err);
              }
              console.log(results.rows);
            }
          );
    }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});