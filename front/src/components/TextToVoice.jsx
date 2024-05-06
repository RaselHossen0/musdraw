import React, { useState } from 'react';

const TextToSpeech = () => {
    const [text, setText] = useState('');

    const handleTextChange = (event) => {
        setText(event.target.value);
    };

    const speakText = () => {
        if (!window.speechSynthesis) {
            alert('Text to speech not supported in this browser.');
            return;
        }
        const utterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(utterance);
    };

    return (
        <div>
            {/* <input type="text" value={text} onChange={handleTextChange} placeholder="Enter text here" className='' /> */}
            <button onClick={speakText} className='bg-primary'>Speak</button>
        </div>
    );
};

export default TextToSpeech;
