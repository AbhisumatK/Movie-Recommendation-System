import React, { useEffect, useState } from "react";
import "./css/Home.css";
import axios from "axios";

const Home = () => {
    const [name, setName] = useState("");
    const [err, setErr] = useState("");
    const [output, setOutput] = useState([]);

    const HandleSubmit = (e) => {
        e.preventDefault();
        if (!name) {
            setOutput([]);
            return setErr("*Field cannot be empty!*")
        };
        axios.post("http://127.0.0.1:5000/prediction", {title: name})
        .then(res => {
            if (res.data.result.length == 0) {
                setOutput(["Movie with this name doesn't exist"]);
            }
            else {
                setOutput(res.data.result);
            }
        })
    }

    return (
        <div className="container">
            <h1>Movie Recommendation</h1>
            <div className="input">
                <input type="text" className="input-search" placeholder={err ? err : "Search"} onChange={(e) => {setName(e.target.value); setErr("")}}/>
                <button type="submit" className="btn-search" onClick={HandleSubmit}>Send</button>
            </div>
            <div className="output" style={{display: output.length != 0 ? "flex" : "none"}}>
                {output.map((m, i) => <><li className="m-list">{m}</li></>)}
            </div>
        </div>
    )
}

export default Home;