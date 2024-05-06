import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useSocket } from '../providers/SocketProvider.jsx'; 
import MessageCard from '../cards/MessageCard.jsx';
import GameRoom from '../components/GameRoom.jsx';
import DrawingCanvas from '../components/MainBoard.jsx';

import { useLocation } from 'react-router-dom';
class Message {
    
    constructor(data) {
        // console.log(data);
        this.message_id = data.message_id;
        this.user_name = data.user_name;
        this.user_id = data.user_id;
        this.content = data.message;
    }
}
const WaitingRoom = (
    
) => {
    const [players, setPlayers] = useState(0);
    const [gameStatus, setGameStatus] = useState('Waiting for players...');
    const [message, setMessage] = useState('');
    const [chatMessages, setChatMessages] = useState([]);
    const [myMessages, setMyMessages] = useState([]);
    const location = useLocation();
    const userId = location.state.userId;
    const gameId = location.state.gameId;
    const user_name = location.state.user_name;
    const user = {
        userId: userId,
        gameId: gameId,
        user_name: user_name
    };
    
   
    const socket = useSocket();
   
  
   useEffect(() => {
    const handleNewMessage = (data) => {
        // console.log('New message:', data);
        const newMessage = new Message(data);
        console.log('New message:', newMessage);
        setChatMessages(prevMessages => {
            // Check if the message ID already exists to avoid duplicates
            if (!prevMessages.some(msg => parseInt(msg.message_id, 10) === parseInt(newMessage.user_id, 10))) {
                return [...prevMessages, newMessage];
            }
            return prevMessages;
        });
    };

    socket.on('new_message', handleNewMessage);

    return () => {
        socket.off('new_message', handleNewMessage);
    };
}, [socket]);


    const handleSendMessage = (e) => {
        e.preventDefault();
        if (message.trim()) {


            socket.emit('send_message', { user_id: user.userId,game_id:user.gameId,content: message });
            setMessage('');
        }
    };
    const handleLogOut = (e) => {
        e.preventDefault();
        localStorage.clear();
        window.location.href = '/';
    }

    return (
        <div 
        className='w-full h-screen p-10 bg-cover bg-no-repeat' 
        style={{ backgroundImage: 'url("https://t4.ftcdn.net/jpg/02/66/94/65/360_F_266946580_9fYk4P8vPcfQYgbGcrGPJgoGw70kpBAp.jpg")' }}
    >
<div className='flex flex-row h-full bg-white rounded-lg overflow-hidden shadow-lg'>
        <div className="lg:flex-[1_1_23%] text-lg text-gray-700 p-5 bg-color2 overflow-hidden">
            <h1 className="text-2xl font-bold mb-2 text-white">Welcome to <span>MusDraw</span>  </h1>
            <h1 className="text-3xl font-semibold text-color3 border-gray-100">{user.user_name} !</h1>
            {/* <p>{gameStatus}</p>
            <p>Connected Players: {players}</p> */}
            <div className="mt-4 w-full">
                <h2 className="text-lg font-semibold text-slate-100 rounded-lg">Chat</h2>
                <div className=" h-96 mb-2 p-2 bg-white mt-2 rounded overflow-y-auto" >
                    {chatMessages.map((msg, index) => (
                        <MessageCard
                            key={index}
                            isSender={parseInt(msg.user_id, 10) === parseInt(user.userId, 10)}
                            message={msg.content}
                            userName={msg.user_name || "Unknown"} // Provide a default or pull from a user map
                            timeStamp={msg.timeStamp || "Time"} 
                            avatarSrc={"/path/to/default/avatar.jpg"} 
                        />
                    ))}
                </div>
                <form onSubmit={handleSendMessage} className="flex p-2">
                    <input
                        type="text"
                        className="flex-grow p-2 rounded-l-lg focus:outline-none focus:ring mr-2 bg-slate-400 text-black"
                        placeholder="Type a message..."
                        value={message}
                        onChange={e => setMessage(e.target.value)}
                    />
                    <button
                        type="submit"
                        className="bg-primary text-white p-2 rounded-r-lg hover:bg-blue-600"
                    >
                        Send
                    </button>
                </form>
            </div>
            <div className='mb-2'>
                <button className="bg-primary text-white p-2 rounded-lg  mb-2">Log Out</button>
            </div>
        </div>
        <div className='flex-1 '>
            <DrawingCanvas />
        </div>
        
    </div>
    </div>
    
    );
};

export default WaitingRoom;
