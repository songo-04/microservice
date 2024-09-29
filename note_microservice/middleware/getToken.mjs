import jwt from "jsonwebtoken";
import { SECRET_KEY } from "../config.mjs";
async function getToken(req, res, next) {
  try {
    const token = req.universalCookies.get("token");
    if (!token) {
      return res.json({ isConnected: false });
    }
    jwt.verify(token, SECRET_KEY, (err, decode) => {
      if (err) {
        return res.json({ isConnected: false });
      } else {
        return res.json({ isConnected: true });
      }
    });
  } catch (error) {
    next(error);
  }
}
export default getToken;
