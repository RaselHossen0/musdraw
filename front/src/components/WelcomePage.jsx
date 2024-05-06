import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useSocket } from '../providers/SocketProvider';
import { useUser } from '../providers/UserContext.jsx';
const WelcomePage = () => {
    const [username, setUsername] = useState('');
    const { user, updateUser } = useUser();
  
    
    
   
    const navigate = useNavigate();  // Define navigate here
    const socket = useSocket();
    useEffect(() => {

        
    }, []);

    const handleJoin = async (e) => {
        e.preventDefault();
      
        if (username.trim()) {
          console.log("Joining game as", username);
      
          try {
            const data = {
              user_name: username
            };
      
            const response = await axios.post('http://localhost:8000/create_user', data);
            console.log(response.data);
      
            if (response.status === 200 && response.data.success) {

          
                const usertoUpdate = {
                  userId: response.data.id,
                  user_name: response.data.user_name
                };
                console.log(usertoUpdate);
              
           
                console.log('Connected to server');
           
                socket.emit('join', { user_id: response.data.id });

      
                socket.on('game_created', (data) => {

                
                  const newUserData = {
                    ...user,
                    gameId: data.game_id
                  };
                  console.log('New user data:', newUserData);
                 
            
                  // console.log('Game created:', user.gameId);
                 
                  navigate(`/waiting_room`,
                    {
                      state: {
                        userId: response.data.id,
                        gameId: data.game_id,
                        user_name: username
                      }
                    }
                  );
                });
      
                
            }
          } catch (error) {
            console.error('Error creating user:', error);
          }
        }
      };

    return (
        <div className="flex items-center justify-center h-screen bg-color2 w-screen">
            <div className="text-center">
                <h1 className="text-4xl font-bold text-secondary mb-2">Welcome to MusDraw</h1>
                <p className="text-secondary mb-4">Draw what you hear and guess what others have drawn!</p>
                <form onSubmit={handleJoin} className="flex flex-col items-center">
                    <input
                        type="text"
                        placeholder="Enter your username"
                        className="mb-2 px-4 py-2 border rounded-md text-lg bg-primary"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <button
                        type="submit"
                        className="bg-primary text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        Join Game
                    </button>
                </form>
            </div>
        </div>
    );
};

export default WelcomePage;
