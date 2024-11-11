import express from "express";
import cors from "cors";
import mongoose from "mongoose";
import cookieParser from "cookie-parser";
import bodyParser from "body-parser";
import { offlinedb, PORT } from "./config.mjs";
import universalCookieMiddleware from "universal-cookie-express";
import note_route from "./routes/note_route.mjs";

const app = express();
app.use(bodyParser.json());
app.use(cookieParser());

app.use(universalCookieMiddleware());
app.use(
  cors({
    origin: "*",
    credentials: true,
  })
);

//middleware routes

app.use("/api/note", note_route);

mongoose
  .connect(offlinedb)
  .then(console.log("note service database connected"))
  .catch((err) => {
    console.log(err.message);
    mongoose.disconnect();
  });

app.listen(PORT, () => {
  console.log("server running in port :" + PORT);
});
