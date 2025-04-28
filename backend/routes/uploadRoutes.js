const express = require('express');
const router = express.Router();
const  uploadFile  = require('../controller/uploadController');
const multer = require('multer');
const path = require('path');
const app = express();
const cors = require('cors');

// Allow frontend requests
app.use(cors());

// Create storage for uploaded files
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'divanshi/uploadedfile'); // folder path where files will be saved
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname); // keep original file name
  }
});

// Create upload middleware
const upload = multer({ storage: storage });
// POST /upload
router.post('/', upload.single('file'), uploadFile);



module.exports = router;
