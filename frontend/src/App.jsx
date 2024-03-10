import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import Chats from './components/Chats';
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Chats/>} />
          <Route path="/chats" element={<Chats/>}/>
          <Route path="/chats/:chatId"element={<Chats/>}/>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
