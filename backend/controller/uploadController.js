// Controller to handle file upload

const uploadFile = (req, res) => {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }
  
    res.status(200).json({
      message: 'File uploaded successfully',
      file: req.file,
    });
  };
  
  module.exports =uploadFile ;
  