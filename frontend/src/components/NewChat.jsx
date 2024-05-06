import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/auth";
import Button from "./Button";
import FormInput from "./FormInput";

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


function NewChat() {
  const [chatName, setChatName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const onSubmit = (e) => {
    e.preventDefault();
    console.log("chat creaated witth chat name" + chatName)
    // this will navigate to the chat id that has been created
  }

  return (
    <div className="max-w-96 mx-auto py-8 px-4">
      <form onSubmit={onSubmit}>
        <FormInput type="text" name="ChatName" setter={setChatName}/>
        <Button className="w-full" type="submit">
          create
        </Button>
        <Error message={error} />
      </form>
    </div>
  );
}

export default NewChat;