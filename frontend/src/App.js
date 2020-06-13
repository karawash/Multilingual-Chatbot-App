import React from 'react';
import './App.css';
import BotUI from 'botui';

function App() {
  var botui = new BotUI('botui-app') // id of container
  let dobj = {
      "demand": "hi",
    }; 
  let bot= "how can I help you?";
  let resValue = '';
  let result = '';
  function messageContent(){
  botui.message.add({ 
    content: bot
  }).then(function () { 
    return botui.action.text({ 
      action: {
        placeholder: 'Say something'
      }
    }).then( function (res) {
     resValue = res.value;
     fetchdata(resValue)
     console.log(result);
     
  });
  });
  
  }
  
  async function fetchdata(resValue){
     dobj = {
      "demand": resValue ,
    };
  
   let response = await fetch('http://127.0.0.1:5002/api/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(dobj)
    });
    
    result = await response.json();
    bot = result.response;
    messageContent();
  }
  
  messageContent();
    
  return (
    <div className="App">
           
    </div>
  );
}


export default App;
