import { useEffect, useState } from "react";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";
import Button from "./Button";
import FormInput from "./FormInput";
import { useNavigate } from "react-router-dom";
function Profile() {
  const { logout,token } = useAuth();
  const user = useUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [created_at,setCreatedAt] = useState("")
  const [readOnly, setReadOnly] = useState(true);
  const navigate = useNavigate();

  const reset = () => {
    if (user) {
      setUsername(user.username);
      setEmail(user.email);
      setCreatedAt(user.created_at);
    }
  }

  const clickLogout=()=>{
    logout();
    navigate("/login")
  }

  useEffect(reset, [user]);

  const onSubmit = (e) => {
    e.preventDefault();
    const body=  {username:username ,  email:email}
    fetch(
      `http://127.0.0.1:8000/users/me`,
      {
        method: "PUT",
        headers: {
          "Authorization": "Bearer " + token, "Content-Type": "application/json"
        },body: JSON.stringify(body),
      },
    ).then((response) => {
      if (response.ok) {
        console.log("ok")
      } 
      else {
          console.log("error")
      }
    });
    setReadOnly(true);
  }

  const onClick = () => {
    setReadOnly(!readOnly);
    reset();
  };

  return (
    <div className="max-w-96 mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold py-2">
        details
      </h2>
      <form className="border rounded px-4 py-2" onSubmit={onSubmit}>
        <FormInput
          name="username"
          type="text"
          value={username}
          readOnly={readOnly}
          setter={setUsername}
        />
        <FormInput
          name="email"
          type="email"
          value={email}
          readOnly={readOnly}
          setter={setEmail}
        />
        <FormInput name="created-at"
          type="text"
          value={new Date(created_at).toDateString() +"  "+new Date(created_at).toLocaleTimeString() }
          readOnly = {true}/>
        {!readOnly &&
          <Button className="mr-8" type="submit">
            update
          </Button>
        }
        <Button type="button" onClick={onClick}>
          {readOnly ? "edit" : "cancel"}
        </Button>
      </form>
      <Button onClick={clickLogout}>
        logout
      </Button>
    </div>
  );
}

export default Profile;




// const linkClass = ["text-left", "p-4","hover:bg-zinc-500"].join(" ")
//     const getLinkClass= ({isActive})=>(
//     isActive ? linkClass+" bg-gray-500" : linkClass
//   );