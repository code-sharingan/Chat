import { useQuery,useQueryClient } from "react-query"
import { NavLink, useNavigate, useParams } from "react-router-dom";
import "./Chats.css"
import { useState } from "react";
import Button from "./Button";
import { useAuth } from "../context/auth";
import ScrollContainer from "./ScrollContainer";


function MessageForm({chatid})
{       const navigate = useNavigate();  
        const [message,setMessage] =  useState("")
        const {token} =  useAuth();
        const queryClient = useQueryClient();
        const onChange = (e)=>{setMessage(e.target.value)}
        
        const onSubmit = (e)=>{
            const m =  {text:message}
            e.preventDefault();
            fetch(
                `http://127.0.0.1:8000/chats/${chatid}/messages`,
                {
                  method: "POST",
                  headers: {
                    "Authorization": "Bearer " + token, "Content-Type": "application/json"
                  },body: JSON.stringify(m),
                },
              ).then((response) => {
                if (response.ok) {
                    queryClient.invalidateQueries({
                        queryKey:["chats",chatid]
                    });
                } 
                else {
                    console.log("error")
                }
              });
        }
        return(
            <form onSubmit={onSubmit} className="flex flex-row text-black-500">
            <input type ="text" onChange = {onChange} value={message} placeholder="new message" className="border rounded px-4 py-2 w-96 h-12 m-3 border-solid bg-slate-500"/>
            <Button className="w-24" type="submit" >send </Button>
            </form>
        )
}
function ChatCard({chatId})
{
    if(chatId)
    {
        const {data}=useQuery({
            queryKey:["chats",chatId],
            queryFn: ()=>(
                fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
                .then((response)=>response.json())
            ),
        })
    if(data && data.messages)
    {
       return(
        // the current className=" col-span-2 chat-card flex flex-col flex-1 h-96 overflow-y-scroll m-2 border-solid border-2 border-orange-500"
        <div className=" col-span-2 chat-card flex flex-col flex-1 max-h-fitted ">
            <ScrollContainer>
                {data.messages.map((message)=>(
                    <div className="message-box  border-solid border-2 border-yellow-500 w-auto h-auto p-2 m-4">
                        <div className="user-name flex flex-row text-sm text-green-500">
                            <div className="mr-2">{message.user.username}  -</div>
                            <div>{new Date(message.created_at).toDateString()}{new Date(message.created_at).toLocaleTimeString()}</div>
                        </div>
                    <div className="user-message">{message.text}</div>
                    </div>
                ))}
            </ScrollContainer>
            <div className="border-solid border-t-4 border-blue-400">
            <MessageForm chatid={chatId}/>
            </div>
        </div>
       )
    }
    }
   
    return(<div className=" col-span-2 chat-card flex flex-col flex-1 max-h-fitted ">
        <h1>Select a chat</h1>
    </div>)
}
function ChatList()
{
    
    const {data}=useQuery({
        queryKey:["chats"],
        queryFn: ()=>(
            fetch("http://127.0.0.1:8000/chats")
            .then((response)=>response.json())
        )
    })
    // const classname = [ , active?  : "border-green"].join(" ");
    //--------------------- fix this hover over the chat and selected chat thing
    // const linkClass = ["flex flex-col" , "border-2 rounded","mb-4 p-2","hover:bg-zinc-900"].join(" ")
    // const getLinkClass= ({isActive})=>(isActive ? linkClass+" bg-zinc-500 border-orange-400" : linkClass);


//   // const getLinkClass= ({isActive})=>(
//   //   isActive ? linkClass+" bg-gray-500" : linkClass
//   // );

    // const className = ["text-left", "p-4","hover:bg-zinc-500"].join(" ")
    // const {activeChatId,setActivechatid} = useState(null)
    // const chatEvent = (cahtid)=>{setActivechatid(cahtid)}
    // const getClassName = (chatid) => (
    //     chatid == activeChatId ? className + " bg-purple-500 text-green-500" : className
    //   ); 

    const linkClass = ["text-left", "p-4","hover:bg-zinc-500"].join(" ")
    const getLinkClass= ({isActive})=>(
    isActive ? linkClass+" bg-gray-500 text-green-500" : linkClass
  );
    if(data &&data.chats)
    {
        return(
            <div className="col-span-1 flex flex-col max-h-fitted border-r-2 border-l-4 border-blue-400 font-extrabold text-3xl ">
                {data.chats.map((chat)=>(
                    <NavLink className={getLinkClass} key={chat.id} to={`/chats/${chat.id}`} id={chat.id} onClick={()=>{chatEvent(chat.id)}} >{chat.name}</NavLink>
                ))}
            </div>
        )
    }
    
}

function Chats()
{
    const {chatId} = useParams();
    return (
        <div>
            <div className="grid grid-cols-3">
                <ChatList/>
                <ChatCard chatId={chatId}/>
            </div>
        </div>
        
        
        )
}

export default Chats