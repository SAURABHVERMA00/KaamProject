const multer = require('multer');
const { GridFsStorage } = require('multer-gridfs-storage');

// MongoDB Atlas URI
const mongoURI = '';

// Set up GridFS storage
const storage = new GridFsStorage({
  url: mongoURI,
  options: { useNewUrlParser: true, useUnifiedTopology: true }, // Important for Atlas
  file: (req, file) => {
    return {
      filename: file.originalname,
      bucketName: 'uploads', // This creates "uploads.files" and "uploads.chunks" collections in your suncast DB
    };
  }
});

// Multer upload middleware
const upload = multer({ storage });

module.exports = upload;
