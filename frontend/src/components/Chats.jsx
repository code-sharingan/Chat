import { useQuery } from "react-query"
import { Link, useParams } from "react-router-dom";
import "./Chats.css"

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
        <div className="chat-card flex flex-col flex-1 h-96 overflow-y-scroll m-2 border-solid border-2 border-orange-500">
            {data.messages.map((message)=>(
                <div className="message-box  border-solid border-2 border-yellow-500 w-auto h-auto p-2 m-2">
                    <div className="user-name flex flex-row text-sm text-green-500">
                        <div className="mr-2">{message.user.username}  -</div>
                        <div>{new Date(message.created_at).toDateString()}{new Date(message.created_at).toLocaleTimeString()}</div>
                    </div>
                <div className="user-message">{message.text}</div>
                </div>
            ))}
        </div>
       )
    }
    }
   
    return(<div>
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
    if(data &&data.chats)
    {
        return(
            <div className="chat-List-Container">
                {data.chats.map((chat)=>(
                    <div className="chat-box border-solid border-2 border-orange-500 width-200 m-2">
                        <Link key={chat.id} to={`/chats/${chat.id}`}className="chat-name" id={chat.id}>{chat.name}</Link>
                        <div className="participants text-xs">
                        <br/>
                        <>created-at:{chat.created_at}</>
                        </div>
                    </div>
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
            <h1>PONY-EXPRESS</h1>
            <div className="main-container flex flex-row">
                <ChatList/>
                <ChatCard chatId={chatId}/>
            </div>
        </div>
        
        
        )
}

export default Chats