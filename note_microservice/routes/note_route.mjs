import express from "express";
import {
  create_note,
  delete_one_note,
  get_all_note,
  get_one_note,
  patch_one_note,
} from "../controller/note_controller.mjs";
import isAuthenticate from "../middleware/isAuthenticated.mjs";

const note_route = express.Router();

note_route.post("/", isAuthenticate, create_note);
note_route.get("/", isAuthenticate, get_all_note);
note_route.get("/:id", get_one_note);
note_route.patch("/:id", patch_one_note);
note_route.delete("/:id", delete_one_note);

export default note_route;
