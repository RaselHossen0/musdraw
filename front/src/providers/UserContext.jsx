import React, { createContext, useState, useContext, useEffect } from 'react';

class User {
    constructor(user_name = '', userId = null, gameId = null) {
        this.user_name = user_name;
        this.userId = userId;
        this.gameId = gameId;
    }
}

const UserContext = createContext(null);

export const useUser = () => useContext(UserContext);

export const UserProvider = ({ children, userData }) => {
    const [user, setUser] = useState(new User(userData?.user_name, userData?.userId, userData?.gameId));

    useEffect(() => {
        if (userData) {
            setUser(new User(userData.user_name, userData.userId, userData.gameId));
        }
    }, [userData]);
    // Function to update the user in useEffect
    const updateUser = (newUserData) => {
        setUser(new User(newUserData.user_name, newUserData.userId, newUserData.gameId));
    };

    

    // Function to update the user
    

    // Include updateUser in the context value
    return (
        <UserContext.Provider value={{ user, updateUser }}>
            {children}
        </UserContext.Provider>
    );
};

export default UserProvider;
