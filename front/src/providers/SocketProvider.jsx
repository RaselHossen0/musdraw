import React, { createContext, useContext, useEffect, useState } from 'react';
import io from 'socket.io-client';

const SocketContext = createContext(null);
import { useNavigate } from 'react-router-dom';

export const useSocket = () => useContext(SocketContext);

export const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);
    const navigate = useNavigate(); // Create navigate function instance
    useEffect(() => {
        const newSocket = io(`http://localhost:8000`); // Adjust URL as needed
        setSocket(newSocket);

        return () => newSocket.close();
    }, []);
    useEffect(() => {
        // Redirect if socket is null
        if (!socket) {
            navigate('/');
        }
    }, [socket, navigate]); // Add navigate to the dependency array

    return (
        <SocketContext.Provider value={socket}>
            {children}
        </SocketContext.Provider>
    );
};
