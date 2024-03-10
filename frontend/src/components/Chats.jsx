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
    console.log(data)
    if(data && data.messages)
    {
       return(
        <div className="chat-card">
            {data.messages.map((message)=>(
                <div className="message-box">
                    <div className="user-name">
                        <div>{message.user_id}  -</div>
                        <div>{message.created_at}</div>
                    </div>
                <div className="user-message">{message.text}</div>
                </div>
            ))}
        </div>
       )
    }
    }
   
    return(<div className="chat-card">
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
                    <div className="chat-box">
                        <Link key={chat.id} to={`/chats/${chat.id}`}className="chat-name" id={chat.id}>{chat.name}</Link>
                        <div className="participants">
                        {chat.user_ids.map((user)=>(
                            <>{user} </>
                        ))}
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
        <div className="main-container">
        <ChatList/>
        <ChatCard chatId={chatId}/>
        </div>
        
        )
}

export default Chats