import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, NavLink, Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import Chats from './components/Chats';
import Login from './components/Login';
import TopNav from './components/TopNav';
import { AuthProvider, useAuth } from "./context/auth";
import { UserProvider } from './context/user';
import Profile from './components/Profile';
import Registration from './components/Registration';
import PlsLogin from './components/PlsLogin';
import Error from './components/Error';
import Home from './components/Home';
import NewChat from './components/NewChat';
const queryClient = new QueryClient();


// function Nav()
// {
//   // const linkClass = [
//   //   "border-r-2 border-blue-400",
//   //   "py-2 px-4",
//   //   "hover:bg-gray-500",
//   // ].join(" ")

//   // const getLinkClass= ({isActive})=>(
//   //   isActive ? linkClass+" bg-gray-500" : linkClass
//   // );
//     return(
//       <nav className='flex flex-row border-b-4 border-blue-400'>
//         <NavLink to="/" className={getLinkClass}>Home</NavLink>
//         <div className="flex-1"></div>
//         <NavLink to ="/chats"className={getLinkClass}>login</NavLink>
//       </nav>
//     )
// }



function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Chats />} />
      <Route path="/chats" element={<Chats />} />
      <Route path="/chats/:chatId" element={<Chats />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="*" element={<Error/>}/>
      <Route path="/chats/new" element={<NewChat/>}/>
    </Routes>
  );
}


function NotAuthenticates()
{
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Registration />} />
      <Route path="/chats" element={<Navigate to="/plslogin"/>} />
      <Route path="/chats/:chatId" element={<Navigate to="/plslogin"/>} />
      <Route path="/profile" element={<Navigate to="/plslogin"/>} />
      <Route path="/plslogin" element={<PlsLogin/>}/>
      <Route path = "*" element={<Error/>}/>
    </Routes>
  );
}
function Header()
{
  return (
    <header>
      <TopNav />
    </header>
  );
}


function Main()
{   const{isLoggedIn} = useAuth();
    return(
        <main className='max-h-main'>
          { isLoggedIn? 
          <AuthenticatedRoutes/>:
          <NotAuthenticates/>
          }
        </main>
    )
}
function App() {
  const className = [
    "max-w-3xl mx-auto",
    "bg-zinc-800 text-white",
    "flex flex-col",
  ].join(" ");
  return (
    <QueryClientProvider client={queryClient}>
        <BrowserRouter>
        <AuthProvider>
          <UserProvider>
            <div className={className}>
            <Header/>
            <Main/>
            </div>
          </UserProvider>
        </AuthProvider> 
        </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
