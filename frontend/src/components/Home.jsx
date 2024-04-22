import TopNav from "./TopNav";
import Button from "./Button";
import { useAuth } from "../context/auth";
import { useNavigate } from "react-router-dom";
function Home()
{   const navigate = useNavigate();
    const buttonClick = ()=>{
        navigate("/login");
    }
    const {isLoggedIn} =  useAuth;
    return(
        <div className="text-center p-4 m-4 text-xl">
        <h1>This is the pony express chat application used to chat with friends<br/> if you have an account pls log in or else register</h1>  
        <Button  onClick={buttonClick}> get Started</Button>
        </div>
    )
}


export default Home;