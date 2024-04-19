import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter,NavLink, Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import Chats from './components/Chats';
const queryClient = new QueryClient();


function Nav()
{
  const linkClass = [
    "border-r-2 border-blue-400",
    "py-2 px-4",
    "hover:bg-gray-500",
  ].join(" ")

  const getLinkClass= ({isActive})=>(
    isActive ? linkClass+" bg-gray-500" : linkClass
  );
    return(
      <nav className='flex flex-row border-b-4 border-blue-400'>
        <NavLink to="/" className={getLinkClass}>Home</NavLink>
        <div className="flex-1"></div>
        <NavLink to ="/chats"className={getLinkClass}>login</NavLink>
      </nav>
    )
}
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
       <main className="max-w-3xl mx-auto bg-gray-700 text-white py-0 h-screen">
        <header> 
          <Nav/> 
        </header>
          <section>
            <Routes>
              <Route path="/" element={<Chats/>} />
              <Route path="/chats" element={<Chats/>}/>
              <Route path="/chats/:chatId"element={<Chats/>}/>
            </Routes>
          </section>
        </main>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
