import { useQuery,useQueryClient } from "react-query"
import { NavLink, useNavigate, useParams } from "react-router-dom";
import "./Chats.css"
import { useState } from "react";
import Button from "./Button";
import { useAuth } from "../context/auth";
import ScrollContainer from "./ScrollContainer";

// my frontend contains .css files but the are all commented out
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
                    setMessage("")
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


function EditMessageForm({message,onChange , onCancel,onSubmit})
{
    // const onChange = (e)=>{setNewText(e.target.value)}

    return(
        <form onSubmit = {onSubmit}>
            <textarea className="w-full border rounded border-blue-300 text-black "
             value={message}
             onChange={onChange}
            />
            <div>
                <button className="border rounded border-bulue-300 w-36" type ="submit">Save</button>
                <button className="border rounded border-bulue-300 mx-4 w-36" type="button" onClick={onCancel}>cancel</button>
            </div>
        </form>
    )
}
function Error({ message }) {
    if (message === "") {
      return <></>;
    }
    return (
      <div className="text-red-300 text-xs">
        {message}
      </div>
    );
  }
function ChatCard({chatId})
{   const queryClient = useQueryClient();
    const {token} =  useAuth();
    const [error, setError] = useState("");
    const [editMessageId,setEditMessageID] =  useState(null);
    const [newText,setNewText]  = useState("")
    const onEditClick = (id,message)=>{
        setNewText(message);
        setEditMessageID(id);
    }
    const onDeleteClick = (chat_id,message_id)=>{
        fetch(
            `http://127.0.0.1:8000/chats/${chat_id}/messages/${message_id}`,
            {
              method: "delete",
              headers: {
                "Authorization": "Bearer " + token, "Content-Type": "application/json"
              },
            },
          ).then((response) => {
            if (response.ok) {
                queryClient.invalidateQueries({
                    queryKey:["chats",chat_id]
                });
                setError("")
            } 
            else if(response.status ===403) {
                setError("You dont have permission to delete this message")
            }
          });
        }
    const onCancel=()=>{
        setEditMessageID(null);
    }
    const onChange = (e)=>{setNewText(e.target.value)
        console.log(newText)
    }
    const onSubmit=(e)=>{
        e.preventDefault();
        const text = newText
        fetch(
            `http://127.0.0.1:8000/chats/${chatId}/messages/${editMessageId}`,
            {
              method: "put",
              headers: {
                "Authorization": "Bearer " + token, "Content-Type": "application/json"
              }, body: JSON.stringify({ text}),
            },
          ).then((response) => {
            if (response.ok) {
                queryClient.invalidateQueries({
                    queryKey:["chats",chatId]
                });
                setError("")
                setEditMessageID(null);
            } 
            else if(response.status ===403) {
                setError("You dont have permission to edit this message");
                setEditMessageID(null);
            }
          });
    }
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
                    <div className="message-box  border-solid border-2 rounded-md  border-blue-100 shadow-sm shadow-blue-500 w-auto h-auto p-2 m-4">
                        <div className="user-name flex flex-row text-sm text-green-500  justify-between items-center mb-2">
                            <div className="flex flex-row items-strech">
                                <div >{message.user.username}   -       </div>
                                <div>
                                    {new Date(message.created_at).toDateString()}{new Date(message.created_at).toLocaleTimeString()}
                                </div>
                                <div/>
                                <div  className=" flex flex-rowmx-1 my-1 h-8 w-24 text-center text-white-500">
                                    <button  onClick= {()=>onDeleteClick(chatId,message.id)} className="border rounded border-blue-300 w-full ml-4">x</button>
                                    <button onClick = {()=>onEditClick(message.id,message.text)} className="border rounded border-blue-300 w-full">e</button>
                                </div>
                            </div>
                        </div>
                    { editMessageId ===message.id ? 
                        <EditMessageForm  message={newText} onChange={onChange} onCancel={onCancel} onSubmit={onSubmit}/> : 
                        <div >{message.text}</div>
                    }
                    
                    </div>
                ))}
            </ScrollContainer>
            <Error message={error}/>
            <div className="border-solid border-t-4 border-blue-400">
            <MessageForm chatid={chatId}/>
            </div>
        </div>
       )
    }
    }
   
    return(<div className=" col-span-2 chat-card flex flex-col flex-1 max-h-fitted text-center m-4">
        <h1>Select a chat</h1>
    </div>)
}





function ChatList()
{
    const {token} =  useAuth();
    const {data}=useQuery({
        queryKey:["chats"],
        queryFn: ()=>(
            fetch("http://127.0.0.1:8000/chats",
                {
                    method: "get",
              headers: {
                "Authorization": "Bearer " + token, "Content-Type": "application/json"
              }
                }
            )
            .then((response)=>response.json())
        )
    })
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