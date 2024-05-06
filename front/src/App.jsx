import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';

import WelcomePage from './components/WelcomePage';
import GameRoom from './components/GameRoom';
import WaitingRoom from './game/WaitingRoom';
import { SocketProvider } from './providers/SocketProvider';
import { UserProvider } from './providers/UserContext';

function App() {
  return (
    
    <Router>
     <SocketProvider> 
        <UserProvider>


        <Routes>
          <Route path="/" element={<WelcomePage  />} />
          <Route path="/waiting_room" element={<WaitingRoom />} />
        
        </Routes>
        </UserProvider>
        </SocketProvider>
     
    </Router>
   
  );
}

export default App;
