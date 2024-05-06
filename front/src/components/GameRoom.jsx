import React, { useState } from 'react';
import DrawingCanvas from './MainBoard';
import TextToSpeech from './TextToVoice';

export default function GameRoom() {
    const [players, setPlayers] = useState([
        { id: 1, name: "Player 1", score: 150 },
        { id: 2, name: "Player 2", score: 120 },
        // Add more players as needed
    ]);
    const [joinGame, setJoinGame] = useState(false);

    const handleJoinGame = () => {
        console.log("Join game logic here");
        // Join game logic
    };

    const handleClearBoard = () => {
        // Logic to clear the board
        console.log("Clear the drawing board");
    };

    return (
        // <div className="">
           
            <div className="p-5 h-screen">
                {/* <button
                    onClick={handleClearBoard}
                    className="mb-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 "
                >
                    Clear Board
                </button> */}
               
                
              
                
            </div>
        // </div>
    );
}
