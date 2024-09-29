import jwt from "jsonwebtoken";
import { SECRET_KEY } from "../config.mjs";

async function isAuthenticate(req, res, next) {
  try {
    const token = req.universalCookies.get("access_token");
    if (!token) {
      return res.json("token is not found");
    }
    jwt.verify(token, SECRET_KEY, (err, decode) => {
      if (err) {
        return res.json("token have a mistake or invalid");
      }
      req.userId = decode.userId;
      next();
    });
  } catch (error) {
    next(error);
  }
}
export default isAuthenticate;
