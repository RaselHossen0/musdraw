//const mysql = require('mysql');
import mysql from 'mysql2/promise';
import dotenv from 'dotenv';
dotenv.config();

const pool = mysql.createPool({
  // port: process.env.DB_PORT,
   host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.MYSQL_DB,
  // connectionLimit: 10//to limit the number of connections to the database
});
if(pool){

  
  console.log('Connected to the database');
}
if (!pool) {
  console.log('not Connected to the database');
}
export default pool;