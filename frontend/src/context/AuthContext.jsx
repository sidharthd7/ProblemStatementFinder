import {createContext, useContext, useState } from 'react'

const AuthContext = createContext(null);

export const AuthProvider = ({children}) => {
    const [user, setUser] = useState(null);

    const login = async (email, password) => {
        // TODO: Implement actual login logic with your backend
        try {
            // Mock login for now
            setUser({ email });
            return true;
        } catch (error) {
            console.error('Login failed:', error);
            return false;
        }
    };

    const signup = async (email, password) => {
        // TODO: Implement actual signup logic with your backend
        try {
          // Mock signup for now
          setUser({ email });
          return true;
        } catch (error) {
          console.error('Signup failed:', error);
          return false;
        }
    };

    const logout = () => {
        setUser(null);
    };


  return (
    <AuthContext.Provider value={{user, login, signup, logout}}>
        {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
    const context = useContext(AuthContext);

    if(!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};