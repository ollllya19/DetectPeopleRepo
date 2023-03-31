import cv2

class VideoGenerator:

    def __init__(self, 
            path1="./static/test1.mp4",
            path2='./static/test2.mp4', 
            out_video_path="./static/output.mp4",
            classif_path='./static/haarcascade_fullbody.xml'):
        self.human_cascade = cv2.CascadeClassifier(classif_path)
        self.stream1 = cv2.VideoCapture(path1)
        self.stream2 = cv2.VideoCapture(path2)
        self.out_video = None
        self.out_video_path = out_video_path
        

    def get_people_count(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        humans = self.human_cascade.detectMultiScale(gray, 1.9, 1)
        humanCount = len(humans)
        print(humanCount)
        return humanCount
    
    def make_out_size(self):
        width = int(self.stream1.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.stream1.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.stream1.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out_video = cv2.VideoWriter(self.out_video_path, fourcc, fps, (width*2, height))

    def get_out_video(self, frame1, frame2):
        videoCount1 = self.get_people_count(frame1)
        videoCount2 = self.get_people_count(frame2)

        if videoCount1 > videoCount2: return frame1
        else: return frame2

        
    def clear(self):
        self.stream1.release()
        self.stream2.release()
        self.out_video.release()
        cv2.destroyAllWindows()

    def get_video(self):
        if (not self.stream1.isOpened()) or (not self.stream2.isOpened()):
            print("Error opening input video streams")
            
        self.make_out_size()

        while (self.stream1.isOpened() and self.stream2.isOpened()):
            ret1, frame1 = self.stream1.read()
            ret2, frame2 = self.stream2.read()
            
            if (not ret1) or (not ret2):
                break

            rez_frame = self.get_out_video(frame1, frame2)
            
            ret, buffer = cv2.imencode('.jpg', rez_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        self.clear()