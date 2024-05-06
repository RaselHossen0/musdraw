import express from 'express';
import cors from 'cors';
import http from 'http';
import { Server } from 'socket.io';
import pool from './db.js';
const app = express();
app.use(cors());
app.use(express.json());
const server = http.createServer(app);

const io = new Server(server, {
    cors: {
        origin: '*',
        methods: ['GET', 'POST'],
    },
});


app.post('/create_user', async (req, res) => {
    // console.log(req.body);
    const { user_name } = req.body;
    try {
        const result = await pool.query('SELECT * FROM users WHERE username = ?', [user_name]);
        //console.log(result);
        if (result[0].length > 0) {
            res.status(200).send({ success: true, id: result[0][0].id, user_name: result[0][0].username });
        } else {
            const insertResult = await pool.query('INSERT INTO users (username) VALUES (?)', [user_name]);
            if (insertResult.affectedRows > 0) {
                const newUser = await pool.query('SELECT * FROM users WHERE username = ?', [user_name]);
                if (newUser[0].length > 0) {
                    res.status(200).send({ success: true, id: newUser[0][0].id, user_name: newUser[0][0].username });
                } else {
                    res.status(500).send('Error retrieving new user');
                }
            } else {
                res.status(500).send('Error creating user');
            }
        }
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal server error');
    }
});

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}
async function checkGameForUser (user_id) {
    const game= await pool.query(`SELECT * from game_users where user_id=${user_id}`);
    if(game[0].length>0){
        return game[0][0].game_id;
    }
    else{
        return -1;
    }
}
async function getEmptyGame() {
  const game = await pool.query("SELECT games.id FROM games JOIN game_users ON games.id = game_users.game_id WHERE games.active = 1 GROUP BY games.id HAVING COUNT(game_users.user_id) < 5");
 // console.log(game);
  if (game[0].length > 0) {
      return game[0][0].id;
  } else {
      return -1;
  }
}

async function getPlayerCount(game_id){
    const game = await pool.query(`SELECT COUNT(*) as player_count FROM game_users WHERE game_id = ${game_id}`);
    return game[0][0];
}
io.on('connection', (socket) => {
    console.log(`a user connected ${socket.id}`);
  
    socket.on('disconnect', () => {
      console.log('user disconnected');
    });
  
    socket.on('join', async (data) => {
       console.log('User joined:', data);
      const emptyGameId = await getEmptyGame();
      console.log('Empty Game ID:', emptyGameId);
      if(emptyGameId!=-1){
        //check if user is already in a game
        const gameIdUser = await checkGameForUser(data.user_id);
        if(gameIdUser!=-1){
          socket.join(`${gameIdUser}`);
          socket.emit('game_created', { game_id: gameIdUser });
          return;
        }
        const assign = await pool.query(`INSERT INTO game_users (game_id, user_id) VALUES (${emptyGameId}, ${data.user_id})`);
        socket.join(`${emptyGameId}`);
        socket.emit('game_created', { game_id: emptyGameId });

      }

      
      // socket.emit('user_joined', { user_id: data.user_id });
      const gameIdUser = await checkGameForUser(data.user_id);
      if(gameIdUser!=-1){
        socket.join(`${gameIdUser}`);
        socket.emit('game_created', { game_id: gameIdUser });
        return;
      }
      else {
        const createNewGame = await pool.query('INSERT INTO games (active, player_count) VALUES (1, 1)');
        const gameId = createNewGame[0].insertId;
        const assign = await pool.query(`INSERT INTO game_users (game_id, user_id) VALUES (${gameId}, ${data.user_id})`);
        socket.join(`${gameId}`);
        socket.emit('game_created', { game_id: gameId });
        return ;
      }
  
    });

    socket.on('draw', (data) => {
      
       console.log('Drawing:', data);
      const game_id=data.game_id;
    
      io.to(`${game_id}`).emit('drawing_rcv', data);
    }
    );
    socket.on('drawing', (data) => {
      console.log('Drawing:', data);
      const game_id=data.game_id;
      io.to(`${game_id}`).emit('drawing_rcv', data);
    }
    );
  
    
  
  
    socket.on('send_message', async (data) => {
      const { game_id, user_id, content } = data;
      console.log('Message:', content);
      console.log('Game ID:', game_id);
      console.log('User ID:', user_id);
      const message = await pool.query('INSERT INTO messages (user_id, game_id, content) VALUES (?, ?, ?)', [user_id, game_id, content]);
      const messageId = message[0].insertId;
      console.log('Message ID:', messageId);
      const user = await pool.query('SELECT username FROM users WHERE id = ?', [user_id]);
      // console.log('User:', user[0][0].username);
      var userName=user[0][0].username;
      console.log('User:', userName);
  
      io.to(`${game_id}`).emit('new_message', { message_id: messageId, user_id: user_id, user_name:userName,message: content });
      console.log('Message sent');

    });
    socket.on('player_count', async (data) => {
      const { game_id } = data;
      const playerCount = await getPlayerCount(game_id);
      console.log('Player Count:', playerCount);
      socket.broadcast.to(game_id).emit('new_message', { message_id: messageId, user_id: user_id, message: content });
    }
    );
    
  
    socket.on('submit_guess', async (data) => {
      const { game_id, user_id, guess } = data;
      const game = await pool.query('SELECT * FROM games WHERE id = ?', [game_id]);
      const word = await pool.query('SELECT word FROM words WHERE id = ?', [game[0][0].word_id]);
      const correctWord = word[0][0].word;
  
      let score = 0;
      if (guess.toLowerCase() === correctWord.toLowerCase()) {
        score = 100; // Adjust the score as needed
        await pool.query('UPDATE games SET active = 0 WHERE id = ?', [game_id]);
      }
  
      const userScore = await pool.query('INSERT INTO scores (game_id, user_id, score) VALUES (?, ?, ?)', [game_id, user_id, score]);
  
      // Emit the guess result to all players in the game room
      io.to(`game_${game_id}`).emit('guess_result', { user_id, guess, correct_word: correctWord, score });
    });
  });

  

server.listen(8000, () => {
    console.log('Server is running on port 8000');
});