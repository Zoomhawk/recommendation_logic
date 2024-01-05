import bodyParser from 'body-parser';
import express from 'express';
const app = express();
import cp from 'child_process';
import cors from 'cors'
import { getUserFavouriteList, updateRecommendationToFireBase } from './firebase.js';


app.use(cors())

app.use(bodyParser.json())

const port = process.env.PORT || 3080


app.post("/",(req,resp)=>{
    if(req.body == undefined)
    {
        resp.send("No data given to process !!!")
        return
    }
    let email = req.body.email
    console.log("email: ", email)
    getUserFavouriteList(email).then((result)=>{
        result = JSON.parse(result)
        console.log(result)
        console.log("computing recommendations")
        let output = cp.spawnSync("python",['logic.py', ...result ])
        output = output.stdout.toString()
        console.log("recommendations computed")
        // console.log(output + "sumit")
        output = JSON.parse(output)
        console.log(typeof(output))
        updateRecommendationToFireBase(email,output).then(()=>{console.log(`Recommendations updated for ${email}`)}).catch((error=>{console.log(error)}))
        resp.send("recommendations computed")
    }).catch((error)=>{
        console.log(error)
        resp.send("recommedation error")
    })


    // resp.send("done")
    // resp.send(output.stdout.toString())

})

app.listen(port,()=>{
    console.log(`server is live at ${port}`)
})