import mongoose, { Schema, Types } from "mongoose";

const noteSchema = Schema(
  {
    note_title: { type: String, require: true },
    note_desc: { type: String, require: true },
    userId: { type: Types.ObjectId, require: true },
  },
  { timestamps: true }
);

const NoteModel = mongoose.model("note",noteSchema)
export default NoteModel
