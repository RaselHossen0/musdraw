import React from 'react';

function MessageCard({ isSender, message, userName, timeStamp, avatarSrc }) {
    //console.log(message);
    return (
        <div className={`flex ${isSender ? 'flex-row-reverse' : 'flex-row'} items-start gap-2.5`}>
          
            <div className="flex flex-col gap-1 ">
                <div className={`flex items-center ${isSender ? 'justify-end' : ''} space-x-2 rtl:space-x-reverse`}>
                    <span className="text-sm font-semibold text-primary dark:text-primary">{ isSender?"Me":userName}</span>
                    
                </div>
                <div className={`flex flex-col leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl ${isSender ? 'rounded-e-none bg-primary dark:bg-color3' : 'rounded-es-none dark:bg-primary'}`}>
                    <p className={`text-sm font-normal text-white   ${isSender? 'dark:text-white':'dark:text-white'} `}>{message}</p>
                </div>
                
            </div>
            
           
        </div>
    );
}

export default MessageCard;
