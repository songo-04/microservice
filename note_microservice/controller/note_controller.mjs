import NoteModel from "../model/note_model.mjs";

async function create_note(req, res, next) {
  try {
    const userId = req.userId;
    const { note_title, note_desc } = req.body;
    if (!note_title || !note_desc) {
      return res.json({
        message: "data is empty",
      });
    }
    const new_note = NoteModel({
      note_title,
      note_desc,
      userId: userId,
    });
    await new_note.save();
    res.json({
      note: new_note,
    });
  } catch (error) {
    next(error);
  }
}

async function get_all_note(req, res, next) {
  try {
    const userId = req.userId;
    const notes = await NoteModel.find({ userId: userId });
    if (!notes || notes.length == 0 ) {
      return res.json({ message: "note note found or empty" });
    }
    res.json(notes);
  } catch (error) {
    next(error);
  }
}

async function get_one_note(req, res, next) {
  try {
    console.log("first");
    res.json({ message: "ok" });
  } catch (error) {
    next(error);
  }
}

async function patch_one_note(req, res, next) {
  try {
    console.log("first");
    res.json({ message: "ok" });
  } catch (error) {
    next(error);
  }
}

async function delete_one_note(req, res, next) {
  try {
    console.log("first");
    res.json({ message: "ok" });
  } catch (error) {
    next(error);
  }
}

export {
  create_note,
  get_all_note,
  get_one_note,
  patch_one_note,
  delete_one_note,
};
