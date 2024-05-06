import React, { useEffect, useRef, useState } from 'react';
import { useSocket } from '../providers/SocketProvider'; 
const DrawingCanvas = () => {
    const [isDrawing, setIsDrawing] = useState(false);
    const canvasRef = useRef(null);
    const contextRef = useRef(null);
    const socket = useSocket();
    const game_id=localStorage.getItem('gameId');
   
    useEffect(() => {
        const canvas = canvasRef.current;
        const canvasWidth = window.innerWidth * 0.7; // 80% of window width
        const canvasHeight = window.innerHeight ; // 80% of window height
        canvas.width = canvasWidth * 2; // For high DPI screens
        canvas.height = canvasHeight * 2; // For high DPI screens
        canvas.style.width = `${canvasWidth}px`;
        canvas.style.height = `${canvasHeight}px`;

        const context = canvas.getContext("2d");
        context.scale(2, 2);
        context.lineCap = "round";
        context.strokeStyle = "black";
        context.lineWidth = 5;
        contextRef.current = context;

      

        socket.on("drawing_rcv", data => {
            console.log('Drawing:', data);
            const x=data.x;
            const y=data.y;
            const type=data.type;
            console.log(x, y, type);
            if (type === "draw") {
                contextRef.current.lineTo(x, y);
                contextRef.current.stroke();
            } else if (type === "start") {
                console.log('start');
                contextRef.current.beginPath();
                contextRef.current.moveTo(x, y);
            }
        });
    }, []);

    const startDrawing = ({ nativeEvent }) => {
        const { offsetX, offsetY } = nativeEvent;
        contextRef.current.beginPath();
        contextRef.current.moveTo(offsetX, offsetY);
        setIsDrawing(true);
        socket.emit("draw", { type: "start", x: offsetX, y: offsetY ,game_id:game_id});
    };
    
    const draw = ({ nativeEvent }) => {
        if (!isDrawing) {
            return;
        }
        const { offsetX, offsetY } = nativeEvent;
        contextRef.current.lineTo(offsetX, offsetY);
        contextRef.current.stroke();
        socket.emit("drawing", { type: "draw", x: offsetX, y: offsetY,game_id:game_id });
    };
    
    const stopDrawing = () => {
        contextRef.current.closePath();
        setIsDrawing(false);
        // Emitting stop drawing might not be necessary unless you want to handle it specially on the server
    };
    

    return (
        <div className='w-100 bg-white'>
        <canvas
        className="drawing-canvas"
            onMouseDown={startDrawing}
            onMouseUp={stopDrawing}
            onMouseMove={draw}
            ref={canvasRef}
        />
        </div>
    );
};

export default DrawingCanvas;
