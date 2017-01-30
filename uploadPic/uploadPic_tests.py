import os
import sys
import io
import unittest
import tempfile
import uploadPic

class MyTestCase(unittest.TestCase):
    def setUp(self):
        uploadPic.app.config['TESTING'] = True
        self.app = uploadPic.app.test_client()
        print sys.path[0]
        os.chdir(sys.path[0])


    #Accessing "upload" with GET returns error message
    #In the future, we will want to change this to a redirection
    #back to the original form
    def test_upload_GET(self):
        rv = self.app.get('/upload')
        assert b'File upload failed, please try again' in rv.data

    #Posting a valid photo gives back redirect link to
    #uploads/<filename>
    def test_upload_Photo(self):
        data = dict(photo=(io.BytesIO(b'jpg test'), 'test.jpg'))
        rv = self.app.post('/upload', content_type='multipart/form-data',
                           data=data)
        assert b'<a href="/uploads/test.jpg">' in rv.data

    #Posting an invalid file type gives back error
    def test_upload_Pdf(self):
        data = dict(photo=(io.BytesIO(b'pdf test'), 'test.pdf'))
        rv = self.app.post('/upload', content_type='multipart/form-data',
                           data=data)
        assert b'Please upload a valid file' in rv.data

        #Add: test that jpg file is available, and has the right contents
        #Add: test that form shows up?

if __name__ == '__main__':
    unittest.main()
